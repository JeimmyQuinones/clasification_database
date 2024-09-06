from api.domain.repositories.scan_database_repository_interface import (
    ScanDatabaseRepositoryInterface,
)
from api.domain.repositories.type_data_repository_interface import (
    TypeDataRepositoryInterface,
)
from api.domain.repositories.user_repository_interface import UserRepositoryInterface
from api.infrastructure.repositories.scan_database.scan_database_repository_impl import (
    ScanDatabaseRepositoryImpl,
)
from api.infrastructure.repositories.type_data.type_data_repository_impl import (
    TypeDataRepositoryImpl,
)
from api.infrastructure.repositories.users.user_repository_impl import (
    UserRepositoryImpl,
)
from api.domain.repositories.database_repository_interface import (
    DatabaseRepositoryInterface,
)
from api.infrastructure.repositories.databasec.database_repository_impl import (
    DatabaseRepositoryImpl,
)


def get_user_domain() -> UserRepositoryInterface:
    return UserRepositoryImpl()


def get_database_domain() -> DatabaseRepositoryInterface:
    return DatabaseRepositoryImpl()


def get_type_data_domain() -> TypeDataRepositoryInterface:
    return TypeDataRepositoryImpl()


def get_scan_database_domain() -> ScanDatabaseRepositoryInterface:
    return ScanDatabaseRepositoryImpl()
