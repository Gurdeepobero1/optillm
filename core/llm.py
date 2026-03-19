import requests

SARVAM_URL = "https://api.sarvam.ai/v1/chat/completions"

def query_llm(prompt, api_key):
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "sarvam-m",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(SARVAM_URL, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]

        return f"API Error: {response.text}"

    except Exception as e:
        return f"Exception: {str(e)}"