from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def rewrite_query(question, chat_history):

    history = ""

    for message in chat_history:
        role = message["role"].capitalize()
        history += f"{role}: {message['content']}\n"

    prompt = f"""
Rewrite the user's latest question into a complete, standalone question.

Rules:
- Use the conversation history to replace pronouns like:
  he, she, it, they, his, her, this, that.
- Do not answer the question.
- Only rewrite it.
- If the question is already complete, return it unchanged.

Conversation History:
{history}

Current Question:
{question}

Rewritten Question:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()