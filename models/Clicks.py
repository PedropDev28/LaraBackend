from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Clicks(BaseModel):
    class_: Optional[str] = None
    method: Optional[str] = None
    tag: Optional[str] = None
    usuario: Optional[str] = None
    timestamp: Optional[datetime] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }