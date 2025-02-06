from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class UsuarioEspecial(BaseModel):
    fecha_nacimiento: datetime
    mail: str
    password: str
    rol: str = "cliente"
    nombre: str
    sexo: str
    ultima_conexion: datetime = datetime.now()

    class Config:
        from_attributes = True