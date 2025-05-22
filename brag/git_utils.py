import git
import os
from brag.doc_utils import get_brag_doc_path
from brag.constants import GIT_COMMIT_MESSAGE

def sync_with_git():
    brag_doc = get_brag_doc_path()
    repo = git.Repo(os.getcwd())
    repo.git.add(brag_doc)
    repo.index.commit(GIT_COMMIT_MESSAGE)
    origin = repo.remote(name='origin')
    origin.push()

def get_git_history():
    brag_doc = get_brag_doc_path()
    repo = git.Repo(os.path.dirname(brag_doc))
    return list(repo.iter_commits(paths=brag_doc))
