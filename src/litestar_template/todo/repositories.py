from sqlalchemy.ext.asyncio import AsyncSession

from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository

from litestar_template.todo.models import List, Note


class ListRepository(SQLAlchemyAsyncRepository[List]):
    model_type = List

    def __init__(self, session: AsyncSession):
        super().__init__(session=session)


class NoteRepository(SQLAlchemyAsyncRepository[Note]):
    model_type = Note


async def provide_list_repo(db_session: AsyncSession) -> ListRepository:
    return ListRepository(session=db_session)


async def provide_note_repo(db_session: AsyncSession) -> NoteRepository:
    return NoteRepository(session=db_session)
