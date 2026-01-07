import zoneinfo
from datetime import datetime

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
   return {"message": "Hello, World"}


country_timezones = {
   "CO": "America/Bogota",
   "EC": "America/Guayaquil",
   "PE": "America/Lima",
}


@app.get("/time/{iso_code}")
def get_date(iso_code: str):
   iso_code = iso_code.upper()
   timezone = country_timezones.get(iso_code)
   tz = zoneinfo.ZoneInfo(timezone)
   return {"time": datetime.now(tz)}