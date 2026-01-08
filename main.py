from typing import List

from fastapi import FastAPI, HTTPException, status
from sqlmodel import select

from db import SessionDep, create_all_tables
from models import Customer, CustomerCreate, CustomerUpdate, Invoice, Transaction

app = FastAPI(lifespan=create_all_tables)


@app.get("/")
async def root():
    return {"message": "Hello, World"}


@app.post("/customer", response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@app.get("/customer/{customer_id}", response_model=Customer)
async def read_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    return customer_db


@app.patch(
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


@app.delete("/customer/{customer_id}")
async def delete_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    session.delete(customer_db)
    session.commit()
    return {"detail": "ok"}


@app.get("/customer", response_model=List[Customer])
async def get_customer(session: SessionDep):
    customers = session.exec(select(Customer)).all()
    return customers


@app.post("/transactions")
async def create_transaction(transaction_data: Transaction, session: SessionDep):
    session.add(transaction_data)
    session.commit()
    session.refresh(transaction_data)
    return transaction_data


@app.post("/invoices")
async def create_invoice(invoices_data: Invoice, session: SessionDep):
    session.add(invoices_data)
    session.commit()
    session.refresh(invoices_data)
    return invoices_data
