from naas.types import t_notebook, t_scheduler, t_error, t_health
from .proxy import escape_kubernet
from sanic import response
import papermill as pm
import traceback
import json
import time
import bs4
import csv
import os
import io

kern_manager = None
try:
    from enterprise_gateway.services.kernels.remotemanager import RemoteKernelManager

    kern_manager = RemoteKernelManager
except ImportError:
    pass


class Notebooks:
    __logger = None
    __port = None
    __notif = None
    __api_internal = None

    def __init__(self, logger, notif=None):
        self.__port = int(os.environ.get("NAAS_RUNNER_PORT", 5000))
        self.__user = os.environ.get("JUPYTERHUB_USER", "joyvan@naas.com")
        self.__single_user_api_path = os.environ.get(
            "SINGLEUSER_PATH", ".jupyter-single-user.dev.svc.cluster.local"
        )
        self.__api_internal = f"http://jupyter-{escape_kubernet(self.__user)}{self.__single_user_api_path}:{self.__port}/"
        self.__logger = logger
        self.__notif = notif

    def response(self, uid, res, duration, params):
        next_url = params.get("next_url", None)
        if next_url is not None:
            if "http" not in next_url:
                next_url = f"{self.__api_internal}{next_url}"
            self.__logger.info(
                {"id": uid, "type": t_notebook, "status": "next_url", "url": next_url}
            )
            return response.redirect(next_url)
        else:
            res_data = self.__get_res(res)
            if res_data and res_data.get("type"):

                async def streaming_fn(res):
                    await res.write(str(res_data.get("data")).encode("utf-8"))

                return response.stream(streaming_fn, content_type=res_data.get("type"))
            else:
                return response.json({"id": uid, "status": "Done", "time": duration})

    def __convert_csv(self, data):
        soup = bs4.BeautifulSoup(data)
        output = []
        for table_num, table in enumerate(soup.find_all("table")):
            csv_string = io.StringIO()
            csv_writer = csv.writer(csv_string, delimiter=";", quoting=csv.QUOTE_ALL)
            for tr in table.find_all("tr"):
                row = [
                    "".join(cell.stripped_strings) for cell in tr.find_all(["td", "th"])
                ]
                csv_writer.writerow(row)
            table_attrs = dict(num=table_num)
            output.append((csv_string.getvalue(), table_attrs))
        return output[0][0]

    def __get_res(self, res):
        cells = res.get("cells")
        result = None
        result_type = None
        for cell in cells:
            outputs = cell.get("outputs", [])
            for output in outputs:
                metadata = output.get("metadata", [])
                data = output.get("data", dict())
                for meta in metadata:
                    if metadata[meta].get("naas_api"):
                        if data.get("application/json") and metadata[meta].get(
                            "naas_type"
                        ):
                            result_type = metadata[meta].get("naas_type")
                            try:
                                path = data.get("application/json").get("path")
                                with open(path, "r") as f:
                                    result = f.read()
                                    f.close()
                            except:  # noqa: E722
                                result_type = "application/json"
                                result = {"error": "file not found"}
                        elif data.get("application/json"):
                            result_type = "application/json"
                            result = json.dumps(data.get(result_type))
                        elif (
                            data.get("text/html")
                            and metadata[meta].get("naas_type") == "csv"
                        ):
                            result_type = "text/csv"
                            result = self.__convert_csv(data.get("text/html"))
                        elif data.get("text/html"):
                            result_type = "text/html"
                            result = data.get("text/html")
                        elif data.get("image/jpeg"):
                            result_type = "image/jpeg"
                            result = data.get("image/jpeg")
                        elif data.get("image/png"):
                            result_type = "image/png"
                            result = data.get("image/png")
                        elif data.get("image/svg+xml"):
                            result_type = "image/svg+xml"
                            result = data.get("image/svg+xml")
                        if result is not None or result_type is not None:
                            return {"type": result_type, "data": result}
        return None

    def __pm_exec(self, file_dirpath, file_filepath, file_filepath_out, params):
        if kern_manager:
            return pm.execute_notebook(
                input_path=file_filepath,
                output_path=file_filepath_out,
                progress_bar=False,
                cwd=file_dirpath,
                parameters=params,
                kernel_manager_class=kern_manager,
            )
        else:
            return pm.execute_notebook(
                input_path=file_filepath,
                output_path=file_filepath_out,
                progress_bar=False,
                cwd=file_dirpath,
                parameters=params,
            )

    async def exec(self, uid, job):
        value = job.get("value", None)
        current_type = job.get("type", None)
        file_filepath = job.get("path")
        if not os.path.exists(file_filepath):
            err = "file not found"
            self.__logger.error(
                {
                    "id": uid,
                    "type": "filepath",
                    "status": t_error,
                    "filepath": file_filepath,
                    "error": err,
                }
            )
            return {"error": err, "duration": 0}
        file_dirpath = os.path.dirname(file_filepath)
        file_filename = os.path.basename(file_filepath)
        file_filepath_out = os.path.join(file_dirpath, f"out_{file_filename}")
        params = job.get("params", dict())
        notif_down = params.get("notif_down", None)
        notif_up = params.get("notif_up", None)
        params["run_uid"] = uid
        start_time = time.time()
        res = None
        try:
            res = self.__pm_exec(file_dirpath, file_filepath, file_filepath_out, params)
        except pm.PapermillExecutionError as err:
            tb = traceback.format_exc()
            res = {"error": err, "traceback": str(tb)}
            self.__logger.error(
                {
                    "id": uid,
                    "type": "PapermillExecutionError",
                    "status": t_error,
                    "filepath": file_filepath,
                    "output_filepath": file_filepath_out,
                    "error": str(err),
                }
            )
        except pm.PapermillException as err:
            tb = traceback.format_exc()
            res = {"error": err, "traceback": str(tb)}
            self.__logger.error(
                {
                    "id": uid,
                    "type": "Exception",
                    "status": t_error,
                    "filepath": file_filepath,
                    "output_filepath": file_filepath_out,
                    "error": err,
                    "traceback": str(tb),
                }
            )
        except:  # noqa: E722
            tb = traceback.format_exc()
            res = {"error": "Unknow error", "traceback": str(tb)}
            self.__logger.error(
                {
                    "id": uid,
                    "type": "Exception",
                    "status": t_error,
                    "filepath": file_filepath,
                    "output_filepath": file_filepath_out,
                    "error": res.get("error"),
                    "traceback": str(tb),
                }
            )
        if not res:
            res = {"error": "Unknow error"}
            self.__logger.error(
                {
                    "id": uid,
                    "type": "Exception",
                    "status": t_error,
                    "filepath": file_filepath,
                    "output_filepath": file_filepath_out,
                    "error": res["error"],
                }
            )
        else:
            self.__logger.info(
                {
                    "id": uid,
                    "type": "Done",
                    "status": t_health,
                    "filepath": file_filepath,
                    "output_filepath": file_filepath_out,
                }
            )
        res["duration"] = time.time() - start_time
        if res.get("error"):
            email_admin = os.environ.get("JUPYTERHUB_USER", None)
            if email_admin is not None:
                self.__notif.send_status(
                    uid, "down", email_admin, file_filepath, current_type, value
                )
            if notif_down and self.__notif:
                self.__notif.send_status(
                    uid, "down", notif_down, file_filepath, current_type, value
                )
        elif notif_up and current_type == t_scheduler and self.__notif:
            self.__notif.send_status(
                uid, "up", notif_down, file_filepath, current_type, value
            )
        elif notif_up and self.__notif:
            self.__notif.send_status(uid, "up", notif_up, file_filepath, current_type)
        return res
