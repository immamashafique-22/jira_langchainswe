# Test cases
Here is the code implementation, unit tests, and a short README for the Jira ticket with ID OPS-6:

## Code Implementation:

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formatdate

def send_payment_confirmation(recipient_email, amount, transaction_id):
    # Configure email settings
    sender_email = "payments@example.com"
    sender_password = "your_password"
    smtp_server = "smtp.example.com"
    smtp_port = 587

    # Create the email content
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Date"] = formatdate(localtime=True)
    msg["Subject"] = "Payment Confirmation"

    # Attach the payment receipt as a PDF
    with open("receipt.pdf", "rb") as file:
        attachment = MIMEApplication(file.read(), _subtype="pdf")
        attachment.add_header("Content-Disposition", "attachment", filename="receipt.pdf")
    msg.attach(attachment)

    # Add the email body
    message_text = f"Dear Customer,\n\nThis is to confirm that your payment of {amount} has been successfully received. Your transaction ID is {transaction_id}.\n\nRegards,\nYour Company Name"
    msg.attach(MIMEText(message_text, "plain"))

    # Connect to the SMTP server and send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Payment confirmation email sent successfully.")
    except smtplib.SMTPException as e:
        print("Error sending email:", e)

# Example usage
send_payment_confirmation("recipient@example.com", "100.00", "TRANS12345")
```

## Unit Tests:

```python
import unittest
from unittest.mock import patch, call
from payment_confirmation import send_payment_confirmation  # assuming the code is in a module named payment_confirmation

class PaymentConfirmationTests(unittest.TestCase):
    @patch("smtplib.SMTP")
    def test_send_payment_confirmation(self, mock_smtp):
        send_payment_confirmation("recipient@example.com", "100.00", "TRANS12345")

        mock_smtp.return_value.starttls.assert_called_once()
        mock_smtp.return_value.login.assert_called_once_with("payments@example.com", "your_password")
        mock_smtp.return_value.sendmail.assert_called_once_with(
            "payments@example.com",
            "recipient@example.com",
            mock.ANY
        )
        self.assertEqual(mock_smtp.mock_calls, [
            call().__enter__(),
            call().starttls(),
            call().login("payments@example.com", "your_password"),
            call().sendmail("payments@example.com", "recipient@example.com", mock.ANY),
            call().__exit__(None, None, None)
        ])

    def test_email_content(self):
        with patch("smtplib.SMTP") as mock_smtp:
            send_payment_confirmation("recipient@example.com",