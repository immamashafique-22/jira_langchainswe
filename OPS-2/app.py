Sure! Here is the expected output based on the provided Jira ticket:

## Code Implementation:

```python
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime

app = Flask(__name__)

# Placeholder user database (replace with an actual database)
users = {
    "user1": generate_password_hash("password1"),
    "user2": generate_password_hash("password2")
}

# Token settings
app.secret_key = 'your_secret_key'
token_duration = 3600  # Token duration in seconds (1 hour)

def generate_auth_token(user):
    serializer = Serializer(app.secret_key, expires_in=token_duration)
    return serializer.dumps({'username': user})

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users and check_password_hash(users[username], password):
        token = generate_auth_token(username)
        return jsonify({'token': token.decode('utf-8')}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/auth/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')

    if token:
        serializer = Serializer(app.secret_key)
        try:
            data = serializer.loads(token)
        except Exception as e:
            return jsonify({'error': 'Invalid or expired token'}), 401

        username = data.get('username')
        if username in users:
            return jsonify({'message': f'Welcome, {username}! This is a protected resource.'}), 200

    return jsonify({'error': 'Authentication required'}), 401

if __name__ == '__main__':
    app.run(debug=True)
```

## Unit Tests:

```python
import unittest
from flask import Flask, request, json
from werkzeug.test import Client

# Create a test client
app = Flask(__name__)
client = Client(app, Flask(__name__))

# Sample user data for testing
test_users = {
    "testuser1": "password1",
    "testuser2": "password2"
}

class AuthenticationTests(unittest.TestCase):
    def test_login(self):
        # Test successful login
        response = client.post('/api/auth/login', json={'username': 'testuser1', 'password': 'password1'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)

        # Test failed login
        response = client.post('/api/auth/login', json={'username': 'invaliduser', 'password': 'invalidpassword'})
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.json)

    def test_protected_resource(self):
        # Test access to protected resource with valid token
        response = client.post('/api/auth/login', json={'username': 'testuser2', 'password': 'password2'})
        token = response.json['token']
        headers = {'Authorization': token}
        response = client.get('/api/auth/protected', headers=headers)
        self.assertEqual(response.