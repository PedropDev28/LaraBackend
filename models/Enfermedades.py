from pydantic import BaseModel
from datetime import datetime


class Enfermedades(BaseModel):
    nombre: str
    visible: int

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }