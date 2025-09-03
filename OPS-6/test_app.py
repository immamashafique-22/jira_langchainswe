# Test cases
Sure! Here's an implementation of the payment confirmation feature based on the Jira ticket provided:

## Code Implementation:

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_payment_confirmation(recipient_email, amount, transaction_id):
    """
    Send a payment confirmation email to the user.

    :param recipient_email: Email address of the recipient.
    :param amount: Transaction amount.
    :param transaction_id: Unique transaction ID.
    """
    sender_email = "payments@example.com"
    sender_password = "your_email_password"  # Securely store this!

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Payment Confirmation"

    body = f"Dear Customer,\n\nThis is to confirm that your payment of {amount} has been successfully processed.\n" \
           f"Your transaction ID is: {transaction_id}\n\nThank you for your business.\n" \
           f"Regards,\nYour Company Name"

    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP("smtp.example.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        print("Payment confirmation email sent successfully.")
    except smtplib.SMTPException as e:
        print("Error sending email:", e)

# Example usage:
send_payment_confirmation("recipient@example.com", "100.00", "TXN12345")
```

## Unit Tests:

```python
import unittest
from unittest.mock import patch, MagicMock
from payment_confirmation import send_payment_confirmation  # Assuming the function is in a module named payment_confirmation

class TestPaymentConfirmation(unittest.TestCase):
    @patch("smtplib.SMTP")
    def test_send_payment_confirmation(self, mock_smtp):
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        send_payment_confirmation("recipient@example.com", "50.00", "TXN67890")

        mock_smtp.assert_called_with("smtp.example.com", 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with("payments@example.com", "your_email_password")
        mock_server.sendmail.assert_called_once_with("payments@example.com", "recipient@example.com", mock.ANY)

        expected_message = """From: payments@example.com
To: recipient@example.com
Subject: Payment Confirmation

Mime-Version: 1.0
Content-Type: text/plain

Dear Customer,

This is to confirm that your payment of 50.00 has been successfully processed.
Your transaction ID is: TXN67890

Thank you for your business.
Regards,
Your Company Name"""

        mock_server.sendmail.assert_called_with("payments@example.com", "recipient@example.com", expected_message)

    def test_email_content(self):
        recipient_email = "recipient@example.com"
        amount = "150.00"
        transaction_id = "