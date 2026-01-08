from typing import List

from pydantic import BaseModel


class CustomerBase(BaseModel):
    full_name: str
    description: str | None
    email: str
    age: int


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: int | None = None


class Transaction(BaseModel):
    id: int
    amount: int
    description: str


class Invoice(BaseModel):
    id: int
    customer: Customer
    transaction: List[Transaction]

    @property
    def ammount_total(self):
        return sum(transaction.ammount for transaction in self.transaction)
