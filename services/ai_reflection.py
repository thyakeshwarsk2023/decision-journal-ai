import requests
import os
from dotenv import load_dotenv
OLLAMA_URL = os.getenv("OLLAMA_URL")
MODEL_NAME = os.getenv("OLLAMA_MODEL")

def generate_ai_reflection(
    decision_text: str,
    reflections: list[str]
):

    reflection_text = "\n".join(reflections)

    prompt = f"""
You are an expert in psychology and decision-making.

Decision:
{decision_text}

User Reflections:
{reflection_text}

Provide:

1. Short summary
2. Possible cognitive biases
3. Alternative viewpoints
4. Two questions for future reflection

Keep the response concise.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]