import requests
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generar_prompt(texto):
    if not GEMINI_API_KEY:
        return {"error": "API key no configurada"}

    prompt = f"Clasifica el tipo de documento con base en el siguiente texto:\n\n{texto[:3000]} y entregame un array con los valores que puedas extraer"

    response = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
        params={"key": GEMINI_API_KEY},
        json={
            "contents": [{"parts": [{"text": prompt}]}]
        },
    )

    if response.status_code != 200:
        return {"error": response.text}

    result = response.json()
    return result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", result)