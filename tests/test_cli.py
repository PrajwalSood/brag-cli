import os
import pytest
from typer.testing import CliRunner
from brag.cli import app
from datetime import datetime, timedelta

runner = CliRunner()

@pytest.fixture(autouse=True)
def cleanup_bragdoc():
    # Remove bragdoc.md before and after each test
    yield
    if os.path.exists("bragdoc.md"):
        os.remove("bragdoc.md")

def test_init_creates_bragdoc():
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["init"])
        assert "Brag doc initialized." in result.output
        assert os.path.exists("bragdoc.md")

def test_init_when_exists():
    with runner.isolated_filesystem():
        open("bragdoc.md", "w").close()
        result = runner.invoke(app, ["init"])
        assert "Brag doc already exists." in result.output

def test_add_entry():
    with runner.isolated_filesystem():
        runner.invoke(app, ["init"])
        result = runner.invoke(app, ["add", "Did something great!"])
        assert "Added entry: Did something great!" in result.output
        with open("bragdoc.md") as f:
            content = f.read()
        assert "Did something great!" in content

def test_history_shows_entries():
    with runner.isolated_filesystem():
        runner.invoke(app, ["init"])
        runner.invoke(app, ["add", "Achievement 1"])
        result = runner.invoke(app, ["history"])
        assert "Achievement 1" in result.output

def test_sync_with_git(monkeypatch):
    with runner.isolated_filesystem():
        runner.invoke(app, ["init"])
        monkeypatch.setattr("brag.cli.sync_with_git", lambda: None)
        result = runner.invoke(app, ["sync"])
        assert "Brag doc synced with git." in result.output

def test_sync_with_git_error(monkeypatch):
    with runner.isolated_filesystem():
        runner.invoke(app, ["init"])
        monkeypatch.setattr("brag.cli.sync_with_git", lambda: (_ for _ in ()).throw(Exception("fail")))
        result = runner.invoke(app, ["sync"])
        assert "Git sync failed: fail" in result.output

def test_summarize(monkeypatch):
    with runner.isolated_filesystem():
        runner.invoke(app, ["init"])
        monkeypatch.setattr("brag.cli.summarize_brag_doc", lambda: "Summary here.")
        result = runner.invoke(app, ["summarize"])
        assert "Summary here." in result.output

def test_bullets(monkeypatch):
    with runner.isolated_filesystem():
        runner.invoke(app, ["init"])
        monkeypatch.setattr("brag.cli.generate_resume_bullets", lambda: "Bullet 1\nBullet 2")
        result = runner.invoke(app, ["bullets"])
        assert "Bullet 1" in result.output
        assert "Bullet 2" in result.output

def test_purge_by_date():
    with runner.isolated_filesystem():
        runner.invoke(app, ["init"])
        import brag.doc_utils as doc_utils
        # Write three entries with different dates
        dates = [
            (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S"),
            (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]
        messages = ["Entry 1", "Entry 2", "Entry 3"]
        with open("bragdoc.md", "a") as f:
            for ts, msg in zip(dates, messages):
                entry = doc_utils.BragEntry(timestamp=ts, message=msg)
                f.write(f"- [{entry.timestamp}] {entry.message}\n")
        # Purge only the second entry (yesterday)
        purge_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        result = runner.invoke(app, ["purge", "--start", purge_date, "--end", purge_date])
        assert "Purged 1 entries" in result.output
        with open("bragdoc.md") as f:
            content = f.read()
        assert "Entry 2" not in content
        assert "Entry 1" in content
        assert "Entry 3" in content

def test_purge_by_relative(monkeypatch):
    with runner.isolated_filesystem():
        runner.invoke(app, ["init"])
        # Add an entry 2 days ago
        import brag.doc_utils as doc_utils
        old_date = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")
        entry = doc_utils.BragEntry(timestamp=old_date, message="Old Entry")
        with open("bragdoc.md", "a") as f:
            f.write(f"- [{entry.timestamp}] {entry.message}\n")
        # Add a recent entry
        runner.invoke(app, ["add", "Recent Entry"])
        # Purge last 1d (should only remove the recent entry)
        result = runner.invoke(app, ["purge", "--start", "1d"])
        assert "Purged 1 entries" in result.output
        with open("bragdoc.md") as f:
            content = f.read()
        assert "Recent Entry" not in content
        assert "Old Entry" in content

def test_add_with_category_set():
    with runner.isolated_filesystem():
        runner.invoke(app, ["init"])
        runner.invoke(app, ["category", "set", "Machine Learning"])
        result = runner.invoke(app, ["add", "Did something in ML"])
        assert "Added entry: [Machine Learning] Did something in ML" in result.output
        with open("bragdoc.md") as f:
            content = f.read()
        assert "[Machine Learning] Did something in ML" in content

def test_add_auto_category():
    with runner.isolated_filesystem():
        runner.invoke(app, ["init"])
        runner.invoke(app, ["category", "set", "Web Development"])
        runner.invoke(app, ["add", "Built a web app"])
        runner.invoke(app, ["category", "unset"])
        # Add a new entry with a similar topic, no category set
        result = runner.invoke(app, ["add", "Created a website"])
        assert "Assigned to existing category by similarity: 'Web Development'" in result.output
        assert "Added entry: [Web Development] Created a website" in result.output
        with open("bragdoc.md") as f:
            content = f.read()
        assert "[Web Development] Created a website" in content

def test_add_no_category_match():
    with runner.isolated_filesystem():
        runner.invoke(app, ["init"])
        runner.invoke(app, ["category", "set", "Machine Learning"])
        runner.invoke(app, ["add", "Did something in ML"])
        runner.invoke(app, ["category", "unset"])
        # Add a new entry with a very different topic, no category set
        result = runner.invoke(app, ["add", "Wrote a poem"])
        assert "Added entry: Wrote a poem" in result.output
        with open("bragdoc.md") as f:
            content = f.read()
        assert "Wrote a poem" in content
        assert "[Machine Learning]" not in content

def test_category_set_unset_show_change():
    with runner.isolated_filesystem():
        runner.invoke(app, ["init"])
        # Set
        result = runner.invoke(app, ["category", "set", "DevOps"])
        assert "Current category set to: DevOps" in result.output
        # Show
        result = runner.invoke(app, ["category", "show"])
        assert "Current category: DevOps" in result.output
        # Change
        result = runner.invoke(app, ["category", "change", "Backend"])
        assert "Current category changed to: Backend" in result.output
        result = runner.invoke(app, ["category", "show"])
        assert "Current category: Backend" in result.output
        # Unset
        result = runner.invoke(app, ["category", "unset"])
        assert "Current category unset." in result.output
        result = runner.invoke(app, ["category", "show"])
        assert "No current category set." in result.output

def test_category_list_and_select():
    with runner.isolated_filesystem():
        runner.invoke(app, ["init"])
        runner.invoke(app, ["category", "set", "ML"])
        runner.invoke(app, ["add", "Did ML work"])
        runner.invoke(app, ["category", "change", "Web"])
        runner.invoke(app, ["add", "Built a website"])
        runner.invoke(app, ["category", "change", "DevOps"])
        runner.invoke(app, ["add", "Deployed infra"])
        runner.invoke(app, ["category", "unset"])
        # List categories
        result = runner.invoke(app, ["category", "list"])
        assert "0: ML" in result.output
        assert "1: Web" in result.output
        assert "2: DevOps" in result.output
        # Select category by index
        result = runner.invoke(app, ["category", "select", "1"])
        assert "Current category set to: Web" in result.output
        # Show current category
        result = runner.invoke(app, ["category", "show"])
        assert "Current category: Web" in result.output
        # Out of range
        result = runner.invoke(app, ["category", "select", "10"])
        assert "out of range" in result.output or "No categories found." in result.output 