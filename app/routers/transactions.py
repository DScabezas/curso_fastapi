from fastapi import APIRouter

from ..db import SessionDep
from ..models import Transaction

router = APIRouter(tags="Transactions")


@router.post("/transactions")
async def create_transaction(transaction_data: Transaction, session: SessionDep):
    session.add(transaction_data)
    session.commit()
    session.refresh(transaction_data)
    return transaction_data
