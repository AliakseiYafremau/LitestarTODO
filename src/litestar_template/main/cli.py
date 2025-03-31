import uvicorn


def start() -> None:
    """Start the development server."""
    uvicorn.run("litestar_template.main.app:app", reload=True)
