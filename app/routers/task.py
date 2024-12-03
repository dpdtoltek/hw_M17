from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import User, Task
from app.schemas import CreateUser, CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix='/task', tags=['task'])
DbSession = Annotated[Session, Depends(get_db)]


@router.get('/')
async def all_tasks(db: DbSession):
    tasks = db.scalars(select(Task)).all()
    return tasks


@router.get('/task_id')
async def task_by_id(task_id, db: DbSession):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is not None:
        return task
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')


@router.post('/create')
async def create_task(user_id: int, db: DbSession, create_task: CreateTask):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is not None:
        db.execute(insert(Task).values(
            title=create_task.title,
            content=create_task.content,
            priority=create_task.priority,
            user_id=user_id,
            slug=slugify(create_task.title)))
        db.commit()
        return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')


@router.put('/update')
async def update_task(user_id: int, db: DbSession, update_task: UpdateTask):
    user = db.scalar(select(Task).where(User.id == user_id))
    if user is not None:
        db.execute(update(Task).where(User.id == user_id).values(
            title=update_task.title,
            content=update_task.content,
            priority=update_task.priority))
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'Task update is successful!'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')


@router.delete('/delete')
async def delete_task(task_id: int, db: DbSession):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is not None:
        db.execute(delete(Task).where(Task.id == task_id))
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'Task delete is successful!'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')
