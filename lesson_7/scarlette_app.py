from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route


async def hello_world(request):
    return PlainTextResponse("Hello, world!")


app = Starlette(
    routes=[
        Route("/", hello_world),
    ],
)