from api.application.services.database_services.database_services_impl import (
    DatabaseServiceImpl,
)
from api.application.services.database_services.database_services_interface import (
    DatabaseServiceInterface,
)
from api.application.services.users_services.services_interface import (
    UserServiceInterface,
)
from api.application.services.users_services.user_service_impl import UserServiceImpl

from api.application.use_cases.Users.create_user_use_case import CreateUserUseCase
from api.application.services.login_services.login_service_interface import (
    LoginServiceInterface,
)
from api.application.services.login_services.login_service_impl import LoginServiceImpl

from api.application.use_cases.databasec.save_database_use_case import DatabaseUseCase
from api.application.use_cases.databasec.get_data_scan_use_case import (
    GetDataScanUseCase,
)
from api.application.use_cases.databasec.report_use_case import ReportScanUseCase
from api.application.use_cases.login.login_token_use_case import LoginTokenUseCase
from api.application.use_cases.databasec.scan_use_case import ScanUseCase


def get_user_service() -> UserServiceInterface:
    return UserServiceImpl(CreateUserUseCase())


def get_login_services() -> LoginServiceInterface:
    return LoginServiceImpl(LoginTokenUseCase())


def get_database_services() -> DatabaseServiceInterface:
    return DatabaseServiceImpl(
        DatabaseUseCase(), ScanUseCase(), GetDataScanUseCase(), ReportScanUseCase()
    )
