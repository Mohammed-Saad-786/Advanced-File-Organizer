import streamlit as st
import os
import shutil
import zipfile
import uuid
import glob
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

# -----------------------------
# CONFIGURATION & CLEANUP
# -----------------------------
st.set_page_config(page_title="Pro File Organizer", page_icon="⚡", layout="wide")

def cleanup_old_data():
    """Deletes all temporary workspaces and generated ZIPs to free disk space."""
    workspaces = glob.glob("workspace_*")
    zips = glob.glob("Organized_*.zip")
    for folder in workspaces:
        shutil.rmtree(folder, ignore_errors=True)
    for f in zips:
        try: os.remove(f)
        except: pass
    st.sidebar.success("Disk Cleaned!")

# Sidebar for storage management
with st.sidebar:
    st.header("⚙️ Storage Management")
    if st.button("🗑️ Clear All Temp Data"):
        cleanup_old_data()
    st.info("Use this if you get a 'No space left' error.")

# Categories Mapping
CATEGORIES = {
    "PDF Files": [".pdf"],
    "Word Files": [".docx", ".doc", ".rtf"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".dat"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".sql", ".json"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Spreadsheets": [".xlsx", ".xls", ".csv"]
}

EXTENSION_MAP = {ext: folder for folder, exts in CATEGORIES.items() for ext in exts}
MAX_WORKERS = min(32, multiprocessing.cpu_count() * 2)

# -----------------------------
# CORE LOGIC
# -----------------------------
def process_single_file(file_info):
    filename, root, extract_path = file_info
    filepath = os.path.join(root, filename)

    if filename.startswith('.') or filename.startswith('~$'):
        return None

    ext = Path(filename).suffix.lower()
    target_folder = EXTENSION_MAP.get(ext, "Others")
    dest_dir = os.path.join(extract_path, target_folder)
    os.makedirs(dest_dir, exist_ok=True)
    
    dest_path = os.path.join(dest_dir, filename)
    if os.path.exists(dest_path):
        dest_path = os.path.join(dest_dir, f"{uuid.uuid4().hex[:4]}_{filename}")

    try:
        shutil.move(filepath, dest_path)
        return 1
    except:
        return 0

# -----------------------------
# UI & EXECUTION
# -----------------------------
st.title("📂 High-Performance File Organizer")
st.write("Optimized for large folders with automatic disk cleanup.")

uploaded_file = st.file_uploader("Upload Messy ZIP (Max 1GB)", type="zip")

if uploaded_file:
    session_id = uuid.uuid4().hex[:8]
    work_dir = f"workspace_{session_id}"
    output_zip_name = f"Organized_{session_id}"
    
    os.makedirs(work_dir, exist_ok=True)

    try:
        with st.status("⚡ Processing...", expanded=True) as status:
            # 1. Extract
            st.write("📦 Extracting...")
            with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
                zip_ref.extractall(work_dir)

            # 2. Scan
            file_tasks = []
            for root, _, files in os.walk(work_dir):
                if any(cat in root for cat in CATEGORIES): continue
                for f in files:
                    file_tasks.append((f, root, work_dir))

            # 3. Parallel Sort
            st.write(f"🚀 Sorting {len(file_tasks)} files...")
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                results = list(executor.map(process_single_file, file_tasks))

            # 4. ZIP & CLEANUP (Crucial for Errno 28)
            st.write("📦 Compressing results...")
            shutil.make_archive(output_zip_name, 'zip', work_dir)
            
            # Delete extracted folder immediately to free space
            shutil.rmtree(work_dir) 
            
            status.update(label="✅ Finished! Workspace cleared.", state="complete")

        st.balloons()
        with open(f"{output_zip_name}.zip", "rb") as f:
            st.download_button(
                label="⬇️ Download Organized Folder",
                data=f,
                file_name="Organized_Files.zip",
                mime="application/zip",
                use_container_width=True
            )
            
    except OSError as e:
        if e.errno == 28:
            st.error("🚨 Disk Full! Click 'Clear All Temp Data' in the sidebar and try a smaller file.")
        else:
            st.error(f"❌ System Error: {e}")