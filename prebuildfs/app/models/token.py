from .rwmodel import RWModel
from typing import Optional

class TokenPayload(RWModel):
    username: str = ""
    device: Optional[str] = ""
