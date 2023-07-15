from fastapi import HTTPException
from http.client import responses


class Response:
    def __init__(self, status_code: int, message: str, excecution: str) -> None:
        self.message = message
        self.status_code = status_code
        self.excecution_time = excecution

    def response(self):
        if self.status_code == 200:
            mapper = {
                "metaData": {
                    "status": True,
                    "message": responses[self.status_code],
                    "timeExecution": self.excecution_time
                }, "data": self.message
            }
            return mapper
        raise HTTPException(self.status_code, {"metaData": {
            "status": False,
            "message": responses[self.status_code],
            "timeExecution": self.excecution_time
        }})
