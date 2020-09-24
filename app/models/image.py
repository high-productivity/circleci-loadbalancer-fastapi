from typing import Optional

# from pydantic import UrlStr

from .rwmodel import RWModel


class Image(RWModel):
    user_id: str
    key: str
    type: str
    
