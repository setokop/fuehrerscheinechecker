import requests
from bs4 import BeautifulSoup
import hashlib
import smtplib
from email.mime.text import MIMEText

# URL to check
url = "https://example.com"  # Replace with the URL you want to monitor

# Hash file to store previous content
hash_file = "previous_content_hash.txt"

# Email configuration
smtp_host = "smtp.gmail.com"  # Replace with your email provider's SMTP server
smtp_port = 587
sender_email = "your_email@example.com"  # Replace with your email address
receiver_email = "recipient@example.com"  # Replace with the recipient's email address
email_password = "your_email_password"  # Replace with your email password

# Fetch and compare content
response = requests.get(url)
new_content = response.text
new_content_hash = hashlib.md5(new_content.encode()).hexdigest()

try:
    with open(hash_file, "r") as file:
        old_content_hash = file.read()
except FileNotFoundError:
    old_content_hash = ""

if old_content_hash != new_content_hash:
    # Content has changed
    with open(hash_file, "w") as file:
        file.write(new_content_hash)
    subject = "Content Change Alert"
    message = f"The content of {url} has changed.\n\nVisit the URL: {url}"
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(sender_email, email_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
