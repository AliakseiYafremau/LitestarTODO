from litestar import Litestar, Router
from litestar.di import Provide
from litestar.plugins.sqlalchemy import SQLAlchemyPlugin

from litestar_template.core.database import sqlalchemy_config
from litestar_template.todo.controllers import ListController


def create_app():
    app = Litestar(
        route_handlers=[Router(path="", route_handlers=[ListController])],
        debug=True,
        dependencies={
            "db_session": Provide(
                sqlalchemy_config.provide_session, sync_to_thread=True
            )
        },
        plugins=[SQLAlchemyPlugin(config=sqlalchemy_config)],
    )
    return app


app = create_app()
