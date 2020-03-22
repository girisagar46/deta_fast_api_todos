import logging
import random
import sys

from deta.lib import Database
from fastapi import FastAPI, Path
from starlette.responses import JSONResponse

from models import Todo

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
logger.addHandler(handler)

app = FastAPI(openapi_prefix="/rzzj7f2jw5ih/")

todos = Database("todos")

app.add_route("/openapi.json", lambda req: JSONResponse(app.openapi()),
              include_in_schema=False)


@app.get(
    "/",
    summary="Get all todo list",
    tags=["todos"]
)
async def get_all_todos(
        # limit: int = Query(None, description="limit of result", le=10)
):
    logger.info("[GET] /")
    return todos.all()


@app.get(
    "/{todo_id}",
    summary="Get one todo item",
    tags=["todos"],
)
async def get_todo(
        todo_id: str = Path(..., description="Get a todo object with ID")
):
    todo = todos.get(todo_id)
    return todo


@app.post(
    "/",
    summary="Add a todo item",
    tags=["todos"],
    status_code=201,
    response_model=Todo,
)
async def create_todo(todo: Todo):
    todo_item = todo.dict()
    logger.info(todo_item)
    _id = str(random.getrandbits(128))[:5]
    todos.put(_id, todo_item)

    return todo_item


@app.put(
    "/{todo_id}",
    summary="Update a todo item",
    status_code=201,
    tags=["todos"],
    response_model=Todo,
)
async def update_todo(todo_id: str, todo: Todo):
    todos.put(todo_id, todo.dict())
    return todo.dict()


@app.delete(
    "/{todo_id}",
    summary="Delete a todo item",
    tags=["todos"],
    status_code=200
)
async def delete_todo(todo_id: str):
    todos.delete(todo_id)
    return todos.all()
