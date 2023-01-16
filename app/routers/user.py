from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter,Request
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.params import Body
from .. import models,schemas,utils,oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from .. import oauth2
router=APIRouter(
    prefix='/users',
    tags=['Users']
)
@router.post("/signup",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
async def create_user(user:Request ,db : Session = Depends(get_db)):
    print(user.json())
#    schemas.NewUser
    user_credentials=await user.json()
    print(user_credentials)
    print(user_credentials)
    # user={
    #     "email":user_credentials.email,
    #     "age":user_credentials.age,
    #     "title":user_credentials.title,
    #     "password":user_credentials.password
       
    # }
    new_post=models.User(**user_credentials)
    if not db.query(models.User).filter(models.User.email==user_credentials['email']).first():
        hashed_pass=utils.hash(new_post.password)
        new_post.password=hashed_pass
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f'{user_credentials["email"]} is already Registered')

@router.post('/login',status_code=status.HTTP_202_ACCEPTED,response_model=schemas.Token)
# async def loign_User(user_credentials:OAuth2PasswordRequestForm()=Depends(),db:Session = Depends(get_db)):
async def loign_User(user_credentials:Request,db:Session = Depends(get_db)):
    user_credentials=await user_credentials.json()
    print(user_credentials)
    user=db.query(models.User).filter(models.User.email==user_credentials['email']).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials")
    if not utils.verify(user_credentials["password"] ,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials")
    access_token=oauth2.create_access_token(data={
        "username":user.email
    })
    return {'Access_Token':access_token,'Token_type':'Bearer'}


# @router.get('/{id}',response_model=schemas.UserOut)
# async def get_user(id:int ,response: Response,db : Session = Depends(get_db),get_current_user:str =Depends(oauth2.get_current_user)):
#     post=db.query(models.User).filter(models.User.id== id).first( )
#     if not post:
#         raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f'item with id {id} not found')
#     return post

# @router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
# async def delete_user(id:int,response:Response,db : Session = Depends(get_db)):
#     query=db.query(models.User).filter(models.User.id== id)
#     if query.first()==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post with id {id} does not exist')
#     query.delete(synchronize_session=False)
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
@router.get("/",response_model=list[schemas.UserOut])
async def get_allusers(db : Session = Depends(get_db)):
    posts=db.query(models.User).all()
    print('I am clicked')
    return posts
