from typing import Optional

from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from ..crud.user import get_user
from ..db.mongodb import AsyncIOMotorClient
from ..core.config import database_name, profiles_collection_name, referrers_collection_name
from ..models.profile import Profile
from datetime import datetime


async def create_profile(conn: AsyncIOMotorClient, profile: Profile) -> Profile:
    profile.created_at = datetime.now()
    profile.updated_at = datetime.now()
    await conn[database_name][profiles_collection_name].insert_one(profile.dict())
    return profile


async def update_profile_bio(conn: AsyncIOMotorClient, profile: Profile) -> Profile:
    dbuser = await get_profile_for_user(conn, profile.username)
    
    if not dbuser:
        profile.username = username
        dbuser = await create_profile(conn, profile.username)

    await conn[database_name][profiles_collection_name].update_one({"username": profile.username}, {'$set': {
        'phoneNumber': profile.phoneNumber,
        'completed': True
    }})
    await conn[database_name][referrers_collection_name].update_one({"username": profile.username}, {'$set': {'verified': True}})
    return dbuser


async def get_profile_for_user(conn: AsyncIOMotorClient, username: str):
    row = await conn[database_name][profiles_collection_name].find_one({"username": username})
    if row:
        return {'username': username, 'completed': row['completed']}

