import json
import logging
import traceback
from http.server import BaseHTTPRequestHandler

# App
from external import get_currency_data
from exceptions import (
    ServerException,
    NotFoundException,
    BadRequestException
)


logger = logging.getLogger("server")


class ServerHandler(BaseHTTPRequestHandler):
    DEFAULT_RESPONSE_HEADERS = {
        "Content-Type": "text/html"
    }

    def set_headers(self, headers: dict) -> None:
        for key, value in headers.items():
            self.send_header(key, value)

        self.end_headers()

    def writer_response(self, data, headers=None, code=200):
        if headers:
            response_headers = {**self.DEFAULT_RESPONSE_HEADERS, **headers}
        else:
            response_headers = {**self.DEFAULT_RESPONSE_HEADERS}

        self.send_response(code)
        self.set_headers(headers=response_headers)
        self.wfile.write(data)

        logger.info(f"{code} Response {data} for {self.path}")

    def json_writer(self, data, headers=None, code=200):
        respone_headers = {
            "Content-Type": "application/json"
        }

        if headers:
            respone_headers.update(headers)

        self.writer_response(
            json.dumps(data).encode('utf-8'),
            headers=respone_headers,
            code=code
        )

    def json_error_writer(self, error: str, code: int = 500) -> None:
        self.json_writer({"error": str(error)}, code=code)

    def get_request_data(self):
        try:
            return self.rfile.read(
                int(self.headers['Content-Length'])
            )
        except KeyError:
            raise BadRequestException("Request is not valid")

    def log_message(self, format, *args):
        pass

    def do_GET(self):
        try:
            if self.path == "/converter":
                try:
                    req_data = json.loads(self.get_request_data())
                    logger.info(f"GET {self.path} data: {req_data}")
                except json.decoder.JSONDecodeError:
                    raise BadRequestException(
                        "Bad Request: provided data is not json")

                try:
                    data = json.loads(get_currency_data())
                except json.decoder.JSONDecodeError:
                    raise ServerException(
                        "Failed to validate currency server responce")

                try:
                    valute = data["Valute"][req_data["valute"]]
                except KeyError:
                    raise NotFoundException("Data Not Found")

                self.json_writer({
                    "valute": req_data["valute"],
                    "value": req_data["value"],
                    "result": round(req_data["value"] * valute["Value"], 4),
                })

            else:
                raise NotFoundException("Page Not Found")
        except ServerException as error:
            logger.error(f"GET {self.path} error: {error.message}")
            self.json_error_writer(error.message, error.code)
        except Exception:
            logger.error(traceback.format_exc())
            self.json_error_writer("Internal server error", 500)
