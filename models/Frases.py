from pydantic import BaseModel
from datetime import datetime
from models.Usuario import Usuario

class Frases(BaseModel):
    texto: str
    tag: str
    creador: Usuario

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }
        