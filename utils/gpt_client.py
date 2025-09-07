import os
from openai import OpenAI
from dotenv import load_dotenv

import streamlit as st

# Get API key from Streamlit secrets
openai_api_key = st.secrets["openai"]["OPENAI_API_KEY"]

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



