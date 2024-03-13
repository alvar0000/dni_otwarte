from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    phone_nr: Optional[str] = None


# Model przechowujące dane podane przy rejestracji
class NewUser(BaseModel):
    phone_nr: str
    password: str
    city_schools: str
    email: Optional[str]


# Model przechowujący dane użytkownika
class User(BaseModel):
    phone_nr: str
    password: str
    school: str
    email: Optional[str]
    type: int


# Model przechowujący dane ucznia
class Student(User):
    email: None
    type: int = 1


# Model przechowujący dane nauczyciela
class Teacher(User):
    type: int = 2


class NewStand(BaseModel):
    name: str
    description: str
    buildingno_roomcode: str
    club: Optional[str]
    faculty: Optional[str]
    institute: Optional[str]
    company: Optional[str]


class Stand(BaseModel):
    name: str
    description: str
    room_id: Optional[int]
    club_id: Optional[int]
    fac_id: Optional[int]
    inst_id: Optional[int]
    comp_id: Optional[int]
