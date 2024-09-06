from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from api.application.services.login_services.login_service_interface import (
    LoginServiceInterface,
)
from api.application.config.dependencies.aplication_dependencies import (
    get_login_services,
)
from api.application.models.users.user_create_model import UserCreate
from api.application.models.login.token_model import Token

router = APIRouter()


@router.post("/Accestokenswaguer", response_model=Token)
def login_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    login_service: LoginServiceInterface = Depends(get_login_services),
):
    """
    Genera un token de acceso mediante autenticación con credenciales de usuario este endpoint se creo para facilitar el uso de swagger.

    Args:
        form_data (OAuth2PasswordRequestForm): Datos del formulario que contienen el nombre de usuario y contraseña enviados por el cliente.
        login_service (LoginServiceInterface): Dependencia inyectada que maneja la lógica de autenticación y generación de tokens.

    Returns:
        Token: Objeto que contiene el token de acceso generado si la autenticación es exitosa.

    Raises:
        HTTPException: Si ocurre un error de autenticación, se devuelve un código 404 con un mensaje de error detallado.
        HTTPException: Si ocurre un error inesperado, se lanza una excepción con código 500 y un mensaje explicando el problema.
    """
    try:
        user_request = UserCreate(
            username=form_data.username, password=form_data.password
        )
        response = login_service.login_token(user_request)
        if isinstance(response, Token):
            return response
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=response)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )


@router.post("/Accestoken", response_model=Token)
def login_token(
    user_request: UserCreate,
    login_service: LoginServiceInterface = Depends(get_login_services),
):
    """
    Genera un token de acceso mediante autenticación con credenciales de usuario.

    Args:
        form_data (OAuth2PasswordRequestForm): Datos del formulario que contienen el nombre de usuario y contraseña enviados por el cliente.
        login_service (LoginServiceInterface): Dependencia inyectada que maneja la lógica de autenticación y generación de tokens.

    Returns:
        Token: Objeto que contiene el token de acceso generado si la autenticación es exitosa.

    Raises:
        HTTPException: Si ocurre un error de autenticación, se devuelve un código 404 con un mensaje de error detallado.
        HTTPException: Si ocurre un error inesperado, se lanza una excepción con código 500 y un mensaje explicando el problema.
    """
    try:
        response = login_service.login_token(user_request)
        if isinstance(response, Token):
            return response
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=response)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )
