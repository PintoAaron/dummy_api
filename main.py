from fastapi import FastAPI
from database import engine
import users, requests, auth

import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(requests.router)
app.include_router(auth.router)

@app.get("/")
def home():
    return {"message": "Hello World"}
