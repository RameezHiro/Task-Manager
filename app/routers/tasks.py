from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import Task, User
from app.schemas import TaskCreate, TaskResponse, TaskStatusUpdate
from app.utils.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("", response_model=TaskResponse)
def create_task(
    task_data: TaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    task = Task(**task_data.model_dump(), owner_id=current_user.id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.get("", response_model=list[TaskResponse])
def get_tasks(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    tasks = session.exec(select(Task).where(Task.owner_id == current_user.id)).all()
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    task = session.get(Task, task_id)
    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    task = session.get(Task, task_id)
    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task_data.model_dump().items():
        setattr(task, key, value)
    session.commit()
    session.refresh(task)
    return task

@router.patch("/{task_id}/status", response_model=TaskResponse)
def update_status(
    task_id: int,
    status_data: TaskStatusUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    task = session.get(Task, task_id)
    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = status_data.status
    session.commit()
    session.refresh(task)
    return task

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    task = session.get(Task, task_id)
    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"message": "Task deleted"}