from fastapi import APIRouter
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(override=True)
print("ENV KEY =", os.getenv("OPENAI_API_KEY"))
router = APIRouter()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


@router.post("/generate")
def generate_reply():
    email_content = """
    Hello,

    We would like to schedule your interview for next week.

    Please let us know your availability.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an email assistant."
            },
            {
                "role": "user",
                "content": f"Generate professional reply for this email: {email_content}"
            }
        ]
    )

    draft = response.choices[0].message.content

    return {
        "generated_reply": draft
    }