import streamlit as st
from brag.doc_utils import init_brag_doc, add_entry, read_history, purge_entries_between, init_brag_repo, get_brag_doc_path
from brag.git_utils import sync_with_git, get_git_history
from brag.ollama_utils import summarize_brag_doc, generate_resume_bullets
from datetime import datetime, timedelta
import re

st.set_page_config(page_title="Brag Doc Manager", layout="centered")
st.title("Brag Doc Manager 📝")

# --- Initialize Brag Doc ---
st.header("Initialize Brag Doc")
col1, col2 = st.columns(2)
with col1:
    if st.button("Initialize Brag Doc"):
        created = init_brag_doc()
        if created:
            st.success("Brag doc initialized.")
        else:
            st.info("Brag doc already exists.")
with col2:
    if st.button("Init Git Repo with Brag Doc"):
        bragdoc_path = init_brag_repo()
        st.success(f"Initialized git repo and brag doc at: {bragdoc_path}")

# --- Add Entry ---
st.header("Add a New Entry")
message = st.text_area("Message or achievement to add:")
if st.button("Add Entry"):
    if message.strip():
        add_entry(message)
        st.success(f"Added entry: {message}")
    else:
        st.warning("Please enter a message.")

# --- View History ---
st.header("Brag Doc History")
if st.button("Refresh History"):
    st.session_state['history'] = read_history()
    try:
        st.session_state['git_history'] = get_git_history()
    except Exception:
        st.session_state['git_history'] = []

history = st.session_state.get('history', read_history())
git_history = st.session_state.get('git_history', [])

if history:
    st.subheader("Brag Entries:")
    st.text("".join(history))
else:
    st.info("No brag doc entries found.")

if git_history:
    st.subheader("Git History:")
    for commit in git_history:
        st.text(f"- {commit.hexsha[:7]} {commit.summary} ({commit.committed_datetime})")

# --- Summarize ---
st.header("Summarize Brag Doc")
if st.button("Generate Summary with Ollama"):
    summary = summarize_brag_doc()
    st.text_area("Summary:", summary, height=200)

# --- Resume Bullets ---
st.header("Generate Resume Bullets")
if st.button("Generate Resume Bullets with Ollama"):
    bullets = generate_resume_bullets()
    st.text_area("Resume Bullets:", bullets, height=200)

# --- Purge Entries ---
st.header("Purge Entries")
def parse_relative_time(relative: str) -> str:
    now = datetime.now()
    days = 0
    hours = 0
    minutes = 0
    weeks = 0
    pattern = r"(?:(?P<w>\\d+)w)?(?:(?P<d>\\d+)d)?(?:(?P<h>\\d+)h)?(?:(?P<m>\\d+)m)?"
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

start = st.text_input("Start date (YYYY-MM-DD or relative, e.g., 2d, 1w5d, 1h5m)")
end = st.text_input("End date (YYYY-MM-DD or relative, e.g., 1d, 1w)")
if st.button("Purge Entries"):
    if not start and not end:
        st.warning("Please provide at least one of start or end.")
    else:
        now_str = datetime.now().strftime("%Y-%m-%d")
        try:
            start_date = parse_relative_time(start) if start and not re.match(r"\\d{4}-\\d{2}-\\d{2}", start) else (start or "1970-01-01")
        except Exception as e:
            st.error(f"Invalid start: {e}")
            start_date = None
        try:
            end_date = parse_relative_time(end) if end and not re.match(r"\\d{4}-\\d{2}-\\d{2}", end) else (end or now_str)
        except Exception as e:
            st.error(f"Invalid end: {e}")
            end_date = None
        if start_date and end_date:
            removed = purge_entries_between(start_date, end_date)
            st.success(f"Purged {removed} entries between {start_date} and {end_date}.")

# --- Sync with Git ---
st.header("Sync with Git")
if st.button("Sync Brag Doc with Git"):
    try:
        sync_with_git()
        st.success("Brag doc synced with git.")
    except Exception as e:
        st.error(f"Git sync failed: {e}") 