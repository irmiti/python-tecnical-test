import sqlalchemy as sa
from sqlalchemy.orm import relationship
from .base import BaseModel, CustomUUID


class VacationModel(BaseModel):
    __tablename__ = "vacation"
    start_date = sa.Column(sa.Date)
    end_date = sa.Column(sa.Date)
    vacation_type = sa.Column(sa.String)
    employee_id = sa.Column(CustomUUID, sa.ForeignKey("employee.id"))

    employee = relationship("EmployeeModel", back_populates="vacations")
