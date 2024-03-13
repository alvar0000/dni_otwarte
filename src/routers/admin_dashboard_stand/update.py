from fastapi import APIRouter, Depends, Form, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from src.repository.admin_dashboard_stand.add_stand import get_rooms, get_entities, is_owner_valid, get_room_id
from src.repository.admin_dashboard_stand.update_stand import update_stand
from src.repository.dashboard import user_exists, get_user_type, get_all_stands
from src import models, database

# Router aplikacji
router = APIRouter(
    tags=['Admin dashboard'],
    prefix='/dashboard/admin'
)

# Inicjalizacja szablonów Jinja2
templates = Jinja2Templates(directory='templates/admin_dashboard/stand')


# Wyświetlenie panelu aktualizacji stanowiska
@router.get('/{user_id}/stand/update', response_class=HTMLResponse)
def update_root(
        request: Request,
        db: Session = Depends(database.get_db),
        user_id: int = None
):

    # Sprawdzenie, czy użytkownik istnieje
    if not user_exists(db, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id {user_id} not found.'
        )

    # Sprawdzenie, czy użytkownik jest adminem
    if get_user_type(db, user_id) != 4:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Invalid user type'
        )

    # Wszystkie stanowiska
    stands = get_all_stands(db)

    # Nazwy potencjalnych właścicieli stanowiska
    clubs = get_entities(db, models.Club)
    faculties = get_entities(db, models.Faculty)
    institutes = get_entities(db, models.Institute)
    companies = get_entities(db, models.Company)

    # Nazwy sal
    rooms = get_rooms(db)

    return templates.TemplateResponse(
        'update.html',
        {'request': request,
         'stands': stands,
         'clubs': clubs,
         'faculties': faculties,
         'institutes': institutes,
         'companies': companies,
         'rooms': rooms,
         'user_id': user_id
         }
    )


# Logika stojąca za aktualizacją stanowiska
@router.post('/{user_id}/stand/update/update')
def update(
        db: Session = Depends(database.get_db),
        stand=Form(...),
        name=Form(None),
        description=Form(None),
        buildingno_roomcode=Form(None),
        club_id=Form(None),
        faculty_id=Form(None),
        institute_id=Form(None),
        company_id=Form(None),
        user_id: int = None
):
    # Sprawdzenie długości nazwy stanowiska
    if len(name) > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Too long stand name.'
        )

    # Sprawdzenie długości opisu stanowiska
    if len(description) > 500:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Too long description.'
        )

    # Sprawdzenie, czy wybrano poprawnie właściciela stanowiska
    if not is_owner_valid(club_id, faculty_id, institute_id, company_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid owner'
        )

    # Pobranie id sali na podstawie stringu "numer budynku, numer sali"
    if buildingno_roomcode is not None:
        building_no, room_code = buildingno_roomcode.split(', ')
        room_id = get_room_id(db, building_no, room_code)
    else:
        room_id = None

    # Dane zaktualizowanego stanowiska,
    # Jeżeli pole zostało podane w formularzu, zapisz jako nowa wartość stanowiska
    # W przeciwnym razie, zostaw oryginalne wartości
    updated_data = {
        'name': name or stand.name,
        'description': description or stand.description,
        'room_id': room_id or stand.room_id,
        'club_id': club_id or stand.club_id,
        'fac_id': faculty_id or stand.fac_id,
        'inst_id': institute_id or stand.inst_id,
        'comp_id': company_id or stand.comp_id
    }

    # Aktualizacja stanowiska
    updated_stand = update_stand(db, stand.id, updated_data)

    # Sprawdzenie, czy poprawnie zaktualizowano stanowisko
    if updated_stand:
        return RedirectResponse(
            f'/dashboard/admin/{user_id}/stand/success',
            status_code=status.HTTP_302_FOUND
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to delete stand'
        )
