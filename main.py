import zoneinfo
from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def root():
   return {"message": "Hello, World"}

class Customer(BaseModel):
   full_name: str
   description: str | None
   email: str
   age: int


country_timezones = {
   "CO": "America/Bogota",
   "EC": "America/Guayaquil",
   "PE": "America/Lima",
}


@app.get("/time/{iso_code}")
def get_date(iso_code: str):
    iso_code = iso_code.upper()
    timezone = country_timezones.get(iso_code)
    if not timezone:
        return {"error": "Invalid ISO code"}
    tz = zoneinfo.ZoneInfo(timezone)
    return {"time": datetime.now(tz)}

@app.post("/customer/create")
async def create_customer(customer_data: Customer):
   return customer_data