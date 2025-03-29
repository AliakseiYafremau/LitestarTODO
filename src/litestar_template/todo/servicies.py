from litestar_template.todo.models import List
from litestar_template.todo.repositories import ListRepository
from litestar_template.todo.dto import ListReadDTO
from litestar_template.core.database import provide_session


class ListService:
    def __init__(self, list_repo: ListRepository):
        self.list_repo = list_repo
    
    async def get_by_id(self, list_id: int) -> List:
        db_list = await self.list_repo.get(list_id)
        if db_list:
            return ListReadDTO(id=db_list.id, title=db_list.title)
        return None
    
    async def get_all(self) -> list[List]:
        db_lists = await self.list_repo.list()
        if db_lists:
            lists = []
            for list in db_lists:
                lists.append(list)
            return lists
        return None


async def provide_list_service() -> ListService:
    return ListService(ListRepository(provide_session()))