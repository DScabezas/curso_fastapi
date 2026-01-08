from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class CustomerBase(SQLModel):
    full_name: str
    description: Optional[str] = None
    email: str
    age: int


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    pass


class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    invoices: List["Invoice"] = Relationship(back_populates="customer")


class Transaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    amount: int
    description: str
    invoice_id: Optional[int] = Field(foreign_key="invoice.id")
    invoice: Optional["Invoice"] = Relationship(back_populates="transactions")


class Invoice(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_id: Optional[int] = Field(foreign_key="customer.id")
    customer: Optional[Customer] = Relationship(back_populates="invoices")
    transactions: List[Transaction] = Relationship(back_populates="invoice")

    @property
    def amount_total(self):
        return sum(t.amount for t in self.transactions)
