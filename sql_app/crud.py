from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import distinct, func

from . import models, schemas


def create_session(db: Session, session: schemas.VisitingSessionCreate):
    db_session = models.VisitingSession(**session.dict())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)

    return db_session


def get_session_count(db: Session):
    return _get_session_count(db, False)


def get_unique_session_count(db: Session):
    return _get_session_count(db, True)


def _get_session_count(db: Session, is_unique: bool):
    if is_unique:
        query = db.query(
            models.VisitingSession.path,
            func.count(distinct(models.VisitingSession.ip))
        )
    else:
        query = db.query(
            models.VisitingSession.path,
            func.count(models.VisitingSession.ip)
        )

    return query.group_by(
        models.VisitingSession.path
    ).all()


def get_session_count_by_day(db: Session, date: datetime):
    return _get_session_count_between_time(
        db,
        datetime(date.year, date.month, date.day),
        datetime(date.year, date.month, date.day, 23, 59, 59, 999999),
        False
    )


def get_unique_session_count_by_day(db: Session, date: datetime):
    return _get_session_count_between_time(
        db,
        datetime(date.year, date.month, date.day),
        datetime(date.year, date.month, date.day, 23, 59, 59, 999999),
        True
    )


def get_session_count_by_month(db: Session, date: datetime):
    return _get_session_count_between_time(
        db,
        datetime(date.year, date.month, 1),
        datetime(date.year, date.month, 31, 23, 59, 59, 999999),
        False
    )


def get_unique_session_count_by_month(db: Session, date: datetime):
    return _get_session_count_between_time(
        db,
        datetime(date.year, date.month, 1),
        datetime(date.year, date.month, 31, 23, 59, 59, 999999),
        True
    )


def get_session_count_by_year(db: Session, date: datetime):
    return _get_session_count_between_time(
        db,
        datetime(date.year, 1, 1),
        datetime(date.year, 12, 31, 23, 59, 59, 999999),
        False
    )


def get_unique_session_count_by_year(db: Session, date: datetime):
    return _get_session_count_between_time(
        db,
        datetime(date.year, 1, 1),
        datetime(date.year, 12, 31, 23, 59, 59, 999999),
        True
    )


def _get_session_count_between_time(
        db: Session,
        left_border: datetime,
        right_border: datetime,
        is_unique: bool
):
    if is_unique:
        query = db.query(
            models.VisitingSession.path,
            func.count(distinct(models.VisitingSession.ip))
        )
    else:
        query = db.query(
            models.VisitingSession.path,
            func.count(models.VisitingSession.ip)
        )

    return query.filter(
        left_border <= models.VisitingSession.datetime
    ).filter(
        models.VisitingSession.datetime <= right_border
    ).group_by(
        models.VisitingSession.path
    ).all()
