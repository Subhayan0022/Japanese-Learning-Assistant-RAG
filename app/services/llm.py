import requests
from config.settings import OLLAMA_URL, MODEL_NAME, TEMPERATURE


def generate_response(prompt, temperature=TEMPERATURE):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature
                }
            },
            timeout=30
        )
        return response.json().get("response", "")
    except requests.ConnectionError:
        return "Error: Cannot connect to LLM. Make sure it is running."
    except requests.Timeout:
        return "Error: LLM took too long to respond."
