import uvicorn


def start() -> None:
    """Start the development server."""
    uvicorn.run("litestar_todo.main.app:app", reload=True)
