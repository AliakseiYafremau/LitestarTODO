from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy.ext.asyncio import AsyncSession

from litestar_todo.auth.models import User


class UserRepository(SQLAlchemyAsyncRepository[User]):
    """Repository for User model."""

    model_type = User


async def provide_user_repo(db_session: AsyncSession) -> UserRepository:
    """Dependency provider for UserRepository.

    Args:
        db_session: AsyncSession for database operations.

    Returns:
        An instance of UserRepository configured with a User model.

    """
    return UserRepository(session=db_session)
