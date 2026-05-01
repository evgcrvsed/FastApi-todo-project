from fastapi import APIRouter, HTTPException, status, Query
from schemas import TodoCreate, TodoUpdate, Todo
from models import todos, next_id
from datetime import datetime

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("/", response_model=list[Todo])
async def get_all_todos(
    completed: bool | None = Query(None, description="Фильтр по статусу"),
):
    result = list(todos.values())

    if completed is not None:
        result = [todo for todo in result if todo.completed == completed]

    return result


@router.post("/", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate):
    global next_id
    new_todo = Todo(
        id=next_id,
        **todo.model_dump(),
        created_at=datetime.now()
    )
    todos[next_id] = new_todo
    next_id += 1
    return new_todo


@router.get("/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos[todo_id]


@router.put("/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo_update: TodoCreate):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")

    updated_todo = Todo(
        id=todo_id,
        **todo_update.model_dump(),
        created_at=todos[todo_id].created_at
    )
    todos[todo_id] = updated_todo
    return updated_todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos[todo_id]


@router.patch("/{todo_id}", response_model=Todo) # Хуйня какая-то, put лучше
async def patch_todo(todo_id: int, todo_update: TodoUpdate):
    if todo_id not in todos:
        raise HTTPException(
            status_code=404,
            detail="Задача не найдена"
        )

    current = todos[todo_id]

    update_data = todo_update.model_dump(exclude_unset=True)

    updated_dict = {
        **current.model_dump(),
        **update_data
    }

    updated_todo = Todo(**updated_dict)

    todos[todo_id] = updated_todo
    return updated_todo