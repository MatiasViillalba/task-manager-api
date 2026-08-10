import logging
import time

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.config import configure_logging
from app.exceptions import TaskManagerException
from app.routes import auth_router, tasks_router

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Task Manager API",
    description="A production-ready REST API for managing tasks with user authentication.",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(tasks_router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Log every incoming request and its processing time.

    Args:
        request: The incoming HTTP request.
        call_next: The next handler in the middleware chain.

    Returns:
        The HTTP response, unmodified.
    """
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.3f}s"
    )

    return response


@app.exception_handler(TaskManagerException)
async def task_manager_exception_handler(request: Request, exc: TaskManagerException):
    """
    Handle any custom application exception that was not caught explicitly.

    Args:
        request: The incoming HTTP request.
        exc: The raised custom exception.

    Returns:
        A JSON response with a 400 status code and the error message.
    """
    logger.warning(f"Application error on {request.url.path}: {exc.message}")

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"detail": exc.message}
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """
    Handle any unexpected exception that was not caught elsewhere.

    Args:
        request: The incoming HTTP request.
        exc: The unexpected exception.

    Returns:
        A JSON response with a 500 status code and a generic error message.
    """
    logger.error(f"Unexpected error on {request.url.path}: {exc!s}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred. Please try again later."},
    )


@app.get("/")
async def root():
    """
    Root endpoint to verify the API is running.

    Returns:
        A welcome message confirming the API is operational.
    """
    return {"message": "Task Manager API is running"}
