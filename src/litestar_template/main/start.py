from litestar import Litestar
from litestar_template.routers.base_router import hello_world


def create_app():
    app = Litestar(
        route_handlers=[
            hello_world,
        ]
    )
    return app


app = create_app()
