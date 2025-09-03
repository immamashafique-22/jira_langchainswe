Certainly! Below is a complete FastAPI application code based on the provided Jira ticket description, along with pytest-based test cases.

### FastAPI Application Code

```python
# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Model for the ticket
class Ticket(BaseModel):
    id: int
    title: str
    description: str

# In-memory storage for tickets
tickets_db = []

@app.post("/tickets/", response_model=Ticket)
async def create_ticket(ticket: Ticket):
    # Check if the ticket ID already exists
    if any(t.id == ticket.id for t in tickets_db):
        raise HTTPException(status_code=400, detail="Ticket ID already exists")
    
    tickets_db.append(ticket)
    return ticket

@app.get("/tickets/", response_model=List[Ticket])
async def get_tickets():
    return tickets_db

@app.get("/tickets/{ticket_id}", response_model=Ticket)
async def get_ticket(ticket_id: int):
    ticket = next((t for t in tickets_db if t.id == ticket_id), None)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@app.delete("/tickets/{ticket_id}", response_model=Ticket)
async def delete_ticket(ticket_id: int):
    global tickets_db
    ticket = next((t for t in tickets_db if t.id == ticket_id), None)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    tickets_db = [t for t in tickets_db if t.id != ticket_id]
    return ticket
```

### Pytest-Based Test Cases

```python
# test_main.py

import pytest
from fastapi.testclient import TestClient
from main import app, Ticket

client = TestClient(app)

def test_create_ticket():
    response = client.post("/tickets/", json={"id": 1, "title": "Test Ticket", "description": "This ticket is created using Python script."})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Test Ticket", "description": "This ticket is created using Python script."}

def test_create_ticket_duplicate_id():
    client.post("/tickets/", json={"id": 2, "title": "Another Ticket", "description": "Another ticket description."})
    response = client.post("/tickets/", json={"id": 2, "title": "Duplicate Ticket", "description": "This should fail."})
    assert response.status_code == 400
    assert response.json() == {"detail": "Ticket ID already exists"}

def test_get_tickets():
    response = client.get("/tickets/")
    assert response.status_code == 200
    assert len(response.json()) == 2  # We have created two tickets

def test_get_ticket():
    response = client.get("/tickets/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Test Ticket", "description": "This ticket is created using Python script."}

def test_get_ticket_not_found():
    response = client.get("/tickets/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found"}

def test_delete_ticket():
    response = client.delete("/tickets/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Test Ticket", "description": "This ticket is created using Python script."}

def test_delete_ticket_not_found():
    response = client.delete("/tickets/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found"}

def test_get_tickets_after_deletion():
    response = client.get("/tickets/")
    assert response.status_code == 200
    assert len(response.json()) == 1  # Only one ticket should remain after deletion
```

### Instructions to Run the Application and Tests

1. **Install FastAPI and Uvicorn**:
   ```bash
   pip install fastapi uvicorn
   ```

2. **Run the FastAPI Application**:
   ```bash
   uvicorn main:app --reload
   ```

3. **Install Pytest**:
   ```bash
   pip install pytest
   ```

4. **Run the Tests**:
   ```bash
   pytest test_main.py
   ```

This code provides a simple FastAPI application for managing tickets, along with a set of unit tests to ensure the functionality works as expected. You can expand upon this base as needed for your application.