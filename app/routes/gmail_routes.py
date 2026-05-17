from fastapi import APIRouter

router = APIRouter()

@router.get("/emails")
def get_emails():

    sample_emails = [
        {
            "sender": "hr@company.com",
            "subject": "Interview Invitation"
        },
        {
            "sender": "manager@office.com",
            "subject": "Project Update Needed"
        }
    ]

    return {
        "emails": sample_emails
    }