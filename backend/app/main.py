from fastapi import FastAPI
from app.routers import users

app = FastAPI(title="fastAPI_project_template")

app.include_router(users.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to fastAPI_project_template API"}