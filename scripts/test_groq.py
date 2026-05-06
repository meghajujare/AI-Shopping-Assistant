from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "llama-3.1-8b-instant"
)

print("USING MODEL:", MODEL_NAME)

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[
        {
            "role": "user",
            "content": "Say hello"
        }
    ],
    temperature=0
)

print("\nRESPONSE:\n")
print(response.choices[0].message.content)