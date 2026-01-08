from fastapi import FastAPI

from models import CustomerCreate, Invoice, Transaction

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, World"}


@app.post("/customer")
async def create_customer(customer_data: CustomerCreate):
    return customer_data


@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
    return transaction_data


@app.post("/invoices")
async def create_invoice(invoices_data: Invoice):
    return invoices_data
