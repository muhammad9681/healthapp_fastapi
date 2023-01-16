from fastapi import FastAPI,Depends
from fastapi.params import Body
import time
import psycopg2
from . import models,schemas,utils
from sqlalchemy.orm import Session
from .database import engine,get_db
from psycopg2.extras import RealDictCursor
from .routers import data,user
models.Base.metadata.create_all(bind=engine)
app = FastAPI()
while True:
    try:
     conn=psycopg2.connect(host='localhost',database='health_app_db',user='postgres',password='admin',cursor_factory=RealDictCursor)
     cursor=conn.cursor()
     print("Connected Successfuly")
     break
    except Exception as error:
     print("Connecting to database was failed. Error was failed :",error)
     time.sleep(120)
app.include_router(user.router)
@app.get("/", )
async def root(db : Session = Depends(get_db)):
    print('I am clicked')
    return {"message":"Server live"}











