from uuid import UUID

from litestar.controller import Controller
from litestar.handlers.http_handlers.decorators import get, post, delete
from litestar.di import Provide

from litestar_template.todo.models import List
from litestar_template.todo.dto import ListReadDTO, ListCreateScheme
from litestar_template.todo.servicies import provide_list_service, ListService

class ListController(Controller):
    path = "/list"
    dependencies = {"list_service": Provide(provide_list_service)}

    @get()
    async def list_list(self, list_id: UUID, list_service: ListService) -> list[ListReadDTO]:
        return await list_service.get_by_id(list_id=list_id)

    @get("/all")
    async def list_lists(self, list_service: ListService) -> list[ListReadDTO]:
        return await list_service.get_all()
    
    @post()
    async def create_list(self, data: ListCreateScheme, list_service: ListService) -> ListReadDTO:
        return await list_service.create(title=data.title)
    
    @delete("/{list_id:uuid}")
    async def delete_list(self, list_id: UUID, list_service: ListService) -> None:
        await list_service.delete(list_id=list_id)
        return None