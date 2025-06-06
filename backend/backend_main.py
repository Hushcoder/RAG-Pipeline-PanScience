from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
import os
import shutil
import uuid

from backend.db.database import SessionLocal, Base, engine
from backend.db.models import Docum
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI() 

UPLOAD_DIR = "uploaded_documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Automatically create the tables at startup if they don’t exist
Base.metadata.create_all(bind=engine, checkfirst=True)

@app.post("/upload/")
async def upload_files(files: list[UploadFile] = File(...)):
    if len(files) > 20 :
          raise HTTPException(status_code=400, detail="Maximum 20 files allowed.")
    
    # local session set 
    session = SessionLocal()
    results = []

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
        finally:
            session.close()
            
        return {"result" : results} 