from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText


def get_gmail_service(credentials):
    return build("gmail", "v1", credentials=credentials)


def fetch_unread_emails(service):
    results = service.users().messages().list(
        userId="me",
        labelIds=["UNREAD"]
    ).execute()

    return results.get("messages", [])

def send_email(service, to, subject, body):
    message = MIMEText(body)

    message["to"] = to
    message["subject"] = subject

    raw = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    return service.users().messages().send(
        userId="me",
        body={"raw": raw}
    ).execute()
