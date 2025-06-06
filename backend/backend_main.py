from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.embeddings import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from pydantic import BaseModel


import os
import shutil
import uuid
from dotenv import load_dotenv
load_dotenv()

from backend.db.database import SessionLocal, Base, engine
from backend.db.models import Docum
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI() 

UPLOAD_DIR = "uploaded_documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)

FAISS_INDEX_PATH = "vectorstore/faiss_index"
os.makedirs("vectorstore", exist_ok=True)

# API-key
groq_api_key = os.getenv("GROQ_API_KEY")


# Automatically create the tables at startup if they don’t exist
Base.metadata.create_all(bind=engine, checkfirst=True)

@app.post("/upload/")
async def upload_files(files: list[UploadFile] = File(...)):
    if len(files) > 20 :
          raise HTTPException(status_code=400, detail="Maximum 20 files allowed.")
    
    # local session set 
    session = SessionLocal()
    results = []
    all_documents = []

    for file in files:
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        # type check
        if file_ext not in [".pdf", ".txt", ".docx"]:
              raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_ext}")

        # unique-id created --> prevent duplication     
        unique_filename = f"{uuid.uuid4().hex}_{file.filename}"

        file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        if file_ext == ".txt":
                loader = TextLoader(file_path)
        elif file_ext == ".docx":
                loader = UnstructuredWordDocumentLoader(file_path)
        elif file_ext == ".pdf":
                loader = PyPDFLoader(file_path)
        else:
              pass
        
        if file_ext == ".pdf" and len(loader.load()) > 1000:
            raise HTTPException(status_code=400, detail="PDF exceeds 1000 pages.")
        

        # Load and merge document contents
        documents = loader.load()
        all_documents.extend(documents)
        combined_text = "\n\n".join([doc.page_content for doc in documents])

        # Save to MYSQL DB
        try:
            doc_entry = Docum(
                filename=file.filename,
                doc_type=file_ext,
                document_text=combined_text
            )
            session.add(doc_entry)
            session.commit()

            results.append({"filename": file.filename, "status": "Uploaded and saved"})

        except SQLAlchemyError as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
    session.close()

    
    if all_documents:

        # Chunking Function
        def get_text_chunks(documents):
           text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=1000)
           return text_splitter.split_documents(documents)

        # Storing in Vector Database
        def store_in_vdb(docs):
            embedding_model = HuggingFaceEmbeddings()

            if os.path.exists(FAISS_INDEX_PATH):
               db = FAISS.load_local(FAISS_INDEX_PATH, embedding_model, allow_dangerous_deserialization=True)
               db.add_documents(docs)
            else:
               db = FAISS.from_documents(docs, embedding_model)

            db.save_local(FAISS_INDEX_PATH)

        chunks = get_text_chunks(all_documents)
        store_in_vdb(chunks)


# Request schema
class QueryRequest(BaseModel):
    query: str

# Chat-response Workflow
@app.post("/Ask/")
async def conversational_chain(request: QueryRequest):
     
     query = request.query

     # Load vector DB
     embedding_model = HuggingFaceEmbeddings()
     if not os.path.exists(FAISS_INDEX_PATH):
         raise HTTPException(status_code=404, detail="No vector store found. Upload documents first.")
     
     db = FAISS.load_local(FAISS_INDEX_PATH,embedding_model,allow_dangerous_deserialization=True)
     retriever = db.as_retriever(search_kwargs={"k": 3})

     
     prompt = ChatPromptTemplate.from_template(
          """Answer the query as detailed as possible from the provided context, make sure to provide all the relevant information
          ,if answer is not in the available context just say , "Sorry! Answer to the query is not available", don't provide unnecessary reponses\n\n
          <context>
          {context}
          <context>
          Questions:{input}
          """
     )

     # LLM Loading
     llm = ChatGroq(groq_api_key=groq_api_key,
                    model_name="llama3-70b-8192")
     
     # Create Chain --> all chunks stuffed and sent to LLM
     chain = create_retrieval_chain(retriever, create_stuff_documents_chain(llm, prompt))

     output = chain.invoke({"input": query})

     return {"response": output["answer"] if "answer" in output else output}









    

    
