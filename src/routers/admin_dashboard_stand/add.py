from fastapi import APIRouter, Depends, Form, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from src.repository.admin_dashboard_stand.add_stand import (get_rooms, get_entities, is_owner_valid,
                                                            create_stand_request, add_stand_to_db)
from src.repository.dashboard import user_exists, get_user_type
from src import models, database


# Router aplikacji
router = APIRouter(
    tags=['Registration'],
    prefix='/register'
)

# Inicjalizacja szablonów Jinja2
templates = Jinja2Templates(directory="templates/register")


# Wyświetlenie panelu dodawania stanowiska
@router.get('/{user_id}/stand/add', response_class=HTMLResponse)
def add_root(
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

    # Nazwy potencjalnych właścicieli stanowiska
    clubs = get_entities(db, models.Club)
    faculties = get_entities(db, models.Faculty)
    institutes = get_entities(db, models.Institute)
    companies = get_entities(db, models.Company)

    # Nazwy sal
    rooms = get_rooms(db)

    return templates.TemplateResponse(
        'add.html',
        {'request': request,
         'clubs': clubs,
         'faculties': faculties,
         'institutes': institutes,
         'companies': companies,
         'rooms': rooms,
         'user_id': user_id}
    )


# Logika stojąca za dodawaniem stanowiska
@router.post('/{user_id}/stand/add/add')
def add(
        db=Depends(database.get_db),
        name: str = Form(...),
        description: str = Form(...),
        buildingno_roomcode: str = Form(...),
        club: str = Form(None),
        faculty: str = Form(None),
        institute: str = Form(None),
        company: str = Form(None),
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
    if not is_owner_valid(club, faculty, institute, company):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid owner.'
        )

    # Obiekt z danymi rejestracji
    request = create_stand_request(
        name,
        description,
        buildingno_roomcode,
        club,
        faculty,
        institute,
        company
    )

    # Dodanie stanowiska do bazy
    stand_added = add_stand_to_db(db, request)

    # Sprawdzenie, czy pomyślnie dodano stanowisko do bazy
    if stand_added:
        return RedirectResponse(
            f'/dashboard/admin/{user_id}/stand/success',
            status_code=status.HTTP_302_FOUND
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to add stand'
        )
