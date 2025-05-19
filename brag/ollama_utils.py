import requests
import os

BRAG_DOC = "bragdoc.md"
OLLAMA_API_URL = os.environ.get("OLLAMA_API_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama2")

def summarize_brag_doc():
    with open(BRAG_DOC, "r") as f:
        content = f.read()
    prompt = "Summarize the following brag doc:\n" + content
    response = requests.post(OLLAMA_API_URL, json={"model": OLLAMA_MODEL, "prompt": prompt})
    return response.json().get("response", "No summary generated.")

def generate_resume_bullets():
    with open(BRAG_DOC, "r") as f:
        content = f.read()
    prompt = "Generate resume bullet points from the following brag doc:\n" + content
    response = requests.post(OLLAMA_API_URL, json={"model": OLLAMA_MODEL, "prompt": prompt})
    return response.json().get("response", "No bullet points generated.")
