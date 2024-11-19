from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Texto(BaseModel):
    texto: Optional[str] = None
    tag: Optional[str] = None
    tipo: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }