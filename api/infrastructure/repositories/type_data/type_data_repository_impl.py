from typing import List
from sqlalchemy.orm import Session
from api.domain.entities.type_data import TypeDataEntity
from api.domain.repositories.type_data_repository_interface import (
    TypeDataRepositoryInterface,
)
from api.infrastructure.database.connector import get_db_connection
from api.infrastructure.database.models.types_identified_data_db_model import (
    TypeIdentifiedDataDBModel,
)


class TypeDataRepositoryImpl(TypeDataRepositoryInterface):
    def get_all_type_data(self) -> None:
        session: Session = next(get_db_connection())
        db_user = session.query(TypeIdentifiedDataDBModel).all()
        session.close()
        if db_user is None:
            return None
        type_list: List[TypeDataEntity] = []
        for item in db_user:
            data = TypeDataEntity(id=item.id, name=item.name, alias=item.alias)
            type_list.append(data)
        return type_list
