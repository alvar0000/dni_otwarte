from .. import models, schemas, hashing
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
import re


# Uzyskanie listy stringów w postaci 'Miasto, Szkoła'
def get_cities_schools_pairs(db: Session) -> list:
    cities_schools_pairs = (db.query(models.School.name, models.City.name)
                            .join(models.City, models.School.city_id == models.City.id)
                            )
    cities_schools_pairs = [f'{city}, {school}' for school, city in cities_schools_pairs]
    return cities_schools_pairs


# Uzyskanie id szkoły na podstawie jej nazwy
def get_school_id(db: Session, name: str):
    school = db.query(models.School).filter(models.School.name == name).first()

    if school:
        return school.id
    else:
        return None


# Utworzenie nowego obiektu użytkownika
def create_user(db: Session, type_id: int, request: schemas.NewUser):
    school = request.city_schools.split(', ')[1]
    school_id = get_school_id(db, school)
    user = models.Visitor(
        id=get_max_id_plus_1(db),
        phone_nr=request.phone_nr,
        email=request.email,
        password=hashing.Hash.encrypt(request.password),
        school_id=school_id,
        type=type_id,
    )

    return user


# Sprawdzenie, czy użytkownik o danym numerze telefonu lub emailu już istnieje
def user_exists(db: Session, request: schemas.NewUser):
    if request.email is None:
        return db.query(models.Visitor).filter(models.Visitor.phone_nr == request.phone_nr).first() is not None
    else:
        return db.query(models.Visitor).filter(or_(
            models.Visitor.phone_nr == request.phone_nr,
            models.Visitor.email == request.email)
        ).first() is not None


# Sprawdzenie, czy numer telefonu jest w poprawnym formacie
def is_phone_nr_valid(phone_nr: str):
    return phone_nr.isdigit() and len(phone_nr) == 9


# Sprawdzenie, czy hasło jest w poprawnym formacie
def is_password_valid(password: str):
    return len(password) >= 8 and ' ' not in password


# Sprawdzenie, czy email jest w poprawnym formacie
def is_email_valid(email: str):
    pattern = r"[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}$"
    return re.match(pattern, email)


# Utworzenie obiektu requestu z danymi rejestracji
def create_request(phone_nr: str, password: str, city_schools: str, email: str = None):
    return schemas.NewUser(
        phone_nr=phone_nr,
        password=password,
        city_schools=city_schools,
        email=email
    )


# Dodanie nowego użytkownika
def add_user_to_db(db: Session, user_type, request: schemas.NewUser):
    new_user = create_user(db, user_type, request)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user.id


# Uzyskanie maksymalnego id + 1
def get_max_id_plus_1(db: Session):
    max_id = db.query(func.max(models.Visitor.id)).scalar()
    if max_id is None:
        return 1
    else:
        return max_id + 1
