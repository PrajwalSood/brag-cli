import git
import os

BRAG_DOC = "bragdoc.md"

def sync_with_git():
    repo = git.Repo(os.getcwd())
    repo.git.add(BRAG_DOC)
    repo.index.commit("Update brag doc")
    origin = repo.remote(name='origin')
    origin.push()

def get_git_history():
    repo = git.Repo(os.getcwd())
    return list(repo.iter_commits(paths=BRAG_DOC))
