from fastapi import FastAPI

from db import create_all_tables

from routers import 

app = FastAPI(lifespan=create_all_tables)


@app.get("/")
async def root():
    return {"message": "Hello, World"}
