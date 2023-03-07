from datetime import date, timedelta
from typing import Literal, Optional
from pydantic import BaseModel, root_validator
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from app.model.vacation import VacationModel


class VacationBase(sqlalchemy_to_pydantic(VacationModel)):
    vacation_days: Optional[int]

    @root_validator
    def compute_vacation_days(cls, values):
        all_days = [values["start_date"] + timedelta(x) for x in
                    range((values["end_date"] - values["start_date"]).days + 1)]
        count = sum(1 for day in all_days if day.weekday() < 5)
        values["vacation_days"] = count

        return values


class VacationIn(BaseModel):
    start_date: date
    end_date: date
    employee_id: str
    vacation_type: Literal["paid", "unpaid"]
