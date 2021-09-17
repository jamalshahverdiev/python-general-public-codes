from src.variables import app
from flask import request
from datetime import datetime as dt
import logging


@app.after_request
def after_request(response):
    """ Logging after every request. """
    logger = logging.getLogger("app.access")
    logger.info(
        "%s [%s] %s %s %s %s %s %s %s",
        request.remote_addr,
        dt.utcnow().strftime("%d/%b/%Y:%H:%M:%S.%f")[:-3],
        request.method,
        request.path,
        request.scheme,
        response.status,
        response.content_length,
        request.referrer,
        request.user_agent,
    )
    return response
