import logging
from pprint import pprint

import aiohttp

logging.basicConfig(level=logging.DEBUG)

async def hello_world(send):
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [
                [b"content-type", b"text/html"],
            ],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": b"<h1>Hello, World!</h1>",
        }
    )

async def error_404(send):
    await send(
        {
            "type": "http.response.start",
            "status": 404,
            "headers": [
                [b"content-type", b"text/html"],
            ],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": b"<h1>Not Found</h1>",
        }
    )

async def app(scope, receive, send):
    if scope["type"] != "http":
        return

    pprint(scope)

    routes = {
        '/': hello_world
    }

    await receive()

    func = routes.get(scope['path'], error_404)
    await func(send)
