from datetime import timedelta

from fastapi import APIRouter, Body, Depends
from starlette.exceptions import HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

import facebook
import requests 
import urllib.request
import uuid
import os, ssl
import json
import uuid

router = APIRouter()

@router.get("/health", tags=["authentication"])
async def test():
    return {'status': 'ok'}
