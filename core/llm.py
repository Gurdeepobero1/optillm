import requests

SARVAM_URL = "https://api.sarvam.ai/v1/chat/completions"

def query_llm(prompt, api_key):
    if not api_key:
        return "❌ Missing API Key"

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "sarvam-m",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0  # 🔥 prevents hallucination
        }

        response = requests.post(SARVAM_URL, headers=headers, json=payload)

        if response.status_code != 200:
            return f"❌ API Error: {response.text}"

        data = response.json()

        # safe extraction
        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"]

        return "❌ Invalid API response"

    except Exception as e:
        return f"❌ Exception: {str(e)}"