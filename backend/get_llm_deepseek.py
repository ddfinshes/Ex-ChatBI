import requests

def LLM(prompt, model="deepseek-r1:7b"):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False}
    )
    return response.json()["response"]

# print(LLM("你是谁？"))