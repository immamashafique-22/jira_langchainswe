Sure! Below is a complete FastAPI application code along with unit tests using Pytest. The application will have a simple endpoint that returns a message indicating that the ticket was created via the API.

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
    return {"message": "Ticket created successfully", "ticket": ticket}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Unit Tests with Pytest

```python
# test_app.py
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_create_ticket():
    response = client.post("/tickets/", json={"title": "Test Ticket", "description": "This ticket is created using Python script."})
    assert response.status_code == 200
    assert response.json() == {
        "message": "Ticket created successfully",
        "ticket": {
            "title": "Test Ticket",
            "description": "This ticket is created using Python script."
        }
    }

def test_create_ticket_missing_fields():
    response = client.post("/tickets/", json={"title": "Test Ticket"})
    assert response.status_code == 422  # Unprocessable Entity
    assert response.json()["detail"][0]["msg"] == "field required"
```

### Instructions to Run the Application and Tests

1. **Install FastAPI and Uvicorn**:
   Make sure you have FastAPI and Uvicorn installed. You can install them using pip:

   ```bash
   pip install fastapi uvicorn
   ```

2. **Run the FastAPI Application**:
   Save the FastAPI code in a file named `app.py`. You can run the application using the following command:

   ```bash
   uvicorn app:app --reload
   ```

   This will start the FastAPI server at `http://127.0.0.1:8000`.

3. **Install Pytest**:
   If you haven't installed Pytest yet, you can do so with:

   ```bash
   pip install pytest
   ```

4. **Run the Tests**:
   Save the test code in a file named `test_app.py`. You can run the tests using the following command:

   ```bash
   pytest test_app.py
   ```

This setup provides a simple FastAPI application that can create tickets and includes unit tests to verify the functionality. The tests check both the successful creation of a ticket and the validation of required fields.