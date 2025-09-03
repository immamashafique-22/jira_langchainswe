Certainly! Below is a complete FastAPI application code along with unit tests using Pytest. The application will include a simple endpoint that returns a message indicating that the ticket was created via the LangChain SWE pipeline.

### FastAPI Application Code

```python
# app.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Ticket(BaseModel):
    title: str
    description: str

@app.post("/tickets/")
async def create_ticket(ticket: Ticket):
    return {
        "message": "Ticket created successfully",
        "ticket": ticket
    }

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Ticket API"}
```

### Unit Tests using Pytest

```python
# test_app.py
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Ticket API"}

def test_create_ticket():
    ticket_data = {
        "title": "Test Ticket via LangChain SWE",
        "description": "This ticket was created via LangChain SWE pipeline"
    }
    response = client.post("/tickets/", json=ticket_data)
    assert response.status_code == 200
    assert response.json() == {
        "message": "Ticket created successfully",
        "ticket": ticket_data
    }

def test_create_ticket_invalid_data():
    # Testing with missing title
    ticket_data = {
        "description": "This ticket was created via LangChain SWE pipeline"
    }
    response = client.post("/tickets/", json=ticket_data)
    assert response.status_code == 422  # Unprocessable Entity
```

### Instructions to Run the Application and Tests

1. **Install FastAPI and Uvicorn**:
   Make sure you have FastAPI and Uvicorn installed. You can install them using pip:
   ```bash
   pip install fastapi uvicorn
   ```

2. **Run the FastAPI Application**:
   You can run the FastAPI application using Uvicorn:
   ```bash
   uvicorn app:app --reload
   ```

3. **Install Pytest**:
   If you haven't installed Pytest yet, you can do so with:
   ```bash
   pip install pytest
   ```

4. **Run the Tests**:
   You can run the tests using the following command:
   ```bash
   pytest test_app.py
   ```

This setup provides a simple FastAPI application with a ticket creation endpoint and corresponding unit tests to ensure the functionality works as expected.