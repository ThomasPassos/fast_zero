from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.routers import auth, todos, users
from fast_zero.schemas import Message

app = FastAPI(title="Minha API de aprendizado")
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Olá Mundo!"}


@app.get(
    "/hello_world", status_code=HTTPStatus.OK, response_class=HTMLResponse
)
def hello_world():
    return "<h1>Olá Mundo!</h1>"
