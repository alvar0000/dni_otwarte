from fastapi import APIRouter, Depends, Request, HTTPException, status, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from src.repository.registration import (get_cities_schools_pairs, user_exists, is_phone_nr_valid,
                                         is_password_valid, is_email_valid, create_request, add_user_to_db)
from src import database
from sqlalchemy.orm import Session
from typing import Optional


# Router aplikacji
router = APIRouter(
    tags=['Registration'],
    prefix='/register'
)


# Inicjalizacja szablonów Jinja2
templates = Jinja2Templates(directory="templates/register")


# Wyświetlenie szablonu pozwalającego na wpisanie danych nauczyciela
@router.get('/teacher/form', response_class=HTMLResponse)
def register_teacher_root(request: Request, db: Session = Depends(database.get_db)):
    cities_schools_pairs = get_cities_schools_pairs(db)
    return templates.TemplateResponse('teacher.html',
                                      {'request': request,
                                       'cities_schools_pairs': cities_schools_pairs})


# Logika stojąca za rejestracją nauczyciela
@router.post('/teacher/register')
def register_teacher(phone_nr: str = Form(...),
                     password: str = Form(...),
                     city_schools: str = Form(...),
                     email: Optional[str] = Form(...),
                     db: Session = Depends(database.get_db)):

    # Obiekt z danymi rejestracji
    request = create_request(phone_nr, password, city_schools, email)

    # Sprawdzenie, czy numer telefonu jest w poprawnym formacie
    if not is_phone_nr_valid(request.phone_nr):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid phone number.')

    # Sprawdzenie, czy hasło jest w poprawnym formacie
    if not is_password_valid(request.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid password.')

    # Sprawdzenie, czy email jest w poprawnym formacie
    if not is_email_valid(request.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid email.')

    # Sprawdzenie, czy użytkownik o danym numerze telefonu i emailu już istnieje
    if user_exists(db, request):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User already exists.')

    # Dodanie nowego użytkownika
    user_added = add_user_to_db(db=db, user_type=2, request=request)

    # Sprawdzenie, czy użytkownik został poprawnie dodany
    if user_added:
        return RedirectResponse(url="/register/success", status_code=status.HTTP_302_FOUND)
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to register user')
