from fastapi import APIRouter, Depends, HTTPException, status, Query
from schemas.todo import TodoCreate, TodoUpdate, Todo, TodoRead
from models.todo import Todo as TodoModel
from .dependencies import get_todo_repo, CurrentUser
from repositories.todo import TodoRepository
from models.user import User

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("/", response_model=list[Todo])
async def get_all_todos(
    completed: bool | None = Query(None),
    current_user: User = CurrentUser,
    repo: TodoRepository = Depends(get_todo_repo),
):
    return await repo.get_all_by_owner(current_user.id)


@router.post("/", response_model=TodoRead, status_code=201)
async def create_todo(
    todo_in: TodoCreate,
    current_user: User = CurrentUser,
    repo: TodoRepository = Depends(get_todo_repo),
):
    todo = TodoModel(**todo_in.model_dump(), owner_id=current_user.id)
    created_todo = await repo.add(todo)
    return created_todo


@router.get("/{todo_id}", response_model=Todo)
async def get_todo(
    todo_id: int,
    current_user: User = CurrentUser,
    repo: TodoRepository = Depends(get_todo_repo),
):
    todo = await repo.get_by_id(todo_id)
    if todo is None or todo.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: int,
    current_user: User = CurrentUser,
    repo: TodoRepository = Depends(get_todo_repo),
):
    todo = await repo.get_by_id(todo_id)
    if todo is None or todo.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")
    return await repo.delete(todo)


@router.put("/{todo_id}", response_model=Todo)
async def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,          # было TodoCreate — исправил на Update
    current_user: User = CurrentUser,
    repo: TodoRepository = Depends(get_todo_repo),
):
    todo = await repo.get_by_id(todo_id)
    if todo is None or todo.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")

    update_data = todo_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo, key, value)

    return await repo.update(todo)