from sqlalchemy.orm import Session
from src import models


# Aktualizacja stanowiska o danym id na podstawie zaktualizowanych danych
def update_stand(db: Session, stand_id: int, updated_data: dict):
    stand_to_update = (db.query(models.Stand)
                         .filter(stand_id == models.Stand.id)
                         .first())

    if stand_to_update:
        for key, value in updated_data.items():
            setattr(stand_to_update, key, value)
        db.commit()
        return stand_to_update
    return None
