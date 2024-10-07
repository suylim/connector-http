
from typing import Any

import requests  # type: ignore
from spiffworkflow_connector_command.command_interface import CommandResultDictV1
from spiffworkflow_connector_command.command_interface import ConnectorCommand
import xmltodict
import json
from requests.auth import HTTPDigestAuth

class PutRequestV2(ConnectorCommand):
    def __init__(self,
        url: str,
        headers: dict[str, str] | None = None,
        data: dict[str, str] | None = None,
        basic_auth_username: str | None = None,
        basic_auth_password: str | None = None,
        
    ):
        self.url = url
        self.headers = headers or {}
        self.basic_auth_username = basic_auth_username
        self.basic_auth_password = basic_auth_password
        self.data = data or {}

    # backend
    #   spiffworkflow-proxy
    #     GetRequest returns CommandResultDictV1
    def execute(self, _config: Any, _task_data: Any) -> CommandResultDictV1:
        auth = None
        if self.basic_auth_username is not None and self.basic_auth_password is not None:
            # auth = (self.basic_auth_username, self.basic_auth_password)
            auth=HTTPDigestAuth(self.basic_auth_username,self.basic_auth_password)

        try:
            response = requests.request("PUT",self.url, self.params, headers=self.headers, auth=auth, data=self.data,timeout=300,verify=False)

            return {
                "response": response.text,
                "status": response.status_code,
                "mimetype": "application/json",
            }
        except Exception as e:
            return {
                "response": f'{"error": {e}}',
                "status": 500,
                "mimetype": "application/json",
            }

