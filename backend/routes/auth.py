import os
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from database.db import SessionLocal
from models.user import User
from schemas.auth_schema import SignupSchema, LoginSchema
from utils.security import hash_password, verify_password
import traceback


router = APIRouter(prefix="/auth", tags=["Authentication"])

SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def validate_any_email(email: str):
    normalized_email = email.strip().lower()
    
    
    if "@" not in normalized_email or "." not in normalized_email.split("@")[-1]:
        raise HTTPException(status_code=400, detail="Invalid email address format")
        
    return normalized_email


def create_access_token(data: dict):
    expires_at = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = data.copy()
    token_data.update({"exp": expires_at})
    return jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/signup")
async def signup(payload: SignupSchema, db: Session = Depends(get_db)):
    try:
        fullname = payload.fullname 
        password = payload.password
        
        
        email = validate_any_email(payload.email)
        
        # Double check kung registered na ang email
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
            
        hashed_pass = hash_password(password)
            
        new_user = User(
            fullname=fullname,  
            email=email,
            password=hashed_pass
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User registered successfully"}

    except HTTPException as he:
        raise he
    except Exception as e:
        print("======== CRASH LOG DETECTED ========")
        traceback.print_exc()
        print("====================================")
        raise HTTPException(status_code=500, detail=f"Backend Error: {str(e)}")

@router.post("/login")
async def login(user: LoginSchema, db: Session = Depends(get_db)):
    email_clean = validate_any_email(user.email)

    existing_user = db.query(User).filter(
        User.email == email_clean
    ).first()

    if not existing_user or not verify_password(user.password, existing_user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # (Optional) I-check kung anong primary key identity field meron ang model mo (.id o .user_id)
    user_identifier = getattr(existing_user, "id", getattr(existing_user, "user_id", None))
    user_fullname = getattr(existing_user, "fullname", getattr(existing_user, "full_name", "User"))

    return {
        "message": "Login successful",
        "user_id": user_identifier,
        "fullname": user_fullname,
        "email": existing_user.email
    }
    