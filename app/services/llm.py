import requests
from config.settings import OLLAMA_URL, MODEL_NAME

def generate_response(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options":{
                "temperature": 0.2
            }
        }
    )
    return response.json().get("response", "")