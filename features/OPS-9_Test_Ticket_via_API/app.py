Certainly! Below is a complete FastAPI application code that handles a simple API endpoint for a "Test Ticket" and corresponding unit tests using Pytest.

### FastAPI Application Code

```python
# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Data model for a ticket
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

### Pytest Unit Tests

```python
# test_app.py
import pytest
from fastapi.testclient import TestClient
from app import app, Ticket

client = TestClient(app)

def test_create_ticket():
    response = client.post("/tickets/", json={"id": 1, "title": "Test Ticket", "description": "This ticket was created using Jira API."})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Test Ticket", "description": "This ticket was created using Jira API."}

def test_create_ticket_duplicate_id():
    client.post("/tickets/", json={"id": 2, "title": "Another Ticket", "description": "Another description."})
    response = client.post("/tickets/", json={"id": 2, "title": "Duplicate Ticket", "description": "This should fail."})
    assert response.status_code == 400
    assert response.json() == {"detail": "Ticket ID already exists"}

def test_get_tickets():
    response = client.get("/tickets/")
    assert response.status_code == 200
    assert len(response.json()) == 2  # Assuming we created 2 tickets

def test_get_ticket():
    response = client.get("/tickets/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Test Ticket", "description": "This ticket was created using Jira API."}

def test_get_ticket_not_found():
    response = client.get("/tickets/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found"}

def test_delete_ticket():
    response = client.delete("/tickets/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Test Ticket", "description": "This ticket was created using Jira API."}

def test_delete_ticket_not_found():
    response = client.delete("/tickets/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found"}

def test_get_tickets_after_deletion():
    response = client.get("/tickets/")
    assert response.status_code == 200
    assert len(response.json()) == 1  # One ticket should remain after deletion
```

### Instructions to Run the Application and Tests

1. **Install FastAPI and Uvicorn**:
   ```bash
   pip install fastapi uvicorn
   ```

2. **Install Pytest**:
   ```bash
   pip install pytest pytest-asyncio
   ```

3. **Run the FastAPI Application**:
   ```bash
   uvicorn app:app --reload
   ```

4. **Run the Tests**:
   ```bash
   pytest test_app.py
   ```

This code provides a basic FastAPI application for managing tickets and includes unit tests to ensure that the API behaves as expected. You can expand upon this foundation based on your specific requirements.