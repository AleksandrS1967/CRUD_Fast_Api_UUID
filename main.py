from fastapi import FastAPI, Depends, HTTPException
from services import services
from models import models
from schemas import schemas
from db import get_db, engine
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/tasks/", response_model=list[schemas.Task])
def get_all_tasks(db: Session = Depends(get_db)):
    return services.get_tasks(db)

@app.get("/task/{uuid}", response_model=schemas.Task)
def get_task_by_uuid(uuid: str, db: Session = Depends(get_db)):
    try:
        task_queryset = services.get_task(db, uuid)
        return task_queryset
    except Exception:
        raise HTTPException(status_code=404, detail="Неверный UUID")

@app.post("/tasks/", response_model=schemas.Task)
def create_new_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return services.create_task(db, task)

@app.put("/task/{uuid}", response_model=schemas.Task)
def update_task_by_uuid(task: schemas.TaskCreate, uuid: str, db: Session = Depends(get_db)):
    try:
        task_queryset = services.update_task(db, task, uuid)
        return task_queryset
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Неверный UUID - {str(e)}") from e

@app.delete("/task/{uuid}", response_model=schemas.Task)
def delete_task_by_uuid(uuid: str, db: Session = Depends(get_db)):
    try:
        delete_entry = services.delete_task(db, uuid)
        return delete_entry
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Неверный UUID - {str(e)}") from e
