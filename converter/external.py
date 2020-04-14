import logging
import traceback
from urllib import request

# App
from exceptions import ServerException


CURRENCY_REQ_URL = "https://www.cbr-xml-daily.ru/daily_json.js"
logger = logging.getLogger("server")


def get_currency_data():
    try:
        logger.info(f"Request currency data from {CURRENCY_REQ_URL}")
        req = request.urlopen(CURRENCY_REQ_URL)

        if req is None:
            raise Exception

        return req.read()
    except Exception:
        logger.error(traceback.format_exc())
        raise ServerException("Currency server is not avialiable", code=503)
