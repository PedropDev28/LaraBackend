from pydantic import BaseModel
from datetime import datetime


class Surveys(BaseModel):
    emotion: str
    fecha: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }