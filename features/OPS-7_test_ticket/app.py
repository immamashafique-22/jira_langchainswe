Certainly! Below is a complete FastAPI application code along with unit tests using Pytest. Since the Jira ticket does not provide specific functionality, I will create a simple FastAPI app that includes a basic CRUD (Create, Read, Update, Delete) functionality for a resource called "Item".

### FastAPI Application Code

```python
# app/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Data model
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

# In-memory database (for demonstration purposes)
items_db = {}

@app.post("/items/", response_model=Item)
def create_item(item: Item):
    if item.id in items_db:
        raise HTTPException(status_code=400, detail="Item already exists")
    items_db[item.id] = item
    return item

@app.get("/items/", response_model=List[Item])
def read_items():
    return list(items_db.values())

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = item
    return item

@app.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    deleted_item = items_db.pop(item_id)
    return deleted_item
```

### Unit Tests with Pytest

```python
# tests/test_main.py

import pytest
from fastapi.testclient import TestClient
from app.main import app, Item

client = TestClient(app)

def test_create_item():
    response = client.post("/items/", json={"id": 1, "name": "Item 1", "description": "A test item"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Item 1", "description": "A test item"}

def test_read_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Item 1", "description": "A test item"}]

def test_read_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Item 1", "description": "A test item"}

def test_update_item():
    response = client.put("/items/1", json={"id": 1, "name": "Updated Item", "description": "An updated test item"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Updated Item", "description": "An updated test item"}

def test_delete_item():
    response = client.delete("/items/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Updated Item", "description": "An updated test item"}

def test_read_nonexistent_item():
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

def test_create_duplicate_item():
    response = client.post("/items/", json={"id": 1, "name": "Item 1", "description": "A test item"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Item already exists"}
```

### Instructions to Run the Application and Tests

1. **Install FastAPI and Uvicorn**:
   ```bash
   pip install fastapi uvicorn
   ```

2. **Install Pytest**:
   ```bash
   pip install pytest
   ```

3. **Run the FastAPI application**:
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Run the tests**:
   ```bash
   pytest tests/
   ```

This code provides a simple FastAPI application with CRUD operations for an "Item" resource and includes unit tests to verify the functionality. You can expand upon this base as needed based on additional requirements.