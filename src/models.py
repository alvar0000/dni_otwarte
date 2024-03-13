from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey


# Odzwierciedlenie tabeli county w bazie danych
class County(Base):
    __tablename__ = 'county'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)


# Odzwierciedlenie tabeli city w bazie danych
class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    county_id = Column(Integer, ForeignKey('county.id'))


# Odzwierciedlenie tabeli school w bazie danych
class School(Base):
    __tablename__ = 'school'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(500), nullable=False)
    patron = Column(String(300))
    city_id = Column(Integer, ForeignKey('city.id'))
    street = Column(String(50))
    building_no = Column(String(20))


# Odzwierciedlenie tabeli visitor_type w bazie danych
class VisitorType(Base):
    __tablename__ = 'visitor_type'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), nullable=False)


# Odzwierciedlenie tabeli visitor w bazie danych
class Visitor(Base):
    __tablename__ = 'visitor'
    id = Column(Integer, primary_key=True, index=True)
    phone_nr = Column(String(9), nullable=False, unique=True)
    email = Column(String(50))
    password = Column(String(300), nullable=False)
    school_id = Column(Integer, ForeignKey('school.id'))
    type = Column(Integer, ForeignKey('visitor_type.id'), nullable=False)


# Odzwierciedlenie tabeli company w bazie danych
class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(70), nullable=False)


# Odzwierciedlenie tabeli institute w bazie danych
class Institute(Base):
    __tablename__ = 'institute'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(70), nullable=False)


# Odzwierciedlenie tabeli club w bazie danych
class Club(Base):
    __tablename__ = 'club'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)


# Odzwierciedlenie tabeli faculty w bazie danych
class Faculty(Base):
    __tablename__ = 'faculty'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(70), nullable=False)


# Odzwierciedlenie tabeli room w bazie danych
class Room(Base):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True, index=True)
    building_no = Column(String(10), nullable=False)
    schedule_url = Column(String(50))
    code = Column(String(10))


# Odzwierciedlenie tabeli stand w bazie danych
class Stand(Base):
    __tablename__ = 'stand'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    description = Column(String(500))
    room_id = Column(Integer, ForeignKey('room.id'))
    club_id = Column(Integer, ForeignKey('club.id'))
    fac_id = Column(Integer, ForeignKey('faculty.id'))
    inst_id = Column(Integer, ForeignKey('institute.id'))
    comp_id = Column(Integer, ForeignKey('company.id'))


# Odzwierciedlenie tabeli visited_stands w bazie danych
class VisitedStands(Base):
    __tablename__ = 'visited_stands'
    id = Column(Integer, primary_key=True, index=True)
    vis_id = Column(Integer, ForeignKey('visitor.id'), nullable=False)
    stand_id = Column(Integer, ForeignKey('stand.id'), nullable=False)
