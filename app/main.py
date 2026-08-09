from fastapi import FastAPI

from app.routes import auth_router

app = FastAPI(
    title="Task Manager API",
    description="A production-ready REST API for managing tasks with user authentication.",
    version="1.0.0",
)

app.include_router(auth_router)


@app.get("/")
async def root():
    """
    Root endpoint to verify the API is running.

    Returns:
        A welcome message confirming the API is operational.
    """
    return {"message": "Task Manager API is running"}
