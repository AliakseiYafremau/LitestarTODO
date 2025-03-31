from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy.ext.asyncio import AsyncSession

from litestar_todo.todo.models import List, Note


class ListRepository(SQLAlchemyAsyncRepository[List]):
    """Repository for List model."""

    model_type = List


class NoteRepository(SQLAlchemyAsyncRepository[Note]):
    """Repository for Note model."""

    model_type = Note


async def provide_list_repo(db_session: AsyncSession) -> ListRepository:
    """Dependency provider for ListRepository.

    Args:
        db_session: AsyncSession for database operations.

    Returns:
        An instance of ListRepository configured with a ListRepository.

    """
    return ListRepository(session=db_session)
