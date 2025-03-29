from litestar import get, Request


from litestar_template.main.logging import get_logger


logger = get_logger(__name__)


@get("/")
async def hello_world(request: Request) -> dict[str, str]:
    logger.info("Start hello_world")
    return {"message": "Hello, world!"}
