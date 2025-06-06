from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base 

# Enter your database url
URL_DATABASE = 'mysql+pymysql://<user>:<password>@localhost:3306/RagApplication'

#engine created 
engine = create_engine(URL_DATABASE)

#session created
SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind=engine) 

Base = declarative_base()