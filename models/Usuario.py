from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Usuario(BaseModel):
    fecha_nacimiento: Optional[datetime] = None
    mail: Optional[str] = None
    password: Optional[str] = None
    rol: Optional[str] = None
    nombre: Optional[str] = None
    sexo: Optional[str] = None
    parent: Optional[str] = None
    ultima_conexion: Optional[datetime] = None
    cant_audios: Optional[int] = None
    provincia: Optional[str] = None
    enfermedades: Optional[List[str]] = [] 
    dis: Optional[List[str]] = []
    font_size: Optional[float] = None 
    entidad: Optional[str] = None
    observaciones: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }