from sqlalchemy import Column, Integer, String, Date, Boolean, BigInteger
from database import Base, engine

if engine.dialect.name == 'sqlite':
    date_type = String
    bool_type = Integer
    big_int_type = Integer
    
else:
    date_type = Date
    bool_type = Boolean
    big_int_type = BigInteger

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)