from .dbmodel import DBModelMixin, ObjectIdStr
from .rwmodel import RWModel
from bson import ObjectId
from typing import Optional

class Device(DBModelMixin, RWModel):
  fcm_token: str
  device_uuid: str
  platform: str
  user_id: Optional[str] = ""

class DeviceInPhoneLogin(RWModel):
  fcm_token: str
  device_uuid: str
  platform: str