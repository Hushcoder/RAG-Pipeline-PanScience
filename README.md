# RAG-Pipeline-PanScience

📄 DocTalk — Chat with Your Documents using RAG
DocTalk is an end-to-end Retrieval-Augmented Generation (RAG) application that enables users to upload .txt, .pdf, or .docx documents and interact with their content using natural language queries. It uses FAISS for semantic search, a HuggingFace embedding model for vectorization, Groq's LLaMA-3 for question answering, and MySQL for document persistence.

🧠 Features
Upload up to 20 documents (.txt, .pdf, .docx)

Extracts, chunks, and embeds content into a FAISS vector store

Chat interface using Streamlit frontend

LLM-backed Q&A using Groq LLaMA-3

MySQL for structured document storage

HuggingFace-based embeddings for fast similarity search

📁 Project Structure
bash
Copy
Edit
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

⚙️ Setup Instructions
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/yourusername/RAG-Pipeline.git
cd RAG-Pipeline
2. Environment Variables
Create a .env file in the root directory:

ini
Copy
Edit
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key  # (if used in future)
3. Install Dependencies
You can install dependencies either locally or using Docker.

✅ Local Installation (Python 3.9+ recommended)
bash
Copy
Edit
pip install -r requirements.txt
🐳 Docker (Optional)
bash
Copy
Edit
docker-compose up --build
Docker will set up the backend and the frontend; ensure your MySQL service is accessible to the container.

🚀 Running the App
1. Start the FastAPI Backend
bash
Copy
Edit
uvicorn backend.backend_main:app --reload
Backend will be live at http://localhost:8000

2. Start the Streamlit Frontend
bash
Copy
Edit
cd frontend
streamlit run frontend_main.py
Frontend will be available at http://localhost:8501

🧪 API Endpoints
🔹 /upload/ — Upload Documents
Method: POST

Accepts: Multipart files (max 20)

File Types: .txt, .pdf, .docx

Stores content in MySQL and vectorizes using FAISS

🔹 /Ask/ — Ask a Question
Method: POST

Request Body: { "query": "Your question here" }

Returns: JSON response with the LLM-generated answer from the document context

💾 MySQL Integration
Make sure your MySQL server is running and accessible. You can update the connection string in:

backend/db/database.py

python
Copy
Edit
URL_DATABASE = 'mysql+pymysql://<user>:<password>@localhost:3306/RagApplication'
Example:
'mysql+pymysql://root:Vishal%40mysql123@localhost:3306/RagApplication'

🧠 Tech Stack
Layer	Technology
Backend	FastAPI, SQLAlchemy, LangChain
Frontend	Streamlit
DB	MySQL
Embeddings	HuggingFace Transformers
Vector DB	FAISS
LLM	Groq - LLaMA-3
Chunking	LangChain Recursive Splitter

🛡️ Notes
Maximum of 1000 pages is supported per .pdf

Documents are chunked into 2000-character blocks with 1000-character overlap

Make sure FAISS index and MySQL DB are not deleted between sessions

👨‍💻 Developer Tips
Clear previous FAISS index if needed by deleting vectorstore/faiss_index folder.

Ensure .env is not tracked by Git:

.gitignore

bash
Copy
Edit
.env
__pycache__/
vectorstore/
uploaded_documents/
📷 UI Preview
Upload your documents in the sidebar and start asking questions in the chat window.

🔧 Future Enhancements
Support for more file types (.xlsx, .pptx)

User authentication for document-specific chat

Integration with OpenAI or Anthropic models as fallback

Streamed chat interface

Deployment on cloud (e.g., Render, AWS)

📜 License
This project is licensed under the MIT License.

🙌 Acknowledgements
LangChain

HuggingFace

Groq

FAISS