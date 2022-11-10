from functools import wraps
from datetime import datetime
from uuid import uuid1

from typing import Union

from sql_app.database import *
from sql_app import models, crud, schemas

from sqlalchemy.orm.session import Session

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from starlette.staticfiles import StaticFiles

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


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


@app.get("/", response_class=HTMLResponse)
@session_counter
async def root(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("root.html", {"request": request})


@app.get("/lowPollyFloppa", response_class=HTMLResponse)
@session_counter
async def floppa(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("low_polly_floppa.html", {"request": request})


@app.get("/dancingPolishCow")
@session_counter
async def cow(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("polish_cow.html", {"request": request})


@app.get("/api/v1/statistics/sessionCount")
async def get_all_session_count(
        unique: Union[bool, None] = None,
        db: Session = Depends(get_db)
):
    result = {}

    if unique is None:
        result['sessionCount'] = dict(crud.get_session_count(db))
        result['uniqueSessionCount'] = dict(crud.get_unique_session_count(db))
    elif unique:
        result['uniqueSessionCount'] = dict(crud.get_unique_session_count(db))
    else:
        result['sessionCount'] = dict(crud.get_session_count(db))

    return result


@app.get("/api/v1/statistics/sessionCount/{date}")
async def get_session_count_by_date(
        date: str,
        unique: Union[bool, None] = None,
        db: Session = Depends(get_db)
):
    try:
        date = datetime.strptime(date, '%d-%m-%Y')
    except ValueError:
        return HTMLResponse(
            content={'Error': 'date format must be like this 26-08-2022'},
            status_code=422
        )

    result = {}

    if unique is None:
        by_day = crud.get_session_count_by_day(db, date)
        unique_by_day = crud.get_unique_session_count_by_day(db, date)

        by_month = crud.get_session_count_by_month(db, date)
        unique_by_month = crud.get_unique_session_count_by_month(db, date)

        by_year = crud.get_session_count_by_year(db, date)
        unique_by_year = crud.get_unique_session_count_by_year(db, date)

        result['sessionCount'] = {
            f'{date.day}.{date.month}.{date.year}': dict(by_day),
            f'{date.month}.{date.year}': dict(by_month),
            f'{date.year}': dict(by_year)
        }
        result['uniqueSessionCount'] = {
            f'{date.day}.{date.month}.{date.year}': dict(unique_by_day),
            f'{date.month}.{date.year}': dict(unique_by_month),
            f'{date.year}': dict(unique_by_year)
        }
    elif unique:
        unique_by_day = crud.get_unique_session_count_by_day(db, date)
        unique_by_month = crud.get_unique_session_count_by_month(db, date)
        unique_by_year = crud.get_unique_session_count_by_year(db, date)

        result['uniqueSessionCount'] = {
            f'{date.day}.{date.month}.{date.year}': dict(unique_by_day),
            f'{date.month}.{date.year}': dict(unique_by_month),
            f'{date.year}': dict(unique_by_year)
        }
    else:
        by_day = crud.get_session_count_by_day(db, date)
        by_month = crud.get_session_count_by_month(db, date)
        by_year = crud.get_session_count_by_year(db, date)

        result['sessionCount'] = {
            f'{date.day}.{date.month}.{date.year}': dict(by_day),
            f'{date.month}.{date.year}': dict(by_month),
            f'{date.year}': dict(by_year)
        }

    return result
