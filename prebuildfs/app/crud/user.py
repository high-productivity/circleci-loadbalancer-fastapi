from ..db.mongodb import AsyncIOMotorClient
from pydantic import EmailStr
from bson.objectid import ObjectId
from datetime import datetime

from ..core.config import database_name, users_collection_name
from ..models.user import UserInCreate, UserInDB, UserInUpdate, User, UserInPhoneCreate, UserBase

async def get_user(conn: AsyncIOMotorClient, username: str) -> UserInDB:
    row = await conn[database_name][users_collection_name].find_one({"username": username})
    if row:
        user = UserInDB(**row)
        user.id = str(row['_id'])
        return user


async def get_user_by_email(conn: AsyncIOMotorClient, email: EmailStr) -> UserInDB:
    row = await conn[database_name][users_collection_name].find_one({"email": email})
    if row:
        user = UserInDB(**row)
        user.id = str(row['_id'])
        return user


async def create_user(conn: AsyncIOMotorClient, user: UserInCreate) -> UserInDB:
    dbuser = UserInDB(**user.dict())
    dbuser.change_password(user.password)
    dbuser.created_at = datetime.now()
    dbuser.updated_at = datetime.now()
    row = await conn[database_name][users_collection_name].insert_one(dbuser.dict())

    dbuser.id = row.inserted_id
    dbuser.created_at = ObjectId(dbuser.id ).generation_time
    dbuser.updated_at = ObjectId(dbuser.id ).generation_time
    return dbuser


async def update_user(conn: AsyncIOMotorClient, username: str, user: UserInUpdate) -> UserInDB:
    dbuser = await get_user(conn, username)

    dbuser.username = user.username or dbuser.username
    dbuser.email = user.email or dbuser.email
    if user.password:
        dbuser.change_password(user.password)

    await conn[database_name][users_collection_name].update_one({"username": dbuser.username}, {'$set': dbuser.dict()})
    return dbuser
