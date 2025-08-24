import os
from typing import List, Dict
from dotenv import load_dotenv

try:
    from openai import OpenAI
except Exception:
    OpenAI = None  # Allows running without the package during tests

load_dotenv()

SYSTEM_PROMPT = (    "You are a helpful *financial information assistant*. You are not a "    "financial advisor and you cannot provide legal or tax advice. Help the "    "user analyze budgets and transactions and explain scenarios in plain language.")

def chat(messages: List[Dict[str, str]]) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or OpenAI is None:
        return "AI bot is not configured. Add OPENAI_API_KEY to your .env to enable chat."
    client = OpenAI(api_key=api_key)
    # Keep first system message
    msgs = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=msgs,
        temperature=0.3,
    )
    return resp.choices[0].message.content
