from typing import List

from fastapi import FastAPI
from sqlmodel import select

from db import SessionDep, create_all_tables
from models import Customer, CustomerCreate, Invoice, Transaction

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
