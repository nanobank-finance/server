from typing import Union
from fastapi import FastAPI
import schemas

app = FastAPI()


@app.get("/login")
async def login(username: str, password: str) -> bool:
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: schemas.Item):
    return {"item_name": item.name, "item_id": item_id}
