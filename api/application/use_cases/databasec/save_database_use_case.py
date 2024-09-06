import uuid
from fastapi import HTTPException, status
from api.domain.entities.databaseC import DatabaseEntity
from api.domain.repositories.database_repository_interface import (
    DatabaseRepositoryInterface,
)
from api.application.config.dependencies.domain_dependencies import get_database_domain
from api.application.use_cases.encrypt.encrypt_use_case import EncryptUseCase
from api.application.models.databasec.save_model import SaveDatabaseModel


class DatabaseUseCase:

    dominio: DatabaseRepositoryInterface

    def __init__(self) -> None:
        super().__init__()
        self.dominio = get_database_domain()

    def save_data_use_case(
        self, database_request: SaveDatabaseModel, user_id: int
    ) -> dict:
        """
        Guarda la información de una base de datos en el sistema, validando y cifrando la informacion sensible.
        """
        self._validate_data(database_request)
        data_encrypt = DatabaseEntity(
            id=uuid.uuid4(),
            user_id=user_id,
            host=database_request.host,
            port=database_request.port,
            username=EncryptUseCase.encrypt_text(database_request.username),
            password=EncryptUseCase.encrypt_text(database_request.password),
        )

        existing_entry = self.dominio.get_databasec_by_host_port(
            database_request.host, database_request.port
        )
        if existing_entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La base de datos ya existe.",
            )

        self.dominio.create_databasec(data_encrypt)
        return str(data_encrypt.id)

    def _validate_data(selfe, database_request: SaveDatabaseModel):
        """
        Valida los datos del modelo de entrada asegurando que
        todos los campos requeridos estén presentes.
        """
        if not all(
            [
                database_request.password,
                database_request.username,
                database_request.port,
                database_request.host,
            ]
        ):
            raise HTTPException(
                status_code=400, detail="Todos los campos son requeridos"
            )
