from ..db.mongodb import AsyncIOMotorClient
from ..models.device import Device, DeviceInPhoneLogin
from ..core.config import database_name, devices_collection_name
from bson import ObjectId

async def create_device(conn: AsyncIOMotorClient, device: DeviceInPhoneLogin, user_id: str) -> Device:
  existing_row = await conn[database_name][devices_collection_name].find_one({"fcm_token": device.fcm_token})
  if existing_row:
    existing_device = Device(**existing_row)
    existing_device.id = str(existing_row.get('_id'))
    existing_device.user_id = user_id
    await conn[database_name][devices_collection_name].update_one({"fcm_token": device.fcm_token}, {'$set': {'user_id': user_id}})
    return existing_device
  else:
    dbdevice = Device(**device.dict(by_alias=True))
    dbdevice.user_id = user_id
    row = await conn[database_name][devices_collection_name].insert_one(dbdevice.dict())
    dbdevice.id = row.inserted_id
    return dbdevice 
