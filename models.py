from db import Base
from sqlalchemy import Integer,Column,String,Numeric
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,index=True)
    description = Column(String,index=True)
    author = Column(String,index=True)
    year = Column(Integer,nullable=False)
    price = Column(Numeric,nullable=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True)
    name = Column(String,nullable=False)
    email = Column(String,nullable=False)
    role = Column(String,nullable=False)
    hash_pwd: Mapped[str] = mapped_column(nullable=False)
    # Use Mapped[bool] to help the type checker understand the eventual type
    is_active: Mapped[bool] = mapped_column(default=True)
