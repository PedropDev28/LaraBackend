from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from models.Usuario import Usuario
from models.Audios import Audios
from typing import Optional

class Sylabus(BaseModel):
    texto: Optional[str] = None
    creador: Usuario
    tags: Optional[List[str]] = []
    audios: Optional[List[Audios]] = []
    fecha_creacion: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }