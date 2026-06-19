from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText
import re
def parse_email_data(message):

    headers = message["payload"]["headers"]

    subject = ""
    sender = ""

    for header in headers:

        if header["name"] == "Subject":
            subject = header["value"]

        if header["name"] == "From":
            sender = header["value"]

    body = ""

    parts = message["payload"].get("parts")

    if parts:

        for part in parts:

            if part["mimeType"] == "text/plain":

                data = part["body"].get("data")

                if data:

                    body = base64.urlsafe_b64decode(
                        data
                    ).decode("utf-8")

    return {
        "sender": sender,
        "subject": subject,
        "body": body
    }
def get_gmail_service(credentials):
    return build("gmail", "v1", credentials=credentials)



def fetch_unread_emails(service):
    results = service.users().messages().list(
        userId="me",
        labelIds=["UNREAD"]
    ).execute()

    return results.get("messages", [])

def get_email_detail(service, msg_id):

    message = service.users().messages().get(
        userId="me",
        id=msg_id
    ).execute()

    return message

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

def extract_email(from_header):
    match = re.search(r"<(.+?)>", from_header)

    if match:
        return match.group(1)

    return from_header