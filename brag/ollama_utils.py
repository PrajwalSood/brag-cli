import requests
from pydantic import BaseModel
from brag.doc_utils import get_brag_doc_path
from brag.constants import OLLAMA_API_URL, OLLAMA_MODEL
from brag.prompts import SUMMARIZE_BRAG_DOC_PROMPT, GENERATE_RESUME_BULLETS_PROMPT

class OllamaResponse(BaseModel):
    response: str

def summarize_brag_doc() -> str:
    brag_doc = get_brag_doc_path()
    with open(brag_doc, "r") as f:
        content = f.read()
    prompt = SUMMARIZE_BRAG_DOC_PROMPT.format(content=content)
    response = requests.post(OLLAMA_API_URL, json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False})
    data = response.json()
    return OllamaResponse(**data).response if "response" in data else "No summary generated."

def generate_resume_bullets() -> str:
    brag_doc = get_brag_doc_path()
    with open(brag_doc, "r") as f:
        content = f.read()
    prompt = GENERATE_RESUME_BULLETS_PROMPT.format(content=content)
    response = requests.post(OLLAMA_API_URL, json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False})
    data = response.json()
    return OllamaResponse(**data).response if "response" in data else "No bullet points generated."
