from fastapi import FastAPI

app = FastAPI()
items = []
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/items")
def create_item(item: str):
    items.append(item)
    return items

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return items[item_id]

@app.put("/items/{item_id}")
def update_item(item_id: int, item: str):
    items[item_id] = item
    return items

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    items.pop(item_id)
    return items