# 📂 Fast File Organizer (Advanced)

A high-performance, web-based tool designed to instantly sort messy folders into categorized subdirectories using concurrent processing.

### 🔗 Live Demo
**[Try the Live App Here](https://huggingface.co/spaces/mohd-saad/fast-file-organizer)**

---

## 🚀 Key Features
* **Parallel Processing**: Utilizes multi-core threading to handle hundreds of files simultaneously, significantly reducing processing time.
* **Instant Sorting**: Uses `os.rename` logic to update file system pointers instantly rather than physically copying data.
* **Auto-Cleanup Engine**: Automatically wipes temporary workspaces immediately after processing to maintain server storage health and prevent disk errors.
* **Dynamic Workspaces**: Implements unique UUID-based sessions to allow multiple users to organize files simultaneously without conflicts.
* **Bypass Storage Limits**: Configured via `.streamlit/config.toml` to support large file uploads (up to 1GB), bypassing the standard 200MB limit.

---

## 🛠️ Technology Stack
* **Language**: Python 3.11+
* **Web Framework**: Streamlit
* **Deployment**: Docker & Hugging Face Spaces
* **Core Libraries**: `shutil`, `os`, `zipfile`, `concurrent.futures`, `uuid`

---

## 📂 Category Mapping
The tool automatically organizes files into the following structured folders:
* **PDF Files**: `.pdf`
* **Word Files**: `.docx`, `.doc`, `.rtf`
* **Videos**: `.mp4`, `.mov`, `.avi`, `.mkv`, `.dat`
* **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.svg`, `.webp`
* **Code**: `.py`, `.js`, `.html`, `.css`, `.java`, `.cpp`, `.sql`, `.json`
* **Archives**: `.zip`, `.rar`, `.tar`, `.gz`, `.7z`
* **Spreadsheets**: `.xlsx`, `.xls`, `.csv`

---

## ⚙️ How to Use
1. **Compress** your messy files into a `.zip` archive.
2. **Upload** the ZIP to the live link provided above.
3. **Download** the instantly organized ZIP file.

---

## 👨‍💻 Author
**Mohammed Saad** *Computer Science & Engineering Student* [Marri Laxman Reddy Institute of Technology and Management](https://mlritm.ac.in/)
