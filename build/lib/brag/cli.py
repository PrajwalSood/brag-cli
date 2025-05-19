import typer
from brag.doc_utils import init_brag_doc, add_entry, read_history
from brag.git_utils import sync_with_git, get_git_history
from brag.ollama_utils import summarize_brag_doc, generate_resume_bullets

app = typer.Typer(help="Brag CLI: Create and manage your brag document.")

@app.command()
def init():
    """Initialize a new brag doc."""
    created = init_brag_doc()
    if created:
        typer.echo("Brag doc initialized.")
    else:
        typer.echo("Brag doc already exists.")

@app.command()
def sync():
    """Sync brag doc with git."""
    try:
        sync_with_git()
        typer.echo("Brag doc synced with git.")
    except Exception as e:
        typer.echo(f"Git sync failed: {e}")

@app.command()
def add(message: str = typer.Argument(..., help="Message or achievement to add.")):
    """Add a new entry to the brag doc."""
    add_entry(message)
    typer.echo(f"Added entry: {message}")

@app.command()
def history():
    """View brag doc history."""
    lines = read_history()
    typer.echo("".join(lines))
    try:
        commits = get_git_history()
        typer.echo("\nGit History:")
        for commit in commits:
            typer.echo(f"- {commit.hexsha[:7]} {commit.summary} ({commit.committed_datetime})")
    except Exception:
        pass

@app.command()
def summarize():
    """Generate a summary using Ollama."""
    summary = summarize_brag_doc()
    typer.echo(summary)

@app.command()
def bullets():
    """Generate resume bullet points using Ollama."""
    bullets = generate_resume_bullets()
    typer.echo(bullets)

if __name__ == "__main__":
    app()
