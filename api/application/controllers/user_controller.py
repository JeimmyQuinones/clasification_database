from fastapi import APIRouter, Depends, HTTPException, Response, status

from api.application.services.users_services.services_interface import (
    UserServiceInterface,
)
from api.application.config.dependencies.aplication_dependencies import get_user_service
from api.application.models.users.user_create_model import UserCreate

router = APIRouter()


@router.post("/createuser")
def create_user(
    user_request: UserCreate,
    user_service: UserServiceInterface = Depends(get_user_service),
):
    """
    Crea un nuevo usuario en el sistema.

    Args:
        user_request (UserCreate): Objeto que contiene la información del usuario a crear, como el nombre de usuario y contraseña.
        user_service (UserServiceInterface): Dependencia inyectada que maneja la lógica de creación de usuarios.

    Returns:
        Response: Mensaje confirmando que el usuario ha sido creado exitosamente con un código de estado 201.

    Raises:
        HTTPException: Si el usuario ya existe, se lanza una excepción con un código de estado 404 y un mensaje detallado.
        HTTPException: Si ocurre un error inesperado, se lanza una excepción con un código 500 y un mensaje describiendo el problema.
    """
    try:
        response = user_service.create_user(user_request)
        if False is response:
            raise HTTPException(status_code=404, detail="El usuario ya existe.")
        return Response(
            "Usuario creado de manera satisfactoria", status.HTTP_201_CREATED
        )
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )
