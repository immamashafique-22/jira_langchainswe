Sure! Below is a complete FastAPI application code based on the provided Jira ticket description, along with corresponding unit tests using Pytest.

### FastAPI Application Code

```python
# app.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Model for the request body
class Ticket(BaseModel):
    title: str
    description: str

# In-memory storage for tickets
tickets = []

@app.post("/tickets/", response_model=Ticket)
async def create_ticket(ticket: Ticket):
    # Simulate ticket creation
    tickets.append(ticket)
    return ticket

@app.get("/tickets/", response_model=list[Ticket])
async def get_tickets():
    return tickets

@app.get("/tickets/{ticket_id}", response_model=Ticket)
async def get_ticket(ticket_id: int):
    if ticket_id < 0 or ticket_id >= len(tickets):
        raise HTTPException(status_code=404, detail="Ticket not found")
    return tickets[ticket_id]

@app.delete("/tickets/{ticket_id}", response_model=Ticket)
async def delete_ticket(ticket_id: int):
    if ticket_id < 0 or ticket_id >= len(tickets):
        raise HTTPException(status_code=404, detail="Ticket not found")
    return tickets.pop(ticket_id)
```

### Unit Tests with Pytest

```python
# test_app.py

import pytest
from fastapi.testclient import TestClient
from app import app, Ticket

client = TestClient(app)

def test_create_ticket():
    response = client.post("/tickets/", json={"title": "Test Ticket via LangChain SWE", "description": "This ticket was created via LangChain SWE pipeline"})
    assert response.status_code == 200
    assert response.json() == {"title": "Test Ticket via LangChain SWE", "description": "This ticket was created via LangChain SWE pipeline"}

def test_get_tickets():
    response = client.get("/tickets/")
    assert response.status_code == 200
    assert len(response.json()) == 1  # We just created one ticket

def test_get_ticket():
    response = client.get("/tickets/0")
    assert response.status_code == 200
    assert response.json() == {"title": "Test Ticket via LangChain SWE", "description": "This ticket was created via LangChain SWE pipeline"}

def test_get_non_existent_ticket():
    response = client.get("/tickets/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found"}

def test_delete_ticket():
    response = client.delete("/tickets/0")
    assert response.status_code == 200
    assert response.json() == {"title": "Test Ticket via LangChain SWE", "description": "This ticket was created via LangChain SWE pipeline"}

def test_delete_non_existent_ticket():
    response = client.delete("/tickets/0")
    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found"}
```

### Instructions to Run the Application and Tests

1. **Install FastAPI and Uvicorn**:
   ```bash
   pip install fastapi uvicorn
   ```

2. **Run the FastAPI Application**:
   ```bash
   uvicorn app:app --reload
   ```

3. **Install Pytest**:
   ```bash
   pip install pytest
   ```

4. **Run the Tests**:
   ```bash
   pytest test_app.py
   ```

This setup provides a simple FastAPI application that allows creating, retrieving, and deleting tickets, along with unit tests to verify the functionality.