from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def ask_llm(question, context, chat_history):
    history = ""

    for message in chat_history:
        role = message["role"].capitalize()
        history += f"{role}: {message['content']}\n"

    prompt = f"""
You are an intelligent PDF assistant.

Your job is to answer questions using BOTH:

1. The conversation history
2. The retrieved document context

Rules:

- Use the conversation history to understand follow-up questions such as:
  "he", "she", "it", "they", "his", "her", "that", "this".
- Use the document context as the source of facts.
- Never invent information that is not supported by the document.
- If the answer cannot be found in the document context, reply:
  "I couldn't find the answer in the document."
- If information comes from multiple chunks, combine it into one clear answer.
- Answer naturally and clearly.

-----------------------
Conversation History:

{history}

-----------------------
Document Context:

{context}

-----------------------
Current Question:

{question}

Answer:
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

    return response.choices[0].message.content