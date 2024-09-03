from fastapi import FastAPI
from pydantic import BaseModel



app = FastAPI()


class HelloWorld(BaseModel):
    value: str = 'Hello, world!'


@app.get("/")
async def home()-> HelloWorld:
    hw = HelloWorld()
    return hw