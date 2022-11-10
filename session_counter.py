from functools import wraps
from uuid import uuid1
from datetime import datetime

from sql_app import crud, schemas

from sqlalchemy.orm.session import Session
from fastapi import Request


def session_counter(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = _get_request(kwargs)
        db = _get_db(kwargs)

        visiting_session = schemas.VisitingSessionCreate(
            id=str(uuid1()),
            ip=request.client.host,
            datetime=datetime.now(),
            path=request.url.path
        )

        crud.create_session(
            db,
            visiting_session
        )

        return await func(*args, **kwargs)

    return wrapper


def _get_request(kwargs: dict) -> Request:
    for value in kwargs.values():
        if type(value) is Request:
            return value

    raise ValueError('Wrapped function must be with Request param')


def _get_db(kwargs: dict) -> Session:
    for value in kwargs.values():
        if str(type(value)) == "<class 'sqlalchemy.orm.session.Session'>":
            return value

    raise ValueError('Wrapped function must be with Session param')
