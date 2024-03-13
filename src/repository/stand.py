from sqlalchemy.orm import Session, load_only
from sqlalchemy import and_, func
from .. import models, schemas


# Uzyskanie informacji o stanowisku o danym id
def get_stand(db: Session, stand_id: int):
    stand = (db.query(models.Stand, models.Room)
               .join(models.Room, models.Stand.room_id == models.Room.id)
               .filter(models.Stand.id == stand_id)
               .options(
                    load_only(models.Stand.name, models.Stand.room_id, models.Stand.description, models.Stand.room_id),
                    load_only(models.Room.schedule_url))
               .first())

    return stand


# Uzyskanie informacji o właścicielu stanowiska o danym id
def get_owner(db: Session, stand_id: int):
    stand = (db.query(models.Stand)
               .filter(models.Stand.id == stand_id)
               .options(load_only(models.Stand.club_id, models.Stand.fac_id, models.Stand.inst_id, models.Stand.comp_id))
               .first())

    owner = None

    if stand.club_id is not None:
        owner = db.query(models.Club).filter(models.Club.id == stand.club_id).first()
    elif stand.fac_id is not None:
        owner = db.query(models.Faculty).filter(models.Faculty.id == stand.fac_id).first()
    elif stand.inst_id is not None:
        owner = db.query(models.Institute).filter(models.Institute.id == stand.inst_id).first()
    elif stand.comp_id is not None:
        owner = db.query(models.Company).filter(models.Company.id == stand.comp_id).first()

    return owner


# Dodawanie nowego odwiedzonego stanowiska przez danego użytkownika
def add_visited_stand(db: Session, current_user: schemas.TokenData, stand_id: int):
    user = get_user_with_phone_nr(db, current_user.phone_nr)
    id = get_max_id_plus_1(db)
    new_visited_stand = create_visited_stand(id, user.id, stand_id)
    db.add(new_visited_stand)
    db.commit()
    db.refresh(new_visited_stand)


# Uzyskanie maksymalnego id + 1
def get_max_id_plus_1(db: Session):
    max_id = db.query(func.max(models.VisitedStands.id)).scalar()
    if max_id is None:
        return 1
    else:
        return max_id + 1


# Uzyskanie użytkownika na podstawie numeru telefonu
def get_user_with_phone_nr(db: Session, phone_nr: str):
    return (db.query(models.Visitor)
              .filter(phone_nr == models.Visitor.phone_nr)
              .first())


# Utworzenie obiektu odwiedzonego stanowiska
def create_visited_stand(id: int, user_id: int, stand_id: int):
    return models.VisitedStands(
        id=id,
        vis_id=user_id,
        stand_id=stand_id
    )


# Sprawdzenie, czy użytkownik odwiedził już dane stanowisko
def has_visited(db: Session, current_user: schemas.TokenData, stand_id: int):
    user = get_user_with_phone_nr(db, current_user.phone_nr)
    return db.query(models.VisitedStands).filter(and_(
                            stand_id == models.Visitor.stand_id,
                            user.id == models.VisitedStands.vis_id)
                       ).first() is not None


def get_user_type(db: Session, current_user: schemas.TokenData):
    user = db.query(models.Visitor).filter(
        current_user.phone_nr == models.Visitor.phone_nr
    ).first()
    return user.type
