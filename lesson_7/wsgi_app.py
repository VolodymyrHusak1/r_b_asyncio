import logging
import time
from pprint import pprint


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def app(env, start_response):
    if env['RAW_URI'] == '/':
        pprint(env)
        start_response("200 OK", [("Content-Type", "text/html")])
        return [b"<h1>Hello, World!</h1>"]
    start_response("404 Not Found", [("Content-Type", "text/html")])
    return [b"<h1>Not Found</h1>"]