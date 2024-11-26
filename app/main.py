from fastapi import FastAPI
from routers import user, task

app = FastAPI()

app.include_router(user.router)
app.include_router(task.router)

@app.get('/')
async def welcome():
    return {'message': 'Welcome to Taskmanager'}
