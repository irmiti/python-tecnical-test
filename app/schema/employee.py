from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from pydantic import BaseModel

from app.model.employee import EmployeeModel


class EmployeeBase(sqlalchemy_to_pydantic(EmployeeModel)):
    ...


class EmployeeIn(BaseModel):
    first_name: str
    last_name: str
