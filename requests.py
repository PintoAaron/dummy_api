from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Requests, User
from schema import RequestCreate



router = APIRouter(prefix="/requests", tags=["Requests"])



@router.get("/", status_code=status.HTTP_200_OK)
def get_requests(db: Session = Depends(get_db)):
    requests = db.query(Requests).all()
    return {"data": requests}


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_request(request: RequestCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.user_id == request.user_id).first() is None:
        raise HTTPException(
              status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    if db.query(Requests).filter(Requests.user_id == request.user_id).first():
        raise HTTPException(
              status_code=status.HTTP_400_BAD_REQUEST, detail="User already has a request")
    new_request = Requests(user_id=request.user_id, food=request.food)
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return {"data": new_request}
        