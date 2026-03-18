import requests
import os

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

headers = {
    "Authorization": f"Bearer {os.getenv('HF_API_KEY')}"
}

def query_llm(prompt):
    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": prompt}
    )

    if response.status_code != 200:
        return f"API Error: {response.text}"

    data = response.json()

    try:
        return data[0]["generated_text"]
    except:
        return str(data)