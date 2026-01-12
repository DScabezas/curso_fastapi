from fastapi import FastAPI

from db import create_all_tables

from .routers import customers

app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)


@app.get("/")
async def root():
    return {"message": "Hello, World"}
