from typing import Optional
from uuid import UUID

from fastapi import (
    Depends,
    APIRouter,
)
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repository.employee import EmployeeRepository
from app.schema import EmployeeBase, EmployeeIn

router = APIRouter()


@router.get("/{employee_id}", response_model=Optional[EmployeeBase])
def get_employee(session: Session = Depends(get_db), *, employee_id: UUID):
    return EmployeeRepository.get(session=session, id=employee_id)


@router.post("", response_model=Optional[EmployeeBase])
def create_employee(session: Session = Depends(get_db), *, employee: EmployeeIn):
    return EmployeeRepository.create(session=session, obj_in=employee)
