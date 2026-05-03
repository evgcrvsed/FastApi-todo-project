from fastapi import APIRouter, Depends, HTTPException, status, Query
from schemas.todo import TodoCreate, TodoUpdate, Todo, TodoRead
from models.todo import Todo as TodoModel
from repositories.todo import TodoRepository
from .dependencies import get_todo_repo

router = APIRouter(prefix="/todos", tags=["todos"])  # потом сделаем /api/v1


@router.get("/", response_model=list[Todo])
async def get_all_todos(
    completed: bool | None = Query(None),
    repo: TodoRepository = Depends(get_todo_repo),
):
    if completed is not None:
        return await repo.get_by_completed(completed)
    return await repo.get_all()


@router.post("/", response_model=TodoRead, status_code=201)
async def create_todo(
    todo_in: TodoCreate,
    repo: TodoRepository = Depends(get_todo_repo),
):
    todo = TodoModel(**todo_in.model_dump())
    created_todo = await repo.add(todo)
    return created_todo


@router.get("/{todo_id}", response_model=Todo)
async def get_todo(
    todo_id: int,
    repo: TodoRepository = Depends(get_todo_repo)
):
    todo = await repo.get_by_id(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: int,
    repo: TodoRepository = Depends(get_todo_repo)
):
    todo = await repo.get_by_id(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return await repo.delete(todo)


@router.put("/{todo_id}", response_model=Todo)
async def update_todo(
    todo_id: int,
    todo_update: TodoCreate,
    repo: TodoRepository = Depends(get_todo_repo)
):
    todo = await repo.get_by_id(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    update_data = todo_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo, key, value)

    return await repo.update(todo)


#
#
#
#
# @router.patch("/{todo_id}", response_model=Todo) # Хуйня какая-то, put лучше
# async def patch_todo(todo_id: int, todo_update: TodoUpdate):
#     if todo_id not in todos:
#         raise HTTPException(
#             status_code=404,
#             detail="Задача не найдена"
#         )
#
#     current = todos[todo_id]
#
#     update_data = todo_update.model_dump(exclude_unset=True)
#
#     updated_dict = {
#         **current.model_dump(),
#         **update_data
#     }
#
#     updated_todo = Todo(**updated_dict)
#
#     todos[todo_id] = updated_todo
#     return updated_todo
