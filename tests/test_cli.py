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