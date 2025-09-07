import os
from openai import OpenAI
from dotenv import load_dotenv

# Path to key1.env (same folder as gpt_client.py)
ENV_PATH = os.path.join(os.path.dirname(__file__), "key1.env")

# Load env file
load_dotenv(ENV_PATH)

# Get API key
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError(f"OPENAI_API_KEY not found in {ENV_PATH}")

client = OpenAI(api_key=openai_api_key)

def call_gpt4(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()

