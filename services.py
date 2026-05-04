from models import Book, User
from sqlalchemy.orm import Session
from schemas import BookCreate, UserCreate, TokenData
from passlib.context import CryptContext
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import os
from typing import Optional
from datetime import datetime, timedelta
import pytz
from fastapi import FastAPI, Depends, HTTPException
from db import get_db, engine

def get_users(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_new_user_accnt(db: Session, data: UserCreate):
    user_instance = User(**data.model_dump())
    db.add(user_instance)
    db.commit()
    db.refresh(user_instance)
    return user_instance

# - - - - - - - - - - - -
def create_book(db: Session, data: BookCreate):
    book_instance = Book(**data.model_dump())
    db.add(book_instance)
    db.commit()
    db.refresh(book_instance)
    return book_instance

def get_books(db: Session):
    return db.query(Book).all()

def get_book_by_id(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()

def update_book(db: Session, book: BookCreate, book_id: int):
    book_queryset = db.query(Book).filter(Book.id == book_id).first()
    if book_queryset:
        for key,value in book.model_dump().items():
            setattr(book_queryset, key, value)
        db.commit()
        db.refresh(book_queryset)
    return book_queryset

def delete_book(db: Session, book_id: int):
    book_queryset = db.query(Book).filter(Book.id == book_id).first()
    if book_queryset:
        db.delete(book_queryset)
        db.commit()
    return book_queryset

# - - - - - - - - - - - -
# Security Config
SECRET_KEY = str(os.getenv('FASTAPI_SECRET_KEY'))
ALGORITHM = 'HS256'

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def get_current_user( db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    token_data = verify_token(token)
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise HTTPException(status_code=401,
                            detail="Account credentials could not be verified!",
                            headers={"WWW-Authenticate":"Bearer"})
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=404,
                            detail="Account has been deactivated!")
    return current_user


def verify_pwd(input_password: str, hashed_password: str) -> bool:
    return password_context.verify(input_password,hashed_password)

def get_pwd_hash(input_pwd: str) -> str:
    return password_context.hash(input_pwd)

def create_access_token(data:dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(pytz.utc) + expires_delta
    else:
        expire = datetime.now(pytz.utc) + timedelta(minutes=15)
    
    to_encode.update({"expiry":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(input_token: str) -> TokenData:
    try:
        payload = jwt.decode(input_token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401,
                                detail="Account credentials could not be verified!",
                                headers={"WWW-Authenticate":"Bearer"})
        return TokenData(email=email)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401,
                                detail="Account credentials could not be verified!",
                                headers={"WWW-Authenticate":"Bearer"})