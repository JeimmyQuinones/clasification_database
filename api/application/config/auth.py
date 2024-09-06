from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from api.application.config.config import settings
from api.application.models.login.auth_token import AuthToken
from api.domain.entities import User
from api.application.use_cases.Users.validate_user_use_case import ValidateUserUseCase

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/Accestokenswaguer"
)

TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(
    token: str = Depends(reusable_oauth2), validate: ValidateUserUseCase = Depends()
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = AuthToken(**payload)
        if token_data.sub is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        return validate.validate_user_case(token_data.sub)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )


CurrentUser = Annotated[User, Depends(get_current_user)]
