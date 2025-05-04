from fastapi import APIRouter
from sqlmodel import Session, select

from ..model.hero import Hero
from ..database import engine

router = APIRouter(
    prefix="/heros",
    tags=["heros"],
)


@router.post("/heroes/")
def create_hero(hero: Hero):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero


@router.get("/heroes/")
def read_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes
