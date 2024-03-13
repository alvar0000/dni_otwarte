from sqlalchemy.orm import Session, load_only
from src import models, schemas
from sqlalchemy import and_, func


# Uzyskanie id sali na podstawie numery budynku i numeru sali
def get_room_id(db, building_no, room_code):
    room = (db.query(models.Room)
            .filter(and_(building_no == models.Room.building_no, room_code == models.Room.code))
            .first())
    return room.id


# Uzyskanie id właściciela na podstawie nazwy i modelu
def get_owner_id(db: Session, owner_name, owner_model):
    if owner_name is not None:
        owner = (db.query(owner_model)
                 .filter(owner_name == owner_model.name)
                 .first())
        return owner.id
    else:
        return None


# Uzyskaj nazwy właścicieli z tabeli o danym modelu
def get_entities(db: Session, model):
    return db.query(model).options(load_only(model.name)).all()


# Uzyskaj listę stringów w formacie 'numer_budynku, numer sali'
def get_rooms(db: Session):
    rooms = (db.query(models.Room)
             .options(load_only(models.Room.building_no, models.Room.code))
             .all())
    buildingno_roomcode_pairs = [(room.building_no, room.code)for room in rooms]
    buildingno_roomcode_pairs = [f'{building_no}, {code}' for building_no, code in buildingno_roomcode_pairs]
    return buildingno_roomcode_pairs


# Utworzenie obiektu nowego stanowiska
def create_stand_request(
        name: str,
        description: str,
        buildingno_roomcode: str,
        club: str = None,
        faculty: str = None,
        institute: str = None,
        company: str = None
):
    return schemas.NewStand(
        name=name,
        description=description,
        buildingno_roomcode=buildingno_roomcode,
        club=club,
        faculty=faculty,
        institute=institute,
        company=company
    )


# Sprawdzenie, czy poprawnie wybrano właściciela stanowiska
def is_owner_valid(club, faculty, institute, company):
    if (club is not None and faculty is None and institute is None and company is None) or \
            (club is None and faculty is not None and institute is None and company is None) or \
            (club is None and faculty is None and institute is not None and company is None) or \
            (club is None and faculty is None and institute is None and company is not None):
        return True
    else:
        return False


# Uzyskanie maksymalnego id + 1
def get_max_id_plus_1(db: Session):
    max_id = db.query(func.max(models.Stand.id)).scalar()
    if max_id is None:
        return 1
    else:
        return max_id + 1


# Utworzenie modelu stanowiska
def create_stand(db: Session, request: schemas.NewStand):
    building_no, room_code = request.buildingno_roomcode.split(', ')
    room_id = get_room_id(db, building_no, room_code)
    club_id = get_owner_id(db, request.club, models.Club)
    fac_id = get_owner_id(db, request.faculty, models.Faculty)
    inst_id = get_owner_id(db, request.institute, models.Institute)
    comp_id = get_owner_id(db, request.company, models.Company)
    stand = models.Stand(
        id=get_max_id_plus_1(db),
        name=request.name,
        description=request.description,
        room_id=room_id,
        club_id=club_id,
        fac_id=fac_id,
        inst_id=inst_id,
        comp_id=comp_id
    )
    return stand


# Dodanie stanowiska do bazy
def add_stand_to_db(db: Session, request: schemas.NewStand):
    new_stand = create_stand(db, request)
    db.add(new_stand)
    db.commit()
    db.refresh(new_stand)
    return new_stand.id
