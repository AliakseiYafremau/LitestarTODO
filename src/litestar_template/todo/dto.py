import msgspec

from uuid import UUID

from litestar.dto import MsgspecDTO, DTOConfig


class List(msgspec.Struct):
    id: UUID
    title: str


class Note(msgspec.Struct):
    id: UUID
    text: str
    list_id: UUID


class ListReadDTO(MsgspecDTO[List]):
    config = DTOConfig()


class NoteReadDTO(MsgspecDTO[Note]):
    config = DTOConfig()
