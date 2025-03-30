from sqlalchemy.ext.asyncio import AsyncSession

from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository

from litestar_template.todo.models import List, Note


class ListRepository(SQLAlchemyAsyncRepository[List]):
    model_type = List


class NoteRepository(SQLAlchemyAsyncRepository[Note]):
    model_type = Note


async def provide_list_repo(db_session: AsyncSession) -> ListRepository:
    return ListRepository(session=db_session)