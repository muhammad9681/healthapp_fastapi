from pydantic import BaseModel,EmailStr
from typing import Optional
class NewUser(BaseModel):
    email:EmailStr
    password:str
    title:str
    age:int
# Second class will be updated as per data of the patient table later...
class UserData(BaseModel):
    Unique_UserName:str
    Blood_pressure:int
    Temperature:int
    Last_night_sleep:int
    apetite:str
    class Config:
        orm_mode=True
#Signed Up User Response Model..
class UserOut(BaseModel):
    id:int
    email:str
    class Config:
        orm_mode=True
#USerLogin Schemma
class UserLogin(BaseModel):
    email:EmailStr
    password:str
    class Config:
        orm_mode=True
class Token(BaseModel):
    Access_Token:str
    Token_type:str
    class Config:
        orm_mode=True
class TokenData(BaseModel):
    username:Optional[str]=None
    class Config:
        orm_mode=True