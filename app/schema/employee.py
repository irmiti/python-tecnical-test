from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from app.model.employee import EmployeeModel


class EmployeeBase(sqlalchemy_to_pydantic(EmployeeModel)):
    ...
