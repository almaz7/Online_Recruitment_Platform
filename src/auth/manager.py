from typing import Optional, Union

from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models, schemas

from auth.models import User
from auth.utils import get_user_db

from config import SECRET_AUTH


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET_AUTH
    verification_token_secret = SECRET_AUTH

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.username} has registered.")

    async def on_after_login(self, user: User, request: Optional[Request] = None,
                             response: Optional[Response] = None):
        print(f"User {user.username} has logined.")

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["role_id"] = 1

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user
    

    async def validate_password(
        self, password: str, user: Union[schemas.UC, models.UP]
    ) -> None:
        """
        Validate a password.

        *You should overload this method to add your own validation logic.*

        :param password: The password to validate.
        :param user: The user associated to this password.
        :raises InvalidPasswordException: The password is invalid.
        :return: None if the password is valid.
        """
        s1, s2 = 0, 0
        for p in password:
            if p.isupper():
                s1 = 1
            if p.islower():
                s2 = 1
            if s1 == 1 and s2 == 1:
                break
        if s1 == 0 or s2 == 0:
            raise exceptions.InvalidPasswordException('Password should have UPPER and LOWER symbols')
        
        return


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
