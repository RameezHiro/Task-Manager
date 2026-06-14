from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import auth, tasks

app = FastAPI()

app.include_router(auth.router)
app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "Task Manager API is running"}

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/health")
def health():
    return {"status": "ok"}