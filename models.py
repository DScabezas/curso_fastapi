from pydantic import BaseModel


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

