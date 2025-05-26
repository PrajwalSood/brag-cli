# Brag CLI

A command-line utility to help you create and manage a brag document, sync with git, view history, and generate summaries and resume bullet points using Ollama.

## Features
- Initialize a brag doc
- Sync with git
- Add commits to the doc
- View history
- Connect with Ollama for summaries and resume bullets

## Installation

You can install the CLI globally (after publishing to PyPI) with:
```bash
pip install brag-cli
```

Or locally from source:
```bash
pip install .
```

## Usage

After installation, use the CLI with:
```bash
brag [COMMAND]
```

For help:
```bash
brag --help
```

---

## Usage Guide: Real-World Example (Creating This Project)

Let's walk through using brag-cli to document the creation of this very project!

### 1. Initialize Your Brag Doc
```bash
brag init
```
Output:
```
Brag doc initialized.
```

### 2. Add Achievements as You Work
As you complete milestones, add them to your brag doc:
```bash
brag add "Set up project structure and virtual environment."
brag add "Implemented CLI skeleton with Typer."
brag add "Added git sync and history features."
brag add "Integrated Ollama for summaries and resume bullets."
brag add "Wrote and passed all automated tests."
brag add "Packaged and prepared project for PyPI publication."
```

### 2.1. Categorise Your Brags (Updated!)
You can now set a category context for your brags:
```bash
brag category set "Machine Learning"
brag add "Built a new ML model"
```
This will add the brag under the 'Machine Learning' category. To unset the category:
```bash
brag category unset
```
If you do not set a category, brag-cli will try to auto-categorise your brag based on previous topics using string similarity. If a close match is found, it will assign your brag to that category and inform you:
```bash
brag add "Created a website"
# Output: No category set. Assigned to existing category by similarity: 'Web Development'
#         Added entry: [Web Development] Created a website
```
If no similar category is found, the brag will be added without a category.

### 2.2. Managing Categories
You can manage your current category context with:
- `brag category set <category>`: Set the current category for new brags
- `brag category unset`: Unset the current category
- `brag category change <new_category>`: Change the current category
- `brag category show`: Show the current category
- `brag category list`: List all unique categories from your brag history with their indices
- `brag category select <index>`: Select a category by its index from the list and set it as current

**Example:**
```bash
brag category list
# Output:
# 0: Machine Learning
# 1: Web Development
# 2: DevOps

brag category select 1
# Output:
# Current category set to: Web Development
```

### 2.3. Managing Your Developer Profile

You can now maintain a developer profile with your personal and professional details:

- `brag profile init`: Initialize a new developer profile
- `brag profile show`: Show your developer profile
- `brag profile update --field <field> --value <value>`: Update a field in your profile
- `brag profile add-item --field <field> --item <item>`: Add an item to a list field
- `brag profile remove-item --field <field> --index <index>`: Remove an item from a list field

Available profile fields:
- Basic fields: name, title, summary
- Contact fields: contact.email, contact.phone, contact.linkedin, contact.github
- List fields: skills, experience, education

**Example:**
```bash
# Initialize your profile
brag profile init

# Update your name and title
brag profile update --field name --value "Jane Smith"
brag profile update --field title --value "Senior Software Engineer"

# Add skills
brag profile add-item --field skills --item "Python"
brag profile add-item --field skills --item "TypeScript"

# Generate personalized content
brag profile generate-resume
brag profile generate-summary
```

When you add entries to your brag doc with your profile set up, you'll receive a personalized greeting:
```bash
brag add "Completed API integration"
# Output:
# Welcome, Jane Smith!
# Your brag document is helping you track achievements as a Senior Software Engineer.
# Added entry: Completed API integration
```

### 3. View Your Brag Doc and History
See your brag doc and git history:
```bash
brag history
```
Output (example):
```
# Brag Doc

- [2024-06-10 10:00:00] Set up project structure and virtual environment.
- [2024-06-10 10:15:00] Implemented CLI skeleton with Typer.
- [2024-06-10 10:30:00] Added git sync and history features.
- [2024-06-10 11:00:00] Integrated Ollama for summaries and resume bullets.
- [2024-06-10 11:30:00] Wrote and passed all automated tests.
- [2024-06-10 12:00:00] Packaged and prepared project for PyPI publication.

Git History:
- 1a2b3c4 Initial commit (2024-06-10 09:55:00)
- 2b3c4d5 Add CLI skeleton (2024-06-10 10:16:00)
...
```

### 4. Sync Your Brag Doc with Git
```bash
brag sync
```
Output:
```
Brag doc synced with git.
```

### 5. Generate a Summary or Resume Bullets (with Ollama)
```bash
brag summarize
```
Output (example):
```
Summary: Developed and published a Python CLI tool to help users create, manage, and summarize brag documents, with git and AI integration.
```

```bash
brag bullets
```
Output (example):
```
- Designed and implemented a Python CLI for brag documentation
- Automated git sync and history tracking
- Integrated AI for summarization and resume bullet generation
- Published and documented the tool for public use
```

### 6. Generate Profile-Based Content
With your profile set up, you can generate enhanced content that combines your profile information with your brag document:

```bash
brag profile generate-resume
```
Output (example):
```
JANE SMITH
Senior Software Engineer
jane.smith@example.com | github.com/janesmith | linkedin.com/in/janesmith

SUMMARY
Accomplished Senior Software Engineer with expertise in Python, TypeScript, and cloud architecture. Proven track record of building scalable applications and leading technical initiatives.

EXPERIENCE
...
```

```bash
brag profile generate-summary
```
Output (example):
```
Jane Smith is a dedicated Senior Software Engineer with over 8 years of experience building robust, scalable software solutions. Her recent achievements include successfully implementing API integrations, leading development teams, and optimizing performance for mission-critical applications.

With expertise in Python, TypeScript, and cloud architectures, Jane consistently delivers high-quality software that meets business objectives while maintaining clean, maintainable code. Her ability to communicate complex technical concepts to stakeholders makes her an effective team leader and collaborator.
```

## Streamlit Web Application

The project also includes a Streamlit web application for a graphical interface to manage your brag document and profile:

```bash
streamlit run streamlit_app.py
```

The web application provides:
- Brag document initialization and management
- Profile initialization and management
- Content generation with Ollama
- Git synchronization

---

## Setup for Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the CLI:
   ```bash
   python3 -m brag.cli [COMMAND]
   ```

## Running Tests

Tests are located in the `tests/` directory. To run all tests:
```bash
pytest
```
