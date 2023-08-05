from sanic.views import HTTPMethodView
from sanic import response
from sanic.exceptions import ServerError
from naas.types import t_asset, t_health, t_error, t_start
import uuid
import os


class AssetsController(HTTPMethodView):
    __logger = None
    __jobs = None
    __path_lib_files = None
    __path_html_error = None
    __assets_files = "assets"
    __html_files = "html"
    __manager_error = "error.html"

    def __init__(self, logger, jobs, path_assets, *args, **kwargs):
        super(AssetsController, self).__init__(*args, **kwargs)
        self.__logger = logger
        self.__jobs = jobs
        self.__path_lib_files = path_assets
        self.__path_html_error = os.path.join(
            self.__path_lib_files, self.__html_files, self.__manager_error
        )
        print("self.__path_html_error", self.__path_html_error)

    def __html_error(self, content):
        try:
            with open(self.__path_html_error, "r") as f:
                template = f.read()
                f.close()
                return template.replace("{ERROR}", content)
        except Exception:
            print("Cannot get html error")
            return ""

    async def get(self, request, token):
        if token == "up" or token == "down" or token.startswith("naas_"):
            ext = ".png"
            if token.startswith("naas_"):
                ext = ".svg"
            return await response.file(
                os.path.join(
                    self.__path_lib_files, self.__assets_files, f"{token}{ext}"
                )
            )
        else:
            uid = str(uuid.uuid4())
            task = await self.__jobs.find_by_value(uid, token, t_asset)
            if task:
                file_filepath = task.get("path")
                params = task.get("params", dict())
                self.__logger.info(
                    {
                        "id": uid,
                        "type": t_asset,
                        "status": t_start,
                        "filepath": file_filepath,
                        "token": token,
                    }
                )
                try:
                    await self.__jobs.update(
                        uid, file_filepath, t_asset, token, params, t_health, 1
                    )
                    res = await response.file(file_filepath)
                    self.__logger.info(
                        {
                            "id": uid,
                            "type": t_asset,
                            "status": t_start,
                            "filepath": file_filepath,
                            "token": token,
                        }
                    )
                    return res
                except Exception as e:
                    self.__logger.error(
                        {
                            "id": uid,
                            "type": t_asset,
                            "status": t_error,
                            "filepath": file_filepath,
                            "token": token,
                            "error": e,
                        }
                    )
                    await self.__jobs.update(
                        uid, file_filepath, t_asset, token, params, t_error, 1
                    )
                    raise ServerError({"id": uid, "error": e}, status_code=404)
            self.__logger.error(
                {
                    "id": uid,
                    "type": t_asset,
                    "status": t_error,
                    "error": "Cannot find your token",
                    "token": token,
                }
            )
            raise ServerError(
                {"id": uid, "error": "Cannot find your token", "token": token},
                status_code=404,
            )
