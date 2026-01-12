from fastapi import APIRouter

from ..db import SessionDep
from ..models import Invoice

router = APIRouter(tags=["Invoices"])


@router.post("/invoices")
async def create_invoice(invoices_data: Invoice, session: SessionDep):
    session.add(invoices_data)
    session.commit()
    session.refresh(invoices_data)
    return invoices_data
