import uvicorn


def start():
    uvicorn.run("litestar_template.main.app:app", reload=True)
