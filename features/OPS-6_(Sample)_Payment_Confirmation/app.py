Sure! Below is a complete FastAPI application that implements a payment confirmation feature, which sends an email receipt to the user after a successful transaction. Additionally, I've included unit tests using Pytest.

### FastAPI Application Code

```python
# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from starlette.middleware.cors import CORSMiddleware
import os

# Email configuration
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=587,
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_FROM_NAME="Payment Confirmation",
    MAIL_TLS=True,
    MAIL_SSL=False,
)

app = FastAPI()

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Payment(BaseModel):
    user_email: str
    amount: float
    transaction_id: str

@app.post("/confirm-payment/")
async def confirm_payment(payment: Payment):
    # Here you would typically process the payment and check if it was successful
    # For this example, we assume the payment is always successful

    # Send email receipt
    message = MessageSchema(
        subject="Payment Confirmation",
        recipients=[payment.user_email],
        body=f"Thank you for your payment of ${payment.amount}. Your transaction ID is {payment.transaction_id}.",
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)

    return JSONResponse(status_code=200, content={"message": "Payment confirmed and receipt sent."})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Unit Tests with Pytest

```python
# test_main.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def mock_payment_data():
    return {
        "user_email": "testuser@example.com",
        "amount": 100.0,
        "transaction_id": "123456789"
    }

def test_confirm_payment(mock_payment_data, monkeypatch):
    # Mock the email sending function
    async def mock_send_message(*args, **kwargs):
        return

    monkeypatch.setattr("fastapi_mail.FastMail.send_message", mock_send_message)

    response = client.post("/confirm-payment/", json=mock_payment_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Payment confirmed and receipt sent."}

def test_confirm_payment_invalid_email(mock_payment_data):
    mock_payment_data["user_email"] = "invalid-email"
    response = client.post("/confirm-payment/", json=mock_payment_data)
    assert response.status_code == 422  # Unprocessable Entity
```

### Instructions to Run

1. **Install Dependencies**: Make sure you have FastAPI, Uvicorn, FastAPI-Mail, and Pytest installed. You can install them using pip:

   ```bash
   pip install fastapi uvicorn fastapi-mail pytest
   ```

2. **Set Environment Variables**: Set the necessary environment variables for email configuration:

   ```bash
   export MAIL_USERNAME="your_email@example.com"
   export MAIL_PASSWORD="your_password"
   export MAIL_FROM="your_email@example.com"
   export MAIL_SERVER="smtp.example.com"
   ```

3. **Run the FastAPI Application**:

   ```bash
   uvicorn main:app --reload
   ```

4. **Run the Tests**:

   ```bash
   pytest test_main.py
   ```

This code provides a basic implementation of a payment confirmation feature with email notifications and includes unit tests to verify its functionality. Adjust the email configuration and payment processing logic as needed for your specific use case.