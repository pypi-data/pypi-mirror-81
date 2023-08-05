from .proxy import encode_proxy_url
import pretty_cron
import requests
import base64
import json
import os
import uuid


class Notifications:
    logger = None
    base_notif_url = os.environ.get("NOTIFICATIONS_API", None)

    def __init__(self, logger):
        self.logger = logger

    def send(self, email, subject, content, html=None):
        uid = str(uuid.uuid4())
        if self.base_notif_url is None:
            jsn = {"id": uid, "type": "email error", "error": "not configured"}
            self.logger.error(json.dumps(jsn))
            return jsn
        try:
            data = {
                "subject": subject,
                "email": email,
                "content": content,
                "html": html,
            }
            req = requests.post(url=f"{self.base_notif_url}/send", json=data)
            req.raise_for_status()
            jsn = req.json()
            return jsn
        except Exception as err:
            self.logger.error(
                json.dumps({"id": uid, "type": "email error", "error": str(err)})
            )

    def send_notif(self, uid, status, email, file_path, current_type):
        if self.base_notif_url is None:
            jsn = {"id": uid, "type": "notification error", "error": "not configured"}
            self.logger.error(json.dumps(jsn))
            return jsn
        content = f"Your {file_path} accesible as {current_type} is {status}, check the Logs on your manager below :"
        status_url = f"{encode_proxy_url('assets')}/{status}.png"
        message_bytes = file_path.encode("ascii")
        base64_bytes = base64.b64encode(message_bytes)
        file_path_base64 = base64_bytes.decode("ascii")
        link_url = f"{encode_proxy_url('manager')}/?filter={file_path_base64}"
        logo_url = f"{encode_proxy_url('manager')}/asset/naas_logo"
        try:
            data = {
                "subject": f"{current_type.capitalize()} {status}",
                "email": email,
                "title": "Naas manager notification",
                "content": content,
                "image": status_url,
                "vars": {
                    "URL_HOME": encode_proxy_url("manager"),
                    "URL_LOGO": logo_url,
                    "ALT_LOGO": "Naas Manager",
                    "URL_IMAGE": status_url,
                    "URL_LINK": link_url,
                },
            }
            req = requests.post(url=f"{self.base_notif_url}/send_notif", json=data)
            req.raise_for_status()
            jsn = req.json()
            return jsn
        except Exception as err:
            self.logger.error(
                json.dumps({"id": uid, "type": "notification error", "error": str(err)})
            )

    def get_status_server(self):
        req = requests.get(url=f"{self.base_notif_url}/")
        req.raise_for_status()
        jsn = req.json()
        return jsn

    def send_scheduler(self, uid, status, email, file_path, cron_str):
        if self.base_notif_url is None:
            jsn = {"id": uid, "type": "notification error", "error": "not configured"}
            self.logger.error(json.dumps(jsn))
            return jsn
        cron_string = pretty_cron.prettify_cron(cron_str)
        content = f"Your {file_path} who run {cron_string} is {status}, check the Logs on your manager below :"
        status_url = f"{encode_proxy_url('assets')}/{status}.png"
        message_bytes = file_path.encode("ascii")
        base64_bytes = base64.b64encode(message_bytes)
        file_path_base64 = base64_bytes.decode("ascii")
        link_url = f"{encode_proxy_url('manager')}/?filter={file_path_base64}"
        try:
            data = {
                "subject": f"Sheduler {status}",
                "email": email,
                "content": content,
                "image": status_url,
                "link": link_url,
            }
            req = requests.post(url=f"{self.base_notif_url}/send", json=data)
            req.raise_for_status()
            jsn = req.json()
            return jsn
        except Exception as err:
            self.logger.error(
                json.dumps({"id": uid, "type": "notification error", "error": str(err)})
            )

    def send_error(self, uid, error, file_path):
        if self.base_notif_url is None:
            jsn = {"id": uid, "type": "notification error", "error": "not configured"}
            self.logger.error(json.dumps(jsn))
            return jsn
        email = os.environ.get("JUPYTERHUB_USER", None)
        if email is not None:
            content = f"Your {file_path} got Errors : {error},  during run N: {uid} \n Check the Logs on your manager below :"
            status_url = f"{encode_proxy_url('assets')}/down.png"
            message_bytes = file_path.encode("ascii")
            base64_bytes = base64.b64encode(message_bytes)
            file_path_base64 = base64_bytes.decode("ascii")
            link_url = f"{encode_proxy_url('manager')}/?filter={file_path_base64}"
            try:
                data = {
                    "subject": "Manager Error",
                    "email": email,
                    "content": content,
                    "image": status_url,
                    "link": link_url,
                }
                req = requests.post(url=f"{self.base_notif_url}/send", json=data)
                req.raise_for_status()
                jsn = req.json()
                return jsn
            except Exception as err:
                self.logger.error(
                    json.dumps(
                        {"id": uid, "type": "notification error", "error": str(err)}
                    )
                )
