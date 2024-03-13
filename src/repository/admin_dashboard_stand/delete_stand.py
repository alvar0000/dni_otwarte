from src import models
from sqlalchemy.orm import Session


# Uzyskanie stanowiska na podstawie id stanowiska
def get_stand_to_delete(db: Session, stand_id):
    return (db.query(models.Stand)
            .filter(stand_id == models.Stand.id)
            .first())


# Uzyskanie odwiedzonych stanowisk do usunięcia na podstawie id stanowiska
def get_visited_stands_to_delete(db: Session, stand_id: int):
    return (db.query(models.VisitedStands)
              .filter(stand_id == models.VisitedStands.stand_id)
              .all())


# Sprawdzenie, czy stanowisko istnieje w bazie
def stand_exists(db: Session, stand: models.Stand):
    if get_stand_to_delete(db, stand.id) is None:
        return False
    else:
        return True


# Sprawdzenie, czy odwiedzone stanowiska istnieją w bazie
def visited_stands_exist(db: Session, stand_id: int):
    if get_visited_stands_to_delete(db, stand_id):
        return False
    else:
        return True


# Usunięcie stanowiska z bazy
def delete_stand(db: Session, stand: models.Stand):
    db.delete(stand)
    db.commit()


# Usunięcie odwiedzonych stanowisk z bazy
def delete_visited_stands(db: Session, visited_stands: [models.VisitedStands]):
    db.delete(visited_stands)
    db.commit()
