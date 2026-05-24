from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_reply(email_body, tone="formal"):
    prompt = f"""
    You are an intelligent AI email assistant.

    Generate a {tone} professional email reply.

    Rules:
    - Keep response concise
    - Be polite and professional
    - Write clear business communication
    - Do not make up fake information

    Original Email:
    {email_body}

    Reply:
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
