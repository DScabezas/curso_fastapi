from fastapi import APIRouter, status
from sqlmodel import select

from db import SessionDep
from models import Plan

router = APIRouter(tags=["Plans"])


@router.post("/plans", status_code=status.HTTP_201_CREATED)
def create_plan(plan_data: Plan, session: SessionDep):
    plan_db = Plan.model_validate(plan_data.model_dump())
    session.add(plan_db)
    session.commit()
    session.refresh(plan_db)
    return plan_db


@router.get("/plan", response_model=list[Plan])
def list_plan(session: SessionDep):
    query = select(Plan)
    plans = session.exec(query).all()
    return plans
