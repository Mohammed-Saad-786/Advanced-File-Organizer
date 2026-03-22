FROM python:3.11-slim

WORKDIR /app

# ❌ REMOVE apt-get, curl, everything

# Install Python deps only
COPY requirements.txt .
RUN pip install --no-cache-dir streamlit PyPDF2

# Copy app
COPY . .

EXPOSE 7860

CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
