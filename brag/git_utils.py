import git
import os
from brag.doc_utils import get_brag_doc_path

def sync_with_git():
    brag_doc = get_brag_doc_path()
    repo = git.Repo(os.getcwd())
    repo.git.add(brag_doc)
    repo.index.commit("Update brag doc")
    origin = repo.remote(name='origin')
    origin.push()

def get_git_history():
    brag_doc = get_brag_doc_path()
    repo = git.Repo(os.getcwd())
    return list(repo.iter_commits(paths=brag_doc))
