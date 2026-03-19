import requests
import os
from dotenv import load_dotenv
from transformers import pipeline

load_dotenv()

# SARVAM API
SARVAM_URL = "https://api.sarvam.ai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {os.getenv('SARVAM_API_KEY')}",
    "Content-Type": "application/json"
}

# Local fallback
local_model = pipeline("text-generation", model="distilgpt2")

def query_llm(prompt):
    # --- TRY SARVAM FIRST ---
    try:
        payload = {
            "model": "sarvam-m",  # or latest available model
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(SARVAM_URL, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]

        print("Sarvam failed:", response.text)

    except Exception as e:
        print("Sarvam exception:", str(e))

    # --- FALLBACK ---
    result = local_model(prompt, max_length=100, num_return_sequences=1)
    return result[0]["generated_text"]