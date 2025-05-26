# Route which defines a URL path users can access relating to tasks
# Defines functions users can access via method (post, put and delete requests) to specific paths (URLS)

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from app import models, schemas
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import Optional, List

router = APIRouter(
    prefix="/tasks",
    tags=['Task']
)



@router.post("", status_code=status.HTTP_201_CREATED)
def create_task(post: schemas.TaskCreate, db: Session = Depends(get_db)):
    new_task = models.Task(title=post.title)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    return tasks

@router.get("/{id}")
def get_task(id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task



@router.put("/complete/{id}", status_code=status.HTTP_200_OK)
def complete_task(id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = True
    task.completed_at = func.now()
    db.commit()
    db.refresh(task)

    return task



@router.put("/undo-complete/{id}", status_code=status.HTTP_200_OK)
def undo_complete_task(id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = False
    task.completed_at = None
    db.commit()
    db.refresh(task)

    return task



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.query(models.Task).filter(models.Task.id == id).delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)