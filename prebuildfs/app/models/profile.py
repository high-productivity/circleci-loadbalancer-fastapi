from typing import Optional
from .dbmodel import DBModelMixin
from typing import List

from datetime import datetime

# from pydantic import UrlStr

from .rwmodel import RWModel


class Profile(DBModelMixin):
    username: Optional[str] = ""
    phoneNumber: Optional[str] = ""
    bio: Optional[str] = ""
    gender: Optional[str] = ""
    facebookId: Optional[str] = ""
    targetGenders: Optional[List[str]] = []
    targetAge: Optional[int] = 0
    birthday: Optional[datetime] = None
    tags: Optional[List[str]] = []
    location: Optional[List[float]] = []
    drinking: Optional[str] = ""
    smoking: Optional[str] = ""
    residency: Optional[str] = ""
    height: Optional[str] = ""
    hobbies: Optional[List[str]] = []
    movies: Optional[List[str]] = []
    music: Optional[List[str]] = []
    alone: Optional[List[str]] = []
    friends: Optional[List[str]] = []
    avg_score: Optional[float] = 0
    referrers: Optional[int] = 0
    completed: Optional[bool] = False
    verified: Optional[bool] = False

class ProfileInResponse(RWModel):
    profile: Profile
