# pylint: disable=invalid-name, too-few-public-methods, no-name-in-module
"""
Модуль для управления базой данных 'Бухгалтерия' через FastAPI.

Для запуска сервера используйте команду:
# uvicorn task:app --reload
Для просмотра документации перейдите по ссылке:
# http://127.0.0.1:8000/docs
"""

import datetime
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import sessionmaker, relationship, Session, declarative_base

# ==========================================
# НАСТРОЙКА БАЗЫ ДАННЫХ
# ==========================================

SQLALCHEMY_DATABASE_URL = "sqlite:///./accounting.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ==========================================
# МОДЕЛИ БАЗЫ ДАННЫХ (SQLAlchemy)
# ==========================================


class Department(Base):
    """Модель таблицы отделов."""
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    employees = relationship("Employee", back_populates="department")


class Employee(Base):
    """Модель таблицы сотрудников."""
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    position = Column(String)
    salary = Column(Float)
    dept_id = Column(Integer, ForeignKey("departments.id"))

    department = relationship("Department", back_populates="employees")


class Counterparty(Base):
    """Модель таблицы контрагентов."""
    __tablename__ = "counterparties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    inn = Column(String, unique=True)


class Category(Base):
    """Модель таблицы категорий операций."""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


class Transaction(Base):
    """Модель таблицы финансовых транзакций."""
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now)

    emp_id = Column(Integer, ForeignKey("employees.id"))
    counterparty_id = Column(Integer, ForeignKey("counterparties.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))


# Создание всех таблиц в БД
Base.metadata.create_all(bind=engine)


# ==========================================
# СХЕМЫ ДАННЫХ (Pydantic)
# ==========================================


class EmployeeCreate(BaseModel):
    """Схема для создания нового сотрудника."""
    full_name: str
    position: str
    salary: float
    dept_id: int


class EmployeeOut(EmployeeCreate):
    """Схема для вывода данных о сотруднике."""
    id: int

    class Config:
        """Настройки Pydantic для работы с SQLAlchemy."""
        orm_mode = True


# ==========================================
# ВЕБ-ПРИЛОЖЕНИЕ И ЭНДПОЙНТЫ (FastAPI)
# ==========================================

app = FastAPI(title="Система Бухгалтерии (Accounting API)")


def get_db():
    """Генератор сессий базы данных для каждого запроса."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get(
    "/employees/",
    response_model=List[EmployeeOut],
    summary="Получить список всех сотрудников"
)
def read_employees(db: Session = Depends(get_db)):
    """Возвращает список всех сотрудников из базы данных."""
    return db.query(Employee).all()


@app.post(
    "/employees/",
    response_model=EmployeeOut,
    summary="Добавить нового сотрудника"
)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    """Создает нового сотрудника и сохраняет его в базу."""
    db_employee = Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


@app.put("/employees/{emp_id}", summary="Изменить зарплату сотрудника")
def update_employee(emp_id: int, new_salary: float, db: Session = Depends(get_db)):
    """Находит сотрудника по ID и обновляет его заработную плату."""
    db_emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if not db_emp:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")

    db_emp.salary = new_salary
    db.commit()
    return {"message": f"Зарплата сотрудника ID={emp_id} успешно обновлена на {new_salary}"}


@app.delete("/employees/{emp_id}", summary="Уволить (удалить) сотрудника")
def delete_employee(emp_id: int, db: Session = Depends(get_db)):
    """Удаляет сотрудника из базы данных по его ID."""
    db_emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if not db_emp:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")

    db.delete(db_emp)
    db.commit()
    return {"message": "Сотрудник удален из базы"}


@app.post("/setup/", summary="Заполнить справочники (отделы, категории)")
def setup_db(db: Session = Depends(get_db)):
    """Заполняет пустую базу данных базовыми отделами и контрагентами."""
    if db.query(Department).first():
        return {"message": "База уже инициализирована"}

    dept1 = Department(name="Бухгалтерия")
    dept2 = Department(name="IT Отдел")
    cat1 = Category(name="Выплата зарплаты")
    cp1 = Counterparty(name="Банк ВТБ", inn="123456789")

    db.add_all([dept1, dept2, cat1, cp1])
    db.commit()
    return {"message": "Базовые данные добавлены!"}
