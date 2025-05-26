from fastapi import FastAPI
from app.routers import task
from app.database import engine
from app import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(task.router)

@app.get("/") 
async def root(): 
    return {"message": "I am gRoot!"} 