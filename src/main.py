from typing import Union
from fastapi import FastAPI
import schemas
import firebase_admin
from firebase_admin import firestore

db = firestore.client()
app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: schemas.Item):
    return {"item_name": item.name, "item_id": item_id}
