from litestar import get


@get("/")
async def hello_world() -> dict[str, str]:
    return {"message": "Hello, worl!"}