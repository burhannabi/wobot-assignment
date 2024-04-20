from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter, Depends, status

from ...core.database import get_db
from ...core.dependencies import get_current_user
from ...core.models import Todo
from ...api.schemas.task import TaskIn, TaskOut, TaskUpdate
from ...api.schemas.auth import UserIn
from ...misc.helpers import InternalServerError, TaskNotFound

router = APIRouter(prefix="/task", tags=["Tasks"])


@router.get("/fetch", status_code=status.HTTP_200_OK, operation_id="fetch-tasks", response_model=List[TaskOut])
async def get_all_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserIn = Depends(get_current_user),
) -> List[TaskOut]:
    """
    Retrieve all tasks by current user.
    """

    try:
        tasks = db.query(Todo).filter_by(owner_id=current_user.id).offset(skip).limit(limit).all()
        if not tasks:
            raise TaskNotFound()
        return tasks
    except SQLAlchemyError as e:
        db.rollback()
        raise InternalServerError(e)


@router.get("/{task_id}", status_code=status.HTTP_200_OK, operation_id="fetch-task", response_model=TaskOut)
async def get_single_task(task_id: int, current_user: UserIn = Depends(get_current_user), db: Session = Depends(get_db)) -> TaskOut:
    """
    Retrieve a task by `task_id`.
    """
    try:
        task = db.query(Todo).filter(Todo.id==task_id, Todo.owner_id==current_user.id).first()
        
        if not task:
            raise TaskNotFound()

        return task
    except SQLAlchemyError as e:
        db.rollback()
        raise InternalServerError(e)


@router.post("/create", status_code=status.HTTP_201_CREATED, operation_id="create-task", response_model=TaskOut)
async def create_task(
    task: TaskIn,
    db: Session = Depends(get_db),
    current_user: UserIn = Depends(get_current_user),
) -> TaskOut:
    """
    Create a new todo task.
    """
    try:
        new_task = Todo(**task.model_dump(), owner_id=current_user.id)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task
    except SQLAlchemyError as e:
        db.rollback()
        raise InternalServerError(e)


@router.put("/{task_id}", status_code=status.HTTP_202_ACCEPTED, operation_id="update-task", response_model=TaskOut)
async def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: UserIn = Depends(get_current_user),
) -> TaskOut:
    """
    Update a task by `task_id`.
    """
    try:
        update_task = db.query(Todo).filter(Todo.id==task_id, Todo.owner_id==current_user.id).first()

        if not update_task:
            raise TaskNotFound()
        
        for field, value in task.model_dump(exclude_unset=True).items():
            setattr(update_task, field, value)

        db.commit()
        db.refresh(update_task)
        return update_task
    
    except SQLAlchemyError as e:
        db.rollback()
        raise InternalServerError(e)


@router.delete("/{task_id}", status_code=status.HTTP_202_ACCEPTED, operation_id="delete-task", response_model=TaskOut)
async def delete_task(
    task_id: int,
    current_user: UserIn = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TaskOut:
    """
    Delete a task by `task_id`.
    """
    try:
        delete_task = db.query(Todo).filter(Todo.id==task_id, Todo.owner_id==current_user.id).first()

        if not delete_task:
            raise TaskNotFound()
        
        db.delete(delete_task)
        db.commit()
        return delete_task

    except SQLAlchemyError as e:
        db.rollback()
        raise InternalServerError(e)


@router.delete("", status_code=status.HTTP_202_ACCEPTED, operation_id="delete-all", response_model=List[TaskOut])
async def delete_all_tasks(
    current_user: UserIn = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[TaskOut]:
    """
    Delete all tasks by current user.
    """
    try:
        delete_tasks = db.query(Todo).filter_by(owner_id=current_user.id).all()

        if not delete_tasks:
            raise TaskNotFound()
        
        for task in delete_tasks:
            db.delete(task)
        
        db.commit()
        return delete_tasks

    except SQLAlchemyError as e:
        db.rollback()
        raise InternalServerError(e)

