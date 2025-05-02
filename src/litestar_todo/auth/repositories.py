from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository

from litestar_todo.auth.models import User


class UserRepository(SQLAlchemyAsyncRepository[User]):
    """Repository for User model."""

    model_type = User
