from sqlalchemy.orm import Session
from api.domain.repositories.user_repository_interface import UserRepositoryInterface
from api.infrastructure.database.connector import get_db_connection
from api.infrastructure.database.models.user_db_model import UserDBModel
from api.domain.entities.User import UserEntity


class UserRepositoryImpl(UserRepositoryInterface):
    def create_user(self, user: UserEntity) -> None:
        session: Session = next(get_db_connection())
        db_user = UserDBModel(username=user.username, password=user.password)
        session.add(db_user)
        session.commit()
        session.close()

    def get_user_by_username(self, username: str) -> None:
        session: Session = next(get_db_connection())
        db_user = (
            session.query(UserDBModel).filter(UserDBModel.username == username).first()
        )
        session.close()
        if db_user is None:
            return None
        return UserEntity(
            id=db_user.id, username=db_user.username, password=db_user.password
        )

    def get_user_by_id(self, id: int) -> None:
        session: Session = next(get_db_connection())
        db_user = session.query(UserDBModel).filter(UserDBModel.id == id).first()
        session.close()
        if db_user is None:
            return None
        return UserEntity(
            id=db_user.id, username=db_user.username, password=db_user.password
        )
