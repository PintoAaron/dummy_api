from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Dict
from schema import UserLogin, UserOut
from database import get_db
from models import User 
from utils import verify_password



router = APIRouter(tags=["Authentication"])


@router.post("/login",response_model=Dict[str,UserOut])
def login(request: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    return {"data": user}