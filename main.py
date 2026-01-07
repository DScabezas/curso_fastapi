from datetime import datetime

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
   return {"message": "Hello, World"}


@app.get("/date")
def get_date():
   return {"time": datetime.now()}