from asyncio import timeout

import requests
from config.settings import OLLAMA_URL, MODEL_NAME

def generate_response(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options":{
                    "temperature": 0.2
                }
            },
            timeout = 30
        )
        return response.json().get("response", "")
    except requests.ConnectionError:
        return "Error: Cannot connect to LLM. Make sure it is running."
    except requests.Timeout:
        return "Error: LLM took too long to respond."