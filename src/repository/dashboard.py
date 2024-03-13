from sqlalchemy.orm import Session, load_only
from .. import models


# Stanowiska uzyskane przez użytkownika o danym id
def get_stands_by_user_id(db: Session, user_id: int):
    return (db.query(models.VisitedStands, models.Stand)
              .filter(user_id == models.VisitedStands.vis_id)
              .join(models.Stand, models.VisitedStands.stand_id == models.Stand.id)
              .options(load_only(models.Stand.name, models.Stand.id))
              .all())


# Wszystkie stanowiska
def get_all_stands(db: Session):
    return (db.query(models.Stand)
              .options(load_only(models.Stand.name, models.Stand.id))
              .all())


# Liczba wszystkich stanowisk
def get_count_all_stands(db: Session):
    return db.query(models.Stand).count()


# Liczba stanowisk odwiedzonych przez użytkownika o danym id
def get_count_stands_visited_by_user(db: Session, user_id: int):
    return (db.query(models.VisitedStands)
              .filter(user_id == models.VisitedStands.vis_id)
              .count())


# Sprawdzenie, czy użytkownik istnieje
def user_exists(db: Session, user_id: int):
    return (db.query(models.Visitor)
              .filter(user_id == models.Visitor.id)
              .first()) is not None


# Zwrócenie typu użytkownika
def get_user_type(db: Session, user_id: int):
    user = (db.query(models.Visitor)
              .filter(user_id == models.Visitor.id)
              .first())

    return user.type
