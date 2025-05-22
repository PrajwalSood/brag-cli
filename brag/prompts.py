"""
Collection of prompts used by the Brag CLI for AI operations such as summarization and bullet point generation.
"""

# Ollama prompts
SUMMARIZE_BRAG_DOC_PROMPT = """
Summarize the following brag doc. Summarise each project in a single paragraph. Format of the file: - [Date] [Project Name] Brag):
{content}
"""

GENERATE_RESUME_BULLETS_PROMPT = """
Generate resume bullet points from the following brag doc. Summarise each project in one or two bullets . Format of the file: - [Date] [Project Name] Brag):
{content}
"""

# Additional prompt templates can be added here as needed 

