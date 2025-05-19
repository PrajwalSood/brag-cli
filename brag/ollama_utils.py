import requests
import os
from pydantic import BaseModel
from brag.doc_utils import get_brag_doc_path

OLLAMA_API_URL = os.environ.get("OLLAMA_API_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")

class OllamaResponse(BaseModel):
    response: str

def summarize_brag_doc() -> str:
    brag_doc = get_brag_doc_path()
    with open(brag_doc, "r") as f:
        content = f.read()
    prompt = "Summarize the following brag doc:\n" + content
    response = requests.post(OLLAMA_API_URL, json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False})
    data = response.json()
    return OllamaResponse(**data).response if "response" in data else "No summary generated."

def generate_resume_bullets() -> str:
    brag_doc = get_brag_doc_path()
    with open(brag_doc, "r") as f:
        content = f.read()
    prompt = "Generate resume bullet points from the following brag doc:\n" + content
    response = requests.post(OLLAMA_API_URL, json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False})
    data = response.json()
    return OllamaResponse(**data).response if "response" in data else "No bullet points generated."
