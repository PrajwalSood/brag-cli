import requests
import json
from pydantic import BaseModel
from brag.doc_utils import get_brag_doc_path
from brag.constants import OLLAMA_API_URL, OLLAMA_MODEL
from brag.prompts import (
    SUMMARIZE_BRAG_DOC_PROMPT, 
    GENERATE_RESUME_BULLETS_PROMPT,
    PROFILE_BASED_RESUME_PROMPT,
    PROFILE_BASED_SUMMARY_PROMPT
)
from brag.profile import get_profile

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

def generate_profile_based_resume() -> str:
    """Generate a resume using both profile information and brag document."""
    profile = get_profile()
    profile_json = json.dumps(profile, indent=2)
    
    brag_doc = get_brag_doc_path()
    with open(brag_doc, "r") as f:
        content = f.read()
    
    title = profile.get("title", "Developer")
    prompt = PROFILE_BASED_RESUME_PROMPT.format(
        profile=profile_json,
        content=content,
        title=title
    )
    
    response = requests.post(OLLAMA_API_URL, json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False})
    data = response.json()
    return OllamaResponse(**data).response if "response" in data else "No resume generated."

def generate_profile_based_summary() -> str:
    """Generate a professional summary using both profile information and brag document."""
    profile = get_profile()
    profile_json = json.dumps(profile, indent=2)
    
    brag_doc = get_brag_doc_path()
    with open(brag_doc, "r") as f:
        content = f.read()
    
    name = profile.get("name", "Developer")
    prompt = PROFILE_BASED_SUMMARY_PROMPT.format(
        profile=profile_json,
        content=content,
        name=name
    )
    
    response = requests.post(OLLAMA_API_URL, json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False})
    data = response.json()
    return OllamaResponse(**data).response if "response" in data else "No professional summary generated."
