import os
import pytest
from typer.testing import CliRunner
from brag.cli import app

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