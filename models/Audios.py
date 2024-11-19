from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from models.Usuario import Usuario
from models.Texto import Texto


class Audios(BaseModel):
    aws_object_id: Optional[str] = None
    usuario: Optional[Usuario] = None
    fecha: Optional[datetime] = None
    texto: Optional[Texto] = None
    duracion: Optional[float] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }