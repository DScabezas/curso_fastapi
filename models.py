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


class TransactionBase(SQLModel):
    ammount: int
    description: str


class TransactionCreate(TransactionBase):
    customer_id: int = Field(foreign_key="customer.id")


class InvoiceBase(SQLModel):
    pass


class Customer(CustomerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    transactions: List["Transaction"] = Relationship(back_populates="customer")
    invoices: List["Invoice"] = Relationship(back_populates="customer")


class Transaction(TransactionBase, table=True):
    id: int = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    customer: Customer = Relationship(back_populates="transactions")
    invoice_id: int = Field(default=None, foreign_key="invoice.id")
    invoice: Optional["Invoice"] = Relationship(back_populates="transactions")


class Invoice(InvoiceBase, table=True):
    id: int = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    customer: Customer = Relationship(back_populates="invoices")
    transactions: List[Transaction] = Relationship(back_populates="invoice")

    @property
    def amount_total(self):
        return sum(t.amount for t in self.transactions)
