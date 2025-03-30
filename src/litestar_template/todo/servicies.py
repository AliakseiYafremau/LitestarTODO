from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from litestar_template.todo.dto import ListScheme
from litestar_template.todo.models import List
from litestar_template.todo.repositories import ListRepository
from litestar_template.todo.dto import ListReadDTO


class ListService:
    def __init__(self, list_repo: ListRepository):
        self.list_repo = list_repo

    async def get_by_id(self, list_id: UUID) -> ListReadDTO | None:
        exist = await self.list_repo.exists(id=list_id)
        if not exist:
            return None
        db_list = await self.list_repo.get(item_id=list_id)
        return ListScheme(id=db_list.id, title=db_list.title)

    async def get_all(self) -> list[ListReadDTO]:
        db_lists = await self.list_repo.list()
        if db_lists:
            lists = []
            for list in db_lists:
                lists.append(ListScheme(id=list.id, title=list.title))
            return lists
        return []

    async def create(self, title: str) -> ListReadDTO:
        db_list = await self.list_repo.add(data=List(title=title), auto_commit=True)
        return ListScheme(id=db_list.id, title=db_list.title)

    async def delete(self, list_id: UUID) -> ListReadDTO:
        db_list = await self.list_repo.delete(item_id=list_id, auto_commit=True)
        return ListScheme(id=db_list.id, title=db_list.title)


async def provide_list_service(db_session: AsyncSession) -> ListService:
    return ListService(ListRepository(session=db_session))
