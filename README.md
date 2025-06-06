# RAG-Pipeline-PanScience

📄 DocTalk — Chat with Your Documents using RAG
DocTalk is an end-to-end Retrieval-Augmented Generation (RAG) application that enables users to upload .txt, .pdf, or .docx documents and interact with their content using natural language queries. It uses FAISS for semantic search, a HuggingFace embedding model for vectorization, Groq's LLaMA-3 for question answering, and MySQL for document persistence.


## 🚀 Features

- Upload and parse documents (.txt, .docx, .pdf)
- Vector-based document search using FAISS
- LLM-powered query answering (LLaMA3 via Groq)
- MySQL-based metadata/document text storage
- Full-stack: FastAPI backend, Streamlit frontend
- Simple UI for document upload and chat


## 🏗️ Project Structure
RAG-Pipeline/
│
├── backend/
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── models.py
│   └── backend_main.py
│
├── frontend/
│   └── frontend_main.py
│
├── uploaded_documents/          # Automatically created at runtime
├── vectorstore/                 # FAISS index stored here
├── .env                         # API keys (Groq/OpenAI)
├── .gitignore
├── requirements.txt
└── README.md


---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/RAG-Pipeline.git
cd RAG-Pipeline
```

## ✅ Local Installation (Python 3.9+ recommended)

### 1. Install requirements.txt file
```bash
pip install -r requirements.txt
```

## 🚀 Running the App

### 1. Start the FastAPI Backend
```bash
uvicorn backend.backend_main:app --reload
```
## Backend will be live at http://localhost:8000

### 2. Start the Streamlit Frontend
```bash
cd frontend
streamlit run frontend_main.py
```
## Frontend will be available at http://localhost:8501

## 🧪 API Endpoints
### 🔹 /upload/ — Upload Documents
- Method: POST

- Accepts: Multipart files (max 20)

- File Types: .txt, .pdf, .docx

- Stores content in MySQL and vectorizes using FAISS

## 🔹 /Ask/ — Ask a Question
- Method: POST

- Request Body: { "query": "Your question here" }

- Returns: JSON response with the LLM-generated answer from the document context

## 💾 MySQL Integration
- Make sure your MySQL server is running and accessible. You can update the connection string in:

## backend/db/database.py

```python
URL_DATABASE = 'mysql+pymysql://<user>:<password>@localhost:3306/RagApplication'
```
## Example:
- 'mysql+pymysql://root:Vishal%50mysql123@localhost:3306/RagApplication'

## 🧠 Tech Stack
Layer - Technology
Backend	- FastAPI, SQLAlchemy, LangChain
Frontend - Streamlit
DB - MySQL
Embeddings - HuggingFace Transformers
VectorDB - FAISS
LLM	Groq - LLaMA-3
Chunking - LangChain Recursive Splitter

## 👨‍💻 Developer Tips
### 1. Clear previous FAISS index if needed by deleting vectorstore/faiss_index folder.

### 2. Ensure .env is not tracked by Git:
## .gitignore
```bash
.env
__pycache__/
vectorstore/
uploaded_documents/
```

## 📷 UI Preview
### Upload your documents in the sidebar and start asking questions in the chat window.

## 🔧 Future Enhancements
- Support for more file types (.xlsx, .pptx)
- User authentication for document-specific chat
- Deployment on cloud (e.g., Render, AWS)