from ..db.mongodb import AsyncIOMotorClient
from ..models.authen_token import AuthenToken, AuthenTokenInCreate
from ..core.config import database_name, authen_tokens_collection_name
from bson import ObjectId
from ..models.dbmodel import ObjectIdStr

async def create_authen_token(conn: AsyncIOMotorClient, authen_token: AuthenTokenInCreate, user_id: str, device_id: str) -> AuthenToken:
  dbauthen_token = AuthenToken(**authen_token.dict(by_alias=True))
  dbauthen_token.user_id = ObjectIdStr(user_id)
  dbauthen_token.device_id = ObjectIdStr(device_id)
  row = await conn[database_name][authen_tokens_collection_name].insert_one(dbauthen_token.dict())
  dbauthen_token.id = row.inserted_id
  if row:
    return dbauthen_token
    # return AuthenToken(**row)

