from pydantic import BaseModel
from datetime import datetime


class VisitingSessionBase(BaseModel):
    id: str
    ip: str
    datetime: datetime
    path: str


class VisitingSessionCreate(VisitingSessionBase):
    pass


class VisitingSession(VisitingSessionBase):
    class Config:
        orm_mode = True
