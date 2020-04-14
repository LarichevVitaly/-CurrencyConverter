import logging
from http.server import HTTPServer

# App
from logger import configure_logger
from handler import ServerHandler


logger = logging.getLogger("server")


def server_thread(port: int = 8000) -> None:
    server_address = ("0.0.0.0", port)
    httpd = HTTPServer(server_address, ServerHandler)

    try:
        logger.info(f"Starting server at port {port}")
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()


if __name__ == "__main__":
    configure_logger(logging.INFO)
    server_thread()
