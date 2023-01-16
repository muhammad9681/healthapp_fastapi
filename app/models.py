from .database import Base
from sqlalchemy import Column,Integer,String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
class User(Base):
    __tablename__="patients"
    id= Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    title= Column(String,nullable=False)
    age= Column(Integer,nullable=False)
    timestamp=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()')) 