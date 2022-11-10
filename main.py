from datetime import datetime
from typing import Union

from session_counter import session_counter
from sql_app.database import *
from sql_app import models, crud

from sqlalchemy.orm.session import Session

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from starlette.staticfiles import StaticFiles

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
@session_counter
async def root(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "root.html",
        {"request": request}
    )


@app.get("/lowPollyFloppa", response_class=HTMLResponse)
@session_counter
async def floppa(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "low_polly_floppa.html",
        {"request": request}
    )


@app.get("/dancingPolishCow")
@session_counter
async def cow(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "polish_cow.html",
        {"request": request}
    )


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
        result['sessionCount'] = _get_session_count(date, db)
        result['uniqueSessionCount'] = _get_unique_session_count(date, db)
    elif unique:
        result['uniqueSessionCount'] = _get_unique_session_count(date, db)
    else:
        result['sessionCount'] = _get_session_count(date, db)

    return result


def _get_session_count(date: datetime, db: Session) -> dict:
    by_day = crud.get_session_count_by_day(db, date)
    by_month = crud.get_session_count_by_month(db, date)
    by_year = crud.get_session_count_by_year(db, date)

    return {
        f'{date.day}.{date.month}.{date.year}': dict(by_day),
        f'{date.month}.{date.year}': dict(by_month),
        f'{date.year}': dict(by_year)
    }


def _get_unique_session_count(date: datetime, db: Session) -> dict:
    unique_by_day = crud.get_unique_session_count_by_day(db, date)
    unique_by_month = crud.get_unique_session_count_by_month(db, date)
    unique_by_year = crud.get_unique_session_count_by_year(db, date)

    return {
        f'{date.day}.{date.month}.{date.year}': dict(unique_by_day),
        f'{date.month}.{date.year}': dict(unique_by_month),
        f'{date.year}': dict(unique_by_year)
    }
