from typing import Optional, List
from datetime import date, timedelta, datetime
from uuid import UUID

from fastapi import (
    Depends,
    APIRouter,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repository.vacation import VacationRepository
from app.schema import VacationBase, VacationIn

router = APIRouter()


def verify_conflict(session, vacation: VacationIn):
    return VacationRepository.filter(
        session,
        equal={"employee_id": vacation.employee_id},
        lte={"start_date": vacation.end_date},
        gte={"end_date": vacation.start_date},
        ne={"vacation_type": vacation.vacation_type},
    )


def handle_overlap(session, vacation: VacationIn, vacation_id=None):
    start_date, end_date = adjust_date_range(vacation.start_date, vacation.end_date)
    overlaps = VacationRepository.filter(
        session,
        equal={
            "employee_id": vacation.employee_id,
            "vacation_type": vacation.vacation_type
        },
        lte={"start_date": end_date},
        gte={"end_date": start_date},
        ne={"id": vacation_id} if vacation_id else {}
    )
    if not overlaps:
        return vacation.start_date, vacation.end_date
    else:
        start_date = vacation.start_date
        end_date = vacation.end_date
        for overlap in overlaps:
            if overlap.start_date < vacation.start_date:
                start_date = overlap.start_date
            if overlap.end_date > vacation.end_date:
                end_date = overlap.end_date
            VacationRepository.delete(session, id=overlap.id)
        return start_date, end_date


def adjust_date_range(start_date: date, end_date: date):
    start_date = start_date - timedelta(days=3 if start_date.weekday() == 0 else 1)
    end_date = end_date + timedelta(days=3 if end_date.weekday() == 4 else 1)
    return start_date, end_date


@router.post("", response_model=Optional[VacationBase])
def create_vacation(session: Session = Depends(get_db), *, vacation: VacationIn):
    if verify_conflict(session, vacation):
        raise HTTPException(status_code=409, detail=f"Requested vacation conflicts with vacation of another type")
    start_date, end_date = handle_overlap(session=session, vacation=vacation)
    vacation.start_date = start_date
    vacation.end_date = end_date
    return VacationRepository.create(session=session, obj_in=vacation)


@router.delete("/{vacation_id}")
def delete_vacation(session: Session = Depends(get_db), *, vacation_id: UUID):
    if VacationRepository.delete(session=session, id=vacation_id):
        return "OK"
    else:
        raise HTTPException(status_code=404, detail=f"Vacation with id {vacation_id} not found")


@router.put("/{vacation_id}")
def update_vacation(session: Session = Depends(get_db), *, vacation: VacationIn, vacation_id: UUID):
    if verify_conflict(session, vacation):
        raise HTTPException(status_code=409, detail=f"Requested vacation conflicts with vacation of another type")
    start_date, end_date = handle_overlap(session=session, vacation=vacation, vacation_id=vacation_id)
    vacation.start_date = start_date
    vacation.end_date = end_date
    updated_vacation = VacationRepository.update(session, vacation_id, vacation)

    if not updated_vacation:
        raise HTTPException(status_code=404, detail=f"Vacation with id {vacation_id} not found")
    return updated_vacation


@router.get("/now", response_model=List[VacationBase])
def get_now_on_vacation(session: Session = Depends(get_db)):
    today = date.today()
    return VacationRepository.filter(
        session=session,
        equal={},
        gte={"start_date": today},
        lte={"end_date": today},
        ne={}
    )


@router.get("", response_model=List[VacationBase])
def get_vacations(session: Session = Depends(get_db), *, start_date: date = None, end_date: date = None):
    gte = {"start_date": start_date} if start_date else {}
    lte = {"end_date": end_date} if end_date else {}
    return VacationRepository.filter(session=session, equal={}, gte=gte, lte=lte, ne={})
