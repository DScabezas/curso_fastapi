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


class CustomerPlan(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    plan_id: int = Field(foreign_key="plan.id")


class Plan(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: Optional[str] = None
    price: Optional[int] = None
    description: Optional[str] = None
    customers: List["Customer"] = Relationship(
        back_populates="plans", link_model=CustomerPlan
    )


class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    transactions: List["Transaction"] = Relationship(back_populates="customer")
    invoices: List["Invoice"] = Relationship(back_populates="customer")
    plans: List[Plan] = Relationship(
        back_populates="customers", link_model=CustomerPlan
    )


class Transaction(TransactionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    invoice_id: Optional[int] = Field(default=None, foreign_key="invoice.id")
    customer: Customer = Relationship(back_populates="transactions")
    invoice: Optional["Invoice"] = Relationship(back_populates="transactions")


class Invoice(InvoiceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    customer: Customer = Relationship(back_populates="invoices")
    transactions: List[Transaction] = Relationship(back_populates="invoice")

    @property
    def amount_total(self):
        return sum(t.ammount for t in self.transactions)
