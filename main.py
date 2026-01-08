from fastapi import FastAPI

from db import SessionDep, create_all_tables
from models import Customer, CustomerCreate, Invoice, Transaction

app = FastAPI(lifespan=create_all_tables)


@app.get("/")
async def root():
    return {"message": "Hello, World"}


db_customer: list[Customer] = []


@app.post("/customer", response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session=SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    customer.id = len(db_customer)
    db_customer.append(customer)
    return customer


@app.get("/customer")
async def get_customer():
    return db_customer


@app.post("/transactions")
async def create_transaction(transaction_data: Transaction, session=SessionDep):
    return transaction_data


@app.post("/invoices")
async def create_invoice(invoices_data: Invoice, session=SessionDep):
    return invoices_data
