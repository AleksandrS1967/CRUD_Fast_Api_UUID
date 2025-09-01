from models.models import Task
from sqlalchemy.orm import Session
from schemas.schemas import TaskCreate
from fastapi import HTTPException


def create_task(db: Session, data: TaskCreate):
    try:
        task = Task(**data.model_dump())
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка при создании задачи {str(e)}") from e


def get_tasks(db: Session):
    return db.query(Task).all()


def get_task(db: Session, task_uuid: str):
    try:
        task_object = db.query(Task).filter(Task.uuid == task_uuid).first()
        if task_object:
            return task_object
        raise HTTPException(status_code=400, detail=f"неверный UUID")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка при получении задачи {str(e)}") from e


def update_task(db: Session, task: TaskCreate, task_uuid: str):
    try:
        task_object = get_task(db, task_uuid)
        if task_object:
            for key, value in task.model_dump().items():
                setattr(task_object, key, value)
            db.commit()
            db.refresh(task_object)
            return task_object
        raise HTTPException(status_code=400, detail=f"неверный UUID")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка при обновлении задачи {str(e)}") from e


def delete_task(db: Session, uuid: str):
    try:
        task_object = get_task(db, uuid)
        if task_object:
            db.delete(task_object)
            db.commit()
            return task_object
        raise HTTPException(status_code=400, detail=f"неверный UUID")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка при обновлении задачи {str(e)}") from e
