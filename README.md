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
