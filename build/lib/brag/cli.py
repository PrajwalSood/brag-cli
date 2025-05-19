import typer
from brag.doc_utils import init_brag_doc, add_entry, read_history, purge_entries_between
from brag.git_utils import sync_with_git, get_git_history
from brag.ollama_utils import summarize_brag_doc, generate_resume_bullets
from datetime import datetime, timedelta
import re

app = typer.Typer(help="Brag CLI: Create and manage your brag document.")

def parse_relative_time(relative: str) -> str:
    """
    Parse relative time like '1d', '2w', '1w5d', '1h5m', etc. and return the date string (YYYY-MM-DD).
    """
    now = datetime.now()
    days = 0
    hours = 0
    minutes = 0
    weeks = 0
    # Match patterns like 1w5d, 2d, 1h5m, etc.
    pattern = r"(?:(?P<w>\d+)w)?(?:(?P<d>\d+)d)?(?:(?P<h>\d+)h)?(?:(?P<m>\d+)m)?"
    match = re.fullmatch(pattern, relative)
    if not match:
        raise ValueError(f"Invalid relative time format: {relative}")
    if match.group("w"): weeks = int(match.group("w"))
    if match.group("d"): days = int(match.group("d"))
    if match.group("h"): hours = int(match.group("h"))
    if match.group("m"): minutes = int(match.group("m"))
    delta = timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes)
    target = now - delta
    return target.strftime("%Y-%m-%d")

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

@app.command()
def purge(
    start: str = typer.Option(None, help="Start date (YYYY-MM-DD) or relative (e.g., 2d, 1w5d, 1h5m)"),
    end: str = typer.Option(None, help="End date (YYYY-MM-DD) or relative (e.g., 1d, 1w)")
):
    """Purge brag doc entries between two dates or for a relative time period."""
    if not start and not end:
        typer.echo("Please provide at least one of --start or --end.")
        raise typer.Exit(1)
    now_str = datetime.now().strftime("%Y-%m-%d")
    if start:
        try:
            start_date = parse_relative_time(start) if not re.match(r"\d{4}-\d{2}-\d{2}", start) else start
        except Exception as e:
            typer.echo(f"Invalid start: {e}")
            raise typer.Exit(1)
    else:
        start_date = "1970-01-01"
    if end:
        try:
            end_date = parse_relative_time(end) if not re.match(r"\d{4}-\d{2}-\d{2}", end) else end
        except Exception as e:
            typer.echo(f"Invalid end: {e}")
            raise typer.Exit(1)
    else:
        end_date = now_str
    removed = purge_entries_between(start_date, end_date)
    typer.echo(f"Purged {removed} entries between {start_date} and {end_date}.")

if __name__ == "__main__":
    app()
