from .dbmodel import DBModelMixin, ObjectIdStr
from .rwmodel import RWModel
from bson import ObjectId

class AuthenToken(DBModelMixin, RWModel):
  access_token: str
  refresh_token: str
  user_id: ObjectIdStr = ObjectId()
  device_id: ObjectIdStr = ObjectId()
  online_status: str = "off"

class AuthenTokenInCreate(RWModel):
  access_token: str
  refresh_token: str
  online_status: str = "off"
