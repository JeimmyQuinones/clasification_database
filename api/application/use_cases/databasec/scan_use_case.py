from datetime import datetime
from typing import List, Optional
import uuid
from fastapi import HTTPException, status
from api.application.models.databasec.scan_model import (
    ScanDatabaseModel,
    TypeDataBaseModel,
)
from api.domain.entities.scan_table_info import (
    GetDomainInfoEntity,
    ScanDetailTableEntity,
    ScanDomainEntity,
    ScanEntiryList,
    ScanTableEntity,
)
from api.domain.repositories.database_repository_interface import (
    DatabaseRepositoryInterface,
)
from api.application.config.dependencies.domain_dependencies import (
    get_database_domain,
    get_type_data_domain,
    get_scan_database_domain,
)
from api.application.use_cases.encrypt.encrypt_use_case import EncryptUseCase
from api.application.models.databasec.save_model import SaveDatabaseModel
from api.domain.repositories.scan_database_repository_interface import (
    ScanDatabaseRepositoryInterface,
)
from api.domain.repositories.type_data_repository_interface import (
    TypeDataRepositoryInterface,
)


class ScanUseCase:

    dominio_database: DatabaseRepositoryInterface
    domion_type_data: TypeDataRepositoryInterface
    dominio_scan: ScanDatabaseRepositoryInterface

    def __init__(self) -> None:
        super().__init__()
        self.dominio_database = get_database_domain()
        self.domion_type_data = get_type_data_domain()
        self.dominio_scan = get_scan_database_domain()

    def scan_use_case(self, scan_data: ScanDatabaseModel) -> dict:
        """
        Realiza un escaneo de la base de datos basado en los datos proporcionados.
        actualiza la información del escaneo y guarda los resultados del análisis.
        """
        self._validate_input(scan_data)
        existing_entry = self.dominio_database.get_databasec_by_id(scan_data.id)
        if not existing_entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El id ingresado no existe.",
            )
        data_table = self._get_dataBase(existing_entry)
        type_data_list = self.domion_type_data.get_all_type_data()
        existing_entry.date_scan = datetime.now()
        existing_entry.lates_scan_version = (existing_entry.lates_scan_version or 0) + 1
        save_data_result = self._analyze_data(
            type_data_list, data_table, scan_data.id, existing_entry.lates_scan_version
        )
        self.dominio_database.Add_domain_scan_list(save_data_result.domain_list)
        self.dominio_database.Add_tables_scan_list(save_data_result.table_list)
        self.dominio_database.Add_tables_detail_scan_list(
            save_data_result.detail_table_list
        )
        self.dominio_database.Update_databasec(existing_entry)

    def _validate_input(self, scan_data: ScanDatabaseModel):
        """
        Valida que el campo `id` no esté vacío.
        """
        if not scan_data.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Todos los campos son requeridos",
            )

    def _get_dataBase(self, existing_entry):
        """
        Usa la información de conexión descifrada para conectarse a la base de datos y
        obtiene los detalles de las tablas.
        """
        data_decrypt = SaveDatabaseModel(
            username=EncryptUseCase.decrypt_text(existing_entry.username),
            password=EncryptUseCase.decrypt_text(existing_entry.password),
        )
        connection_string = f"mysql+pymysql://{data_decrypt.username}:{data_decrypt.password}@{existing_entry.host}:{existing_entry.port}"
        database = self.dominio_scan.get_info_by_database(connection_string)
        table_list: List[GetDomainInfoEntity] = []
        for baseinfo in database:
            if (
                baseinfo != "information_schema"
                and baseinfo != "performance_schema"
                and baseinfo != "mysql"
            ):
                tableInfo = self.dominio_scan.get_database_info(
                    connection_string, baseinfo
                )
                table_list.append(tableInfo)
        return table_list

    def _analyze_data(
        self,
        type_data_list: List[TypeDataBaseModel],
        data_table,
        database_id,
        last_version,
    ):
        """
        Analiza los datos de las tablas en función de los tipos de datos proporcionados.
        """
        type_list = self._transform_type_list(type_data_list)
        result_Scan = ScanEntiryList()
        for domain in data_table:
            domain_item = ScanDomainEntity(
                id=str(uuid.uuid4()),
                database_id=database_id,
                name=domain.nameDatabase,
                version=last_version,
            )
            result_Scan.domain_list.append(domain_item)
            for table in domain.table_list:
                table_item = ScanTableEntity(
                    id=str(uuid.uuid4()),
                    domain_id=domain_item.id,
                    name=table.name_table,
                )
                result_Scan.table_list.append(table_item)
                for colum in table.colum_list:
                    type = self._classify_column(type_list, colum)
                    table_detail_item = ScanDetailTableEntity(
                        id=str(uuid.uuid4()),
                        table_id=table_item.id,
                        nameColumn=colum,
                        typeIdentified_id=type,
                    )
                    result_Scan.detail_table_list.append(table_detail_item)
        return result_Scan

    def _classify_column(
        self, type_data_list: list[TypeDataBaseModel], name_colum: str
    ) -> Optional[str]:
        """
        Clasifica el tipo de una columna basada en una lista de tipos de datos y alias..
        """
        identified_type_id = None
        default_type = [item for item in type_data_list if item.name == "N/A"]
        if default_type:
            identified_type_id = default_type[0].id
        name = name_colum.upper()
        for type in type_data_list:
            for key in type.alias:
                if key.upper() in name and key != "":
                    identified_type_id = type.id
                    break
        return identified_type_id

    def _transform_type_list(self, type_data_list):
        """
        Convierte una lista de modelos de tipo de datos en una lista transformada,
        Los alias se dividen por comas y se limpian de espacios en blanco.
        """
        type_list: List[TypeDataBaseModel] = []
        for type_split in type_data_list:
            type = TypeDataBaseModel(
                id=type_split.id,
                name=type_split.name,
                alias=[item.strip() for item in type_split.alias.split(",")],
            )
            type_list.append(type)
        return type_list
