from litestar import Litestar, Router
from litestar.di import Provide
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin
from litestar.plugins.sqlalchemy import SQLAlchemyPlugin

from litestar_todo.core.database import sqlalchemy_config
from litestar_todo.todo.controllers import NoteController


def create_app() -> Litestar:
    """Create the Litestar application."""
    return Litestar(
        route_handlers=[
            Router(path="", route_handlers=[NoteController]),
        ],
        openapi_config=OpenAPIConfig(
            title="Litestar TODO",
            version="1.0.0",
            description="Litestar TODO",
            path="/docs",
            render_plugins=[SwaggerRenderPlugin()],
        ),
        debug=True,
        dependencies={
            "db_session": Provide(
                sqlalchemy_config.provide_session, sync_to_thread=True,
            )
        },
        plugins=[SQLAlchemyPlugin(config=sqlalchemy_config)],
    )


app = create_app()
