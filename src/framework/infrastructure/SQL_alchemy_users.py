from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound
from bcrypt import gensalt, hashpw

from framework.domain.repositories import (
    IUsersSQLAlchemyRepository,
    EntityCollisionException,
    EntityUIDNotFoundException,
)
from framework.domain.value_object import UUID
from framework.infrastructure.db_management.db_mapping import (
    map_from_to,
    parse_filters,
    filter_instance_from_db,
)
from framework.infrastructure.db_management.db_structure import (
    UserInstance,
    AttrsUserInstance,
)
from framework.domain.users import User, AttrsUser


class SQLAlchemyUser(IUsersSQLAlchemyRepository):
    def __init__(self, session):
        self._session: Session = session

    def user_to_db_object(self, user: User) -> UserInstance:
        mapped_vol_data = map_from_to(
            user, AttrsUser, AttrsUserInstance, ["password", "salt"]
        )

        return UserInstance(**mapped_vol_data)

    def _db_object_to_user(self, user_instance: UserInstance) -> User:
        mapped_vol_data = map_from_to(
            user_instance, AttrsUserInstance, AttrsUser, ["password", "salt"]
        )

        return User(**mapped_vol_data)

    def _add(self, user: User, password: str):
        filters = parse_filters(UserInstance, filters_eq={"email": user.email})
        users = filter_instance_from_db(self._session, UserInstance, filters)

        if len(users) <= 0:
            user_intance = self.user_to_db_object(user)
            salt: bytes = gensalt()
            enc_password: bytes = hashpw(password.encode(), salt)
            user_intance.salt = salt
            user_intance.password = enc_password

            self._session.add(user_intance)
            self._session.commit()
        else:
            raise EntityCollisionException(user.email)

    def _get_by_uid(self, ref: UUID) -> User:
        query_filter = [UserInstance.uid == ref]

        try:
            user_instance: UserInstance = (
                self._session.query(UserInstance).filter(*query_filter).one()
            )

        except NoResultFound:
            raise EntityUIDNotFoundException(ref)

        user: User = self._db_object_to_user(user_instance)

        return user

    def _get(self, **kwargs):
        email = kwargs.get("email", None)
        password = kwargs.get("password", None)
        users = []

        if not email is None and not password is None:
            filters = parse_filters(UserInstance, filters_eq={"email": email})
            users_instances = filter_instance_from_db(
                self._session, UserInstance, filters
            )

            if len(users_instances) <= 0:
                return users

            user_instance: UserInstance = users_instances[0]
            salt: bytes = user_instance.salt
            hashed_password = hashpw(password.encode(), salt)

            if hashed_password == user_instance.password:
                users.append(self._db_object_to_user(user_instance))

        else:
            filters = parse_filters(UserInstance, **kwargs)
            user_instances = filter_instance_from_db(
                self._session, UserInstance, filters
            )
            users = [self._db_object_to_user(instance) for instance in user_instances]

        return users
