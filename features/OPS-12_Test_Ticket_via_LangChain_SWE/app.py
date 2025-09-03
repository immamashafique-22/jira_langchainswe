Certainly! Below is a complete FastAPI application code based on the provided Jira ticket description, along with corresponding unit tests using Pytest.

### FastAPI Application Code

```python
# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Ticket(BaseModel):
    title: str
    description: str

@app.post("/tickets/", response_model=Ticket)
async def create_ticket(ticket: Ticket):
    if not ticket.title or not ticket.description:
        raise HTTPException(status_code=400, detail="Title and description are required.")
    return ticket

@app.get("/tickets/{ticket_id}", response_model=Ticket)
async def read_ticket(ticket_id: int):
    # In a real application, you would fetch the ticket from a database
    # Here we are simulating a ticket retrieval
    if ticket_id == 1:
        return Ticket(title="Test Ticket via LangChain SWE", description="This ticket was created via LangChain SWE pipeline")
    else:
        raise HTTPException(status_code=404, detail="Ticket not found")
```

### Unit Tests with Pytest

```python
# test_app.py
import pytest
from fastapi.testclient import TestClient
from app import app, Ticket

client = TestClient(app)

def test_create_ticket():
    response = client.post("/tickets/", json={"title": "Test Ticket", "description": "This is a test ticket."})
    assert response.status_code == 200
    assert response.json() == {"title": "Test Ticket", "description": "This is a test ticket."}

def test_create_ticket_missing_fields():
    response = client.post("/tickets/", json={"title": "", "description": ""})
    assert response.status_code == 400
    assert response.json() == {"detail": "Title and description are required."}

def test_read_ticket():
    response = client.get("/tickets/1")
    assert response.status_code == 200
    assert response.json() == {"title": "Test Ticket via LangChain SWE", "description": "This ticket was created via LangChain SWE pipeline"}

def test_read_ticket_not_found():
    response = client.get("/tickets/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found"}
```

### Instructions to Run the Application and Tests

1. **Install FastAPI and Uvicorn**:
   Make sure you have FastAPI and Uvicorn installed. You can install them using pip:
   ```bash
   pip install fastapi uvicorn
   ```

2. **Run the FastAPI Application**:
   Save the FastAPI code in a file named `app.py` and run the application using Uvicorn:
   ```bash
   uvicorn app:app --reload
   ```

3. **Install Pytest**:
   If you haven't already, install Pytest:
   ```bash
   pip install pytest
   ```

4. **Run the Tests**:
   Save the test code in a file named `test_app.py` and run the tests using:
   ```bash
   pytest test_app.py
   ```

This setup provides a basic FastAPI application with a ticket creation and retrieval feature, along with unit tests to ensure the functionality works as expected.