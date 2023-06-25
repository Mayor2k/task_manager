import uvicorn
from fastapi import FastAPI, Depends, status, HTTPException
import models, schemas
from crud import UserCrud, TaskCrud
from database import engine
from typing import List
from utils import Validator
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        #create tables if not exist on startup
        await conn.run_sync(models.Base.metadata.create_all)
        
@app.get("/api/users/", response_model=List[schemas.User], tags=['Users'])
async def get_users(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_async_session)):
    return await UserCrud(session).get_models(skip=skip, limit=limit)

@app.get("/api/users/{user_id}", response_model=schemas.User, tags=['Users'])
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_async_session)):
    db_user = await UserCrud(session).get_model(model_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
        
@app.delete("/api/users/{user_id}", tags=['Users'])
async def delete_user_by_id(user_id: int, session: AsyncSession = Depends(get_async_session)):
    response = await UserCrud(session).delete_model(user_id)
    
    if not response:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"details":"ok"}
        
@app.put("/api/users/{user_id}", response_model=schemas.User, tags=['Users'])
async def update_user_by_id(user_id: int, user: schemas.UserBase, session: AsyncSession = Depends(get_async_session)):
    if user.email != None and not Validator.is_accepted_email(user.email):
        raise HTTPException(status_code=400, detail="Email isn't valid!")
    
    response = await UserCrud(session).update_model(user_id, user)
    
    if not response:
        raise HTTPException(status_code=404, detail="User not found")
    
    return response

@app.post("/api/users/", status_code=status.HTTP_201_CREATED, tags=['Users'])
async def create_user(user: schemas.UserCreate, session: AsyncSession = Depends(get_async_session)):            
    if not Validator.is_accepted_email(user.email):
        raise HTTPException(status_code=400, detail="Email isn't valid!")

    crud = UserCrud(session)
    db_user = await crud.get_model_by_email(email=user.email)
    
    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    if not Validator.is_accepted_password(user.password):
        raise HTTPException(status_code=400, detail="Password must be > 6 characters and contain at least 1 number!")
    
    return await crud.create_model(data=user)

@app.get("/api/tasks/", response_model=List[schemas.Task], tags=['Tasks'])
async def get_tasks(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_async_session)):
    return await TaskCrud(session).get_models(skip=skip, limit=limit)

@app.get("/api/tasks/{task_id}", response_model=schemas.Task, tags=['Tasks'])
async def get_task_by_id(task_id: int, session: AsyncSession = Depends(get_async_session)):
    db_task = await TaskCrud(session).get_model(model_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task
        
@app.delete("/api/tasks/{task_id}", tags=['Tasks'])
async def delete_task_by_id(task_id: int, session: AsyncSession = Depends(get_async_session)):
    response = await TaskCrud(session).delete_model(task_id)
    
    if not response:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"details":"ok"}
        
@app.put("/api/tasks/{task_id}", response_model=schemas.Task, tags=['Tasks'])
async def update_task_by_id(task_id: int, task: schemas.TaskBase, session: AsyncSession = Depends(get_async_session)):
    response = await TaskCrud(session).update_model(task_id, task)
    
    if not response:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return response
        
@app.post("/api/tasks/", response_model=schemas.Task, status_code=status.HTTP_201_CREATED, tags=['Tasks'])
async def create_task(task: schemas.TaskBase, session: AsyncSession = Depends(get_async_session)):
    db_user = await UserCrud(session).get_model(model_id=task.user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User is not exist")
    return await TaskCrud(session).create_model(data=task)


if __name__ == "__main__":
    uvicorn.run("main:app", port = 8000, host = "127.0.0.1", reload = True)