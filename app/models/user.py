from typing import Optional

from pydantic import EmailStr, BaseModel

from .dbmodel import DBModelMixin
from .rwmodel import RWModel
from ..core.security import generate_salt, get_password_hash, verify_password


class UserBase(RWModel):
    name: Optional[str] = ""
    email: Optional[EmailStr] = None # email: Optional[str] = None
    username: Optional[str] = None
    displayed_user_id: Optional[str] = None
    status: Optional[str] = None


class UserInDB(DBModelMixin, UserBase):
    salt: str = ""
    hashed_password: str = ""

    def check_password(self, password: str):
        return verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str):
        self.salt = generate_salt()
        self.hashed_password = get_password_hash(self.salt + password)


class User(DBModelMixin, UserBase):
    image: Optional[str] = None


class UserInResponse(RWModel):
    user: User


class UserCredentialInResponse(RWModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserSignUpResponse(RWModel):
    success: bool
    message: str


class UserInLogin(RWModel):
    email: Optional[EmailStr] = ""
    password: Optional[str] = ""
    device: Optional[str] = ""
    fcm_token: Optional[str] = ""
    device_uuid: Optional[str] = ""
    platform: Optional[str] = ""


class UserInCreate(UserInLogin):
    username: str
    image: Optional[str] = None
    refer: Optional[str] = ""


class UserInUpdate(RWModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    firstName: Optional[EmailStr] = None
    lastName: Optional[EmailStr] = None
    password: Optional[str] = None
    bio: Optional[str] = None
    image: Optional[str] = None
