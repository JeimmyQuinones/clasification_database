from fastapi import APIRouter, Depends, HTTPException, Response, status
from api.application.config.auth import CurrentUser
from api.application.models.databasec.save_model import SaveDatabaseModel
from api.application.models.databasec.scan_model import ScanDatabaseModel
from api.application.services.database_services.database_services_interface import (
    DatabaseServiceInterface,
)
from api.application.config.dependencies.aplication_dependencies import (
    get_database_services,
)

router = APIRouter()


@router.post("/save")
def save_database(
    user_request: SaveDatabaseModel,
    current_user: CurrentUser,
    database_service: DatabaseServiceInterface = Depends(get_database_services),
):
    """
    Guarda la información de la base de datos asociandola a un usuario autenticado.

    Args:
        user_request (SaveDatabaseModel): Modelo que contiene los datos de la base de datos que se desean guardar.
        current_user (CurrentUser): Información del usuario autenticado que realiza la solicitud, utilizada para asociar los datos a dicho usuario.
        database_service (DatabaseServiceInterface): Dependencia inyectada que maneja la lógica de negocio para guardar los datos en la base de datos.

    Returns:
        Response: Respuesta HTTP con el código de estado 201 (CREATED) si la operación es exitosa.

    Raises:
        HTTPException: Excepciones personalizadas en caso de error durante el procesamiento de la solicitud, con códigos de error específicos.
    """
    try:
        response = database_service.Save_database_info(user_request, current_user.id)
        return Response(response, status.HTTP_201_CREATED)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )


@router.post("/scan")
def save_scan_database_by_id(
    scan_data: ScanDatabaseModel,
    current_user: CurrentUser,
    database_service: DatabaseServiceInterface = Depends(get_database_services),
):
    """
    Escanea una base de datos específica por su ID.

    Args:
        scan_data (ScanDatabaseModel): Modelo que contiene la información necesaria para escanear la base de datos, como el ID de la base.
        current_user (CurrentUser): Información del usuario autenticado que solicita el escaneo, para asegurar que tiene permisos adecuados.
        database_service (DatabaseServiceInterface): Dependencia inyectada que contiene la lógica de negocio para realizar el escaneo de la base de datos.

    Returns:
        Response: Respuesta HTTP con el código de estado 201 (CREATED) si el escaneo se inicia correctamente.

    Raises:
        HTTPException: Excepciones específicas capturadas durante el proceso de escaneo, con mensajes personalizados.
    """
    try:
        database_service.scan_database_by_id(scan_data)
        return Response(None, status.HTTP_201_CREATED)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )


@router.get("/GetScan")
def scan_database_by_id(
    id: str,
    current_user: CurrentUser,
    database_service: DatabaseServiceInterface = Depends(get_database_services),
):
    """
    Obtiene los resultados de un escaneo de base de datos específico por su ID.

    Args:
        id (str): El identificador único de la base de datos cuyo escaneo se desea recuperar.
        current_user (CurrentUser): Información del usuario autenticado que solicita los datos, para asegurar que tiene permisos adecuados.
        database_service (DatabaseServiceInterface): Dependencia inyectada que contiene la lógica de negocio para recuperar los resultados del escaneo de la base de datos.

    Returns:
        dict: Un modelo con los datos del escaneo de la base de datos especificada.

    Raises:
        HTTPException: Excepciones específicas capturadas durante el proceso de obtención de datos, con mensajes personalizados.
        HTTPException: Excepción genérica con código 500 si ocurre un error inesperado durante el proceso.
    """
    try:
        data_result = database_service.get_scan_database_by_id(id)
        return data_result
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )


@router.get("/ReportScan")
def report_scan_database_by_id(
    id: str,
    current_user: CurrentUser,
    database_service: DatabaseServiceInterface = Depends(get_database_services),
):
    """
    Genera un informe del escaneo de base de datos específico por su ID.

    Args:
        id (str): El identificador único de la base de datos cuyo informe de escaneo se desea generar.
        current_user (CurrentUser): Información del usuario autenticado que solicita el informe, para validar los permisos adecuados.
        database_service (DatabaseServiceInterface): Dependencia inyectada que contiene la lógica de negocio para generar el informe de escaneo de la base de datos.

    Returns:
        dict: Un modelo con los datos del informe de escaneo de la base de datos especificada.

    Raises:
        HTTPException: Se lanza si ocurre un error conocido relacionado con el proceso del informe.
        HTTPException: Se lanza una excepción con código 500 si ocurre un error inesperado durante el proceso.
    """
    try:
        data_result = database_service.report_scan_database_by_id(id)
        return data_result
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )
