Certainly! Below is a complete FastAPI application that implements a password recovery feature, along with unit tests using Pytest.

### FastAPI Application Code

```python
# main.py
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid
import smtplib
from email.mime.text import MIMEText

app = FastAPI()

# In-memory storage for demonstration purposes
users_db = {
    "user@example.com": {
        "username": "user",
        "password": "hashed_password",  # This should be hashed in a real application
        "reset_token": None
    }
}

class PasswordRecoveryRequest(BaseModel):
    email: EmailStr

def send_email(to_email: str, reset_link: str):
    # Configure your SMTP server settings
    smtp_server = "smtp.example.com"
    smtp_port = 587
    smtp_user = "your_email@example.com"
    smtp_password = "your_password"

    msg = MIMEText(f"Click the link to reset your password: {reset_link}")
    msg['Subject'] = 'Password Reset Request'
    msg['From'] = smtp_user
    msg['To'] = to_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, to_email, msg.as_string())

@app.post("/password-recovery/")
async def password_recovery(request: PasswordRecoveryRequest, background_tasks: BackgroundTasks):
    user = users_db.get(request.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate a reset token
    reset_token = str(uuid.uuid4())
    user['reset_token'] = reset_token

    # Create a reset link (this should be a real URL in production)
    reset_link = f"http://localhost:8000/reset-password/{reset_token}"

    # Send email in the background
    background_tasks.add_task(send_email, request.email, reset_link)

    return JSONResponse(content={"message": "Password reset link sent"}, status_code=200)

@app.get("/reset-password/{token}")
async def reset_password(token: str):
    for user in users_db.values():
        if user['reset_token'] == token:
            return JSONResponse(content={"message": "Token is valid"}, status_code=200}
    raise HTTPException(status_code=400, detail="Invalid or expired token")
```

### Unit Tests with Pytest

```python
# test_main.py
import pytest
from fastapi.testclient import TestClient
from main import app, users_db

client = TestClient(app)

@pytest.fixture
def setup_user():
    # Setup a user for testing
    users_db["testuser@example.com"] = {
        "username": "testuser",
        "password": "hashed_password",
        "reset_token": None
    }
    yield
    # Teardown
    del users_db["testuser@example.com"]

def test_password_recovery_success(setup_user):
    response = client.post("/password-recovery/", json={"email": "testuser@example.com"})
    assert response.status_code == 200
    assert response.json() == {"message": "Password reset link sent"}

def test_password_recovery_user_not_found():
    response = client.post("/password-recovery/", json={"email": "nonexistent@example.com"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_reset_password_valid_token(setup_user):
    # First, request a password recovery to generate a token
    response = client.post("/password-recovery/", json={"email": "testuser@example.com"})
    assert response.status_code == 200

    # Now, extract the token from the user's data
    token = users_db["testuser@example.com"]["reset_token"]

    response = client.get(f"/reset-password/{token}")
    assert response.status_code == 200
    assert response.json() == {"message": "Token is valid"}

def test_reset_password_invalid_token():
    response = client.get("/reset-password/invalid_token")
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid or expired token"}
```

### Instructions to Run

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
   uvicorn main:app --reload
   ```

4. **Run the Tests**:
   ```bash
   pytest test_main.py
   ```

### Notes
- The email sending functionality is a placeholder. You need to configure your SMTP server settings.
- The password should be hashed in a real application. Use libraries like `bcrypt` or `passlib` for hashing.
- The in-memory database (`users_db`) is for demonstration purposes. In a production application, you would use a proper database.