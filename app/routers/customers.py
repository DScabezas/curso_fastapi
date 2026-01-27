from typing import List

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from db import SessionDep
from models import Customer, CustomerCreate, CustomerPlan, CustomerUpdate, Plan

router = APIRouter(tags=["Customers"])


@router.get("/customer", response_model=List[Customer])
async def get_customer(session: SessionDep):
    customers = session.exec(select(Customer)).all()
    return customers


@router.get("/customer/{customer_id}", response_model=Customer)
async def read_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    return customer_db


@router.post("/customer", response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@router.patch(
    "/customer/{customer_id}",
    response_model=Customer,
    status_code=status.HTTP_201_CREATED,
)
async def update_customer(
    customer_id: int, customer_data: CustomerUpdate, session: SessionDep
):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )

    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    customer_db.sqlmodel_update(customer_data_dict)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db


@router.delete("/customer/{customer_id}")
async def delete_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    session.delete(customer_db)
    session.commit()
    return {"detail": "ok"}


@router.post("/customer/{customer_id}/plans/{plan_id}")
async def subscribe_customer_to_plan(
    customer_id: int, plan_id: int, session: SessionDep
):
    customer_db = session.get(Customer, customer_id)
    plan_db = session.get(Plan, plan_id)

    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )
    if not plan_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan does not exist"
        )

    customer_plan_db = CustomerPlan(customer_id=customer_db.id, plan_id=plan_db.id)

    session.add(customer_plan_db)
    session.commit()
    session.refresh(customer_plan_db)
    return customer_plan_db
