from datetime import timedelta

from fastapi import APIRouter, Body, Depends
from starlette.exceptions import HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from ....core.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES
from ....core.jwt import create_access_token, create_request_token
from ....crud.shortcuts import check_free_username_and_email
from ....crud.user import create_user, get_user, get_user_by_email
from ....crud.profile import create_profile
from ....crud.device import create_device
from ....crud.image import create_image
from ....crud.authen_token import create_authen_token
from ....db.mongodb import AsyncIOMotorClient, get_database
from ....models.user import User, UserInCreate, UserInLogin, UserInResponse, UserSignUpResponse, UserCredentialInResponse
from ....models.device import Device, DeviceInPhoneLogin
from ....models.authen_token import AuthenToken, AuthenTokenInCreate
from ....core.otp import create_otp_code, verify_otp_code, VerifyOTPResponse
from ....models.image import Image
from ....models.profile import Profile
from ....core.slack import slack_notification

import facebook
import requests 
import urllib.request
import uuid
import os, ssl
import json
import uuid

router = APIRouter()

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

@router.post("/users/email-login", response_model=UserCredentialInResponse, tags=["authentication"])
async def email_login(
        user: UserInLogin = Body(..., embed=True), db: AsyncIOMotorClient = Depends(get_database)
):
    dbuser = await get_user_by_email(db, user.email)
    if not dbuser or not dbuser.check_password(user.password):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Incorrect email or password"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    request_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"username": dbuser.username}, expires_delta=access_token_expires
    )
    refresh_token = create_request_token(
        data={"username": dbuser.username}, expires_delta=request_token_expires
    )
    
    device = DeviceInPhoneLogin(fcm_token=user.fcm_token, device_uuid=user.device_uuid, platform=user.platform)
    created_device = await create_device(db, device, dbuser.id)
    created_authen_token = await create_authen_token(db, AuthenTokenInCreate(access_token=token, refresh_token=refresh_token, online_status="on"), dbuser.id, created_device.id)
    if not created_authen_token:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid tokens", headers={"WWW-Authenticate": "Bearer"},
        )

    return UserCredentialInResponse(access_token=token, refresh_token=refresh_token, token_type="bearer " + str(created_authen_token.id))


@router.post(
    "/users",
    tags=["authentication"],
    status_code=HTTP_201_CREATED,
)
async def register(
        user: UserInCreate = Body(..., embed=True), db: AsyncIOMotorClient = Depends(get_database)
):
    await check_free_username_and_email(db, user.username, user.email)

    async with await db.start_session() as s:
        async with s.start_transaction():
            dbuser = await create_user(db, user)
            await create_profile(db, Profile(username=dbuser.username))
            return {'message': 'ok'}
