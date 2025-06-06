import typer
from brag.doc_utils import init_brag_doc, add_entry, read_history, purge_entries_between
from brag.git_utils import sync_with_git, get_git_history
from brag.ollama_utils import (
    summarize_brag_doc, generate_resume_bullets,
    generate_profile_based_resume, generate_profile_based_summary
)
from datetime import datetime, timedelta
import re
from brag.category_utils import (
    extract_categories_from_history, find_closest_category,
    set_current_category, get_current_category, unset_current_category, change_current_category,
    list_categories, select_category_by_index
)
from brag.profile import (
    init_profile, get_profile, update_profile_field,
    add_list_item, remove_list_item
)
from brag.constants import PROFILE_FIELDS
from brag.prompts import PROFILE_GREETING
import json

app = typer.Typer(help="Brag CLI: Create and manage your brag document.")
category_app = typer.Typer(help="Manage current brag category.")
profile_app = typer.Typer(help="Manage your developer profile.")
app.add_typer(category_app, name="category")
app.add_typer(profile_app, name="profile")

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

@category_app.command("set")
def set_category(category: str):
    """Set the current category for new brags."""
    set_current_category(category)
    typer.echo(f"Current category set to: {category}")

@category_app.command("unset")
def unset_category():
    """Unset the current category."""
    unset_current_category()
    typer.echo("Current category unset.")

@category_app.command("change")
def change_category(new_category: str):
    """Change the current category."""
    change_current_category(new_category)
    typer.echo(f"Current category changed to: {new_category}")

@category_app.command("show")
def show_category():
    """Show the current category."""
    category = get_current_category()
    if category:
        typer.echo(f"Current category: {category}")
    else:
        typer.echo("No current category set.")

@category_app.command("list")
def list_all_categories():
    """List all unique categories from brag history with their indices."""
    history = read_history()
    categories = list_categories(history)
    if not categories:
        typer.echo("No categories found.")
        return
    for idx, cat in enumerate(categories):
        typer.echo(f"{idx}: {cat}")

@category_app.command("select")
def select_category(index: int):
    """Select a category by its index from the list and set it as current."""
    history = read_history()
    try:
        category = select_category_by_index(history, index)
        set_current_category(category)
        typer.echo(f"Current category set to: {category}")
    except (ValueError, IndexError) as e:
        typer.echo(str(e))

@profile_app.command("init")
def initialize_profile():
    """Initialize a new developer profile."""
    created = init_profile()
    if created:
        typer.echo("Developer profile initialized.")
    else:
        typer.echo("Developer profile already exists.")

@profile_app.command("show")
def show_profile():
    """Show your developer profile."""
    profile = get_profile()
    typer.echo(json.dumps(profile, indent=2))

@profile_app.command("update")
def update_profile(
    field: str = typer.Option(..., help=f"Field to update. Available fields: {', '.join(PROFILE_FIELDS)}"),
    value: str = typer.Option(..., help="New value for the field")
):
    """Update a field in your developer profile."""
    update_profile_field(field, value)
    typer.echo(f"Updated {field} to: {value}")

@profile_app.command("add-item")
def add_to_list(
    field: str = typer.Option(..., help="List field to add to (skills, experience, education)"),
    item: str = typer.Option(..., help="Item to add to the list")
):
    """Add an item to a list field in your profile."""
    add_list_item(field, item)
    typer.echo(f"Added '{item}' to {field}")

@profile_app.command("remove-item")
def remove_from_list(
    field: str = typer.Option(..., help="List field to remove from (skills, experience, education)"),
    index: int = typer.Option(..., help="Index of the item to remove")
):
    """Remove an item from a list field by index."""
    removed = remove_list_item(field, index)
    if removed:
        typer.echo(f"Removed '{removed}' from {field}")
    else:
        typer.echo(f"No item found at index {index} in {field}")

@profile_app.command("generate-resume")
def profile_resume():
    """Generate a comprehensive resume using your profile and brag document."""
    resume = generate_profile_based_resume()
    typer.echo(resume)

@profile_app.command("generate-summary")
def profile_summary():
    """Generate a professional summary using your profile and brag document."""
    summary = generate_profile_based_summary()
    typer.echo(summary)

@app.command()
def add(
    message: str = typer.Argument(..., help="Message or achievement to add.")
):
    """Add a new entry to the brag doc. Uses the current category if set, else auto-categorises."""
    # Display personalized greeting if profile exists
    try:
        profile = get_profile()
        if profile["name"] and profile["title"]:
            typer.echo(PROFILE_GREETING.format(name=profile["name"], title=profile["title"]))
    except:
        pass
        
    assigned_category = get_current_category()
    if not assigned_category:
        history = read_history()
        assigned_category = find_closest_category(message, history)
        if assigned_category:
            typer.echo(f"No category set. Assigned to existing category by similarity: '{assigned_category}'")
        else:
            typer.echo("No category set. No category found by similarity.")
    add_entry(message, assigned_category)
    if assigned_category:
        typer.echo(f"Added entry: [{assigned_category}] {message}")
    else:
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
