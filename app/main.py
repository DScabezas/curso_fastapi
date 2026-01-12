from fastapi import FastAPI

from db import create_all_tables

from .routers import customers, invoices, transactions

app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(invoices.router)


@app.get("/")
async def root():
    return {"message": "Hello, World"}
