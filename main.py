import json

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import request


class ServiceException(Exception):
    def __init__(self, message=None, code=None):
        self.message = message
        self.code = code

    def __str__(self):
        if self.message:
            return "ServiceException, {}".format(self.message)
        else:
            return "ServiceException has been raused."


class ServerHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            if self.path == "/converter":
                self.data_string = self.rfile.read(
                    int(self.headers['Content-Length'])
                )

                try:
                    content = json.loads(self.data_string)
                except json.decoder.JSONDecodeError:
                    raise ServiceException(
                        "Bad Request",
                        400
                    )

                req = request.urlopen("https://www.cbr-xml-daily.ru/daily_json.js")
                req = json.loads(req.read())

                if not req:
                    raise ServiceException(
                        "Page Not Found",
                        404
                    )

                valute = req.get("Valute").get(content["Valute"])

                resp = {
                    "Valute": content["Valute"],
                    "Value": content["Value"],
                    "Result": round(content["Value"] * valute["Value"], 4),
                }

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(resp).encode('utf-8'))
            else:
                raise ServiceException(
                    "Page Not Found",
                    404
                )
        except ServiceException as error:
            self.send_response(error.code)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(
                {"error": error.message}
            ).encode('utf-8'))


def server_thread(port):
    server_address = ("0.0.0.0", port)
    httpd = HTTPServer(server_address, ServerHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


if __name__ == "__main__":
    port = 8000
    print("Starting server at port %d" % port)
    server_thread(port)
