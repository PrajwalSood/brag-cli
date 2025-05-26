"""
Collection of prompts used by the Brag CLI for AI operations such as summarization and bullet point generation.
"""

# Ollama prompts
SUMMARIZE_BRAG_DOC_PROMPT = """
Summarize the following brag doc. Summarise each project in a single paragraph. Format of the file: - [Date] [Project Name] Brag):
{content}
"""

GENERATE_RESUME_BULLETS_PROMPT = """
Generate resume bullet points from the following brag doc. Summarise each project in one or two bullets. Format of the file: - [Date] [Project Name] Brag):
{content}
"""

# Profile-aware prompts
PROFILE_BASED_RESUME_PROMPT = """
Using the developer's profile information and brag document, generate a comprehensive resume that highlights their professional experience and achievements.

Developer Profile:
{profile}

Brag Document:
{content}

Format the resume to emphasize the skills, experience, and achievements most relevant to a {title} role.
"""

PROFILE_BASED_SUMMARY_PROMPT = """
Create a professional summary for {name} based on their profile information and brag document.

Developer Profile:
{profile}

Brag Document:
{content}

Create a concise and impactful 2-3 paragraph professional summary that highlights key strengths, experience, and achievements.
"""

PROFILE_GREETING = """
Welcome, {name}!
Your brag document is helping you track achievements as a {title}.
"""

# Additional prompt templates can be added here as needed 

