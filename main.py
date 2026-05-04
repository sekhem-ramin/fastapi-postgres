from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import services, models, schemas
from db import get_db, engine
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from models import User


app = FastAPI()


@app.get('/users/all', response_model=list[schemas.UserResponse])
def get_all_users(db:Session = Depends(get_db)):
    return services.get_users(db)

@app.get('/users/{id}', response_model=schemas.UserResponse)
def get_user(id:int,db:Session = Depends(get_db)):
    user = services.get_user_by_id(db,id)
    if not user:
        raise HTTPException(status_code=404, detail="User Id not found!")
    return user

@app.post('/users', response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create new user account"""
    if services.get_user_by_email(db,user.email) is not None:
        raise HTTPException(status_code=400, detail="User Email account exists!")
    hashed_password = services.get_pwd_hash(user.hash_pwd)
    user.hash_pwd = hashed_password
    return services.create_new_user_accnt(db,user)

@app.post('/token', response_model=schemas.Token)
def create_user_login_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                   db: Session = Depends(get_db)):
    user_accnt = services.get_user_by_email(db,form_data.username)

    if not user_accnt or not services.verify_pwd(form_data.password, user_accnt.hash_pwd):
        raise HTTPException(status_code=404, detail="Invalid User account details provided!")
    
    if not user_accnt.is_active:
        raise HTTPException(status_code=403, detail="User account is deactivated!")
    
    access_token_expires = timedelta(minutes=20)
    access_token_result = services.create_access_token(
        data ={"sub":user_accnt.email}, expires_delta=access_token_expires)
    
    return {"access_token":access_token_result,"token_type":"bearer"}

@app.get('/profile', response_model=schemas.UserResponse)
def get_user_profile(current_user: User = Depends(services.get_current_active_user)):
    return current_user

@app.get('/verify-token')
def verify_token_endpoint(current_user: User = Depends(services.get_current_active_user)):
    return {
        "valid": True,
        "user": {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "role": current_user.role,
        }
    }


# - - - - - - - - - - - - - -
@app.get('/books/', response_model=list[schemas.Book])
def get_all_books(db: Session = Depends(get_db)):
    return services.get_books(db)

@app.get('/books/{id}', response_model=schemas.Book)
def fetch_book(id:int,db: Session = Depends(get_db)):
    book_queryset = services.get_book_by_id(db,id)
    if book_queryset:
        return book_queryset
    else:
        raise HTTPException(status_code=404, detail="Invalid book id given!")

@app.post('/books/', response_model=schemas.Book)
def create_new_book(book: schemas.BookCreate, db: Session = Depends(get_db), current_user: User = Depends(services.get_current_active_user)):
    return services.create_book(db,book)

@app.put('/books/{id}', response_model=schemas.Book)
def update_book(book: schemas.BookCreate, id:int, db: Session = Depends(get_db), current_user: User = Depends(services.get_current_active_user)):
    db_update = services.update_book(db,book,id)
    if not db_update:
        raise HTTPException(status_code=404, detail="Book not found!")
    return db_update

@app.delete('/books/{id}', response_model=schemas.Book)
def delete_book(id:int,db: Session = Depends(get_db), current_user: User = Depends(services.get_current_active_user)):
    delete_entry = services.delete_book(db,id)
    if delete_entry:
        return delete_entry
    else:
        raise HTTPException(status_code=404, detail="Entry not found!")