import streamlit as st
from brag.doc_utils import init_brag_doc, add_entry, read_history, purge_entries_between, init_brag_repo, get_brag_doc_path
from brag.git_utils import sync_with_git, get_git_history
from brag.ollama_utils import (
    summarize_brag_doc, generate_resume_bullets,
    generate_profile_based_resume, generate_profile_based_summary
)
from brag.profile import (
    init_profile, get_profile, update_profile_field,
    add_list_item, remove_list_item
)
from brag.constants import PROFILE_FIELDS
from datetime import datetime, timedelta
import re
import json

st.set_page_config(page_title="Brag Doc Manager", layout="centered")
st.title("Brag Doc Manager 📝")

# --- Initialize Brag Doc ---
st.header("Initialize Brag Doc")
col1, col2, col3 = st.columns(3)
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
with col3:
    if st.button("Initialize Profile"):
        created = init_profile()
        if created:
            st.success("Developer profile initialized.")
        else:
            st.info("Developer profile already exists.")

# --- Profile Management ---
with st.expander("Profile Management"):
    profile = get_profile()
    
    # Show current profile
    st.subheader("Your Developer Profile")
    st.json(profile)
    
    # Update basic fields
    st.subheader("Update Basic Information")
    basic_field = st.selectbox("Select field to update", 
                              ["name", "title", "summary", "contact.email", 
                               "contact.phone", "contact.linkedin", "contact.github"])
    field_value = st.text_input("New value", value="")
    if st.button("Update Field") and field_value:
        update_profile_field(basic_field, field_value)
        st.success(f"Updated {basic_field}")
        st.rerun()
    
    # List fields management
    st.subheader("Manage List Fields")
    list_field = st.selectbox("Select list field", ["skills", "experience", "education"])
    
    # Add item to list
    col1, col2 = st.columns(2)
    with col1:
        new_item = st.text_input("New item", value="")
        if st.button("Add Item") and new_item:
            add_list_item(list_field, new_item)
            st.success(f"Added to {list_field}")
            st.rerun()
    
    # Remove item from list
    with col2:
        if profile.get(list_field):
            item_index = st.number_input("Item index to remove", min_value=0, 
                                        max_value=len(profile.get(list_field, [])) - 1 if profile.get(list_field) else 0)
            if st.button("Remove Item") and profile.get(list_field):
                if item_index < len(profile.get(list_field, [])):
                    removed = remove_list_item(list_field, int(item_index))
                    st.success(f"Removed: {removed}")
                    st.rerun()
                else:
                    st.error("Invalid index")
        else:
            st.info(f"No items in {list_field} yet")

# --- Add Entry ---
st.header("Add a New Entry")
message = st.text_area("Message or achievement to add:")
if st.button("Add Entry"):
    if message.strip():
        # Display personalized greeting if profile exists
        try:
            if profile["name"] and profile["title"]:
                st.success(f"Hi {profile['name']}! Tracking your achievements as a {profile['title']}.")
        except:
            pass
        
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
st.header("Generate Content with Ollama")
tab1, tab2, tab3, tab4 = st.tabs(["Basic Summary", "Resume Bullets", "Profile Resume", "Profile Summary"])

with tab1:
    if st.button("Generate Basic Summary"):
        summary = summarize_brag_doc()
        st.text_area("Summary:", summary, height=200)

with tab2:
    if st.button("Generate Basic Resume Bullets"):
        bullets = generate_resume_bullets()
        st.text_area("Resume Bullets:", bullets, height=200)

with tab3:
    if st.button("Generate Profile-based Resume"):
        profile_resume = generate_profile_based_resume()
        st.text_area("Complete Resume:", profile_resume, height=300)

with tab4:
    if st.button("Generate Profile-based Summary"):
        profile_summary = generate_profile_based_summary()
        st.text_area("Professional Summary:", profile_summary, height=200)

# --- Purge Entries ---
st.header("Purge Entries")
def parse_relative_time(relative: str) -> str:
    now = datetime.now()
    days = 0
    hours = 0
    minutes = 0
    weeks = 0
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

start = st.text_input("Start date (YYYY-MM-DD or relative, e.g., 2d, 1w5d, 1h5m)")
end = st.text_input("End date (YYYY-MM-DD or relative, e.g., 1d, 1w)")
if st.button("Purge Entries"):
    if not start and not end:
        st.warning("Please provide at least one of start or end.")
    else:
        now_str = datetime.now().strftime("%Y-%m-%d")
        try:
            start_date = parse_relative_time(start) if start and not re.match(r"\d{4}-\d{2}-\d{2}", start) else (start or "1970-01-01")
        except Exception as e:
            st.error(f"Invalid start: {e}")
            start_date = None
        try:
            end_date = parse_relative_time(end) if end and not re.match(r"\d{4}-\d{2}-\d{2}", end) else (end or now_str)
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