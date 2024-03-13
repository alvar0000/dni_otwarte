from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from .. import database
from ..repository.dashboard import (get_stands_by_user_id, get_count_all_stands, get_count_stands_visited_by_user,
                                    user_exists, get_user_type, get_all_stands)

# Router aplikacji
router = APIRouter(
    tags=['Dashboard'],
    prefix='/dashboard'
)

# Inicjalizacja szablonów Jinja2
templates = Jinja2Templates(directory='templates/dashboard')


# Wyświetlenie panelu użytkownika
@router.post('/student/{user_id}', response_class=HTMLResponse)
def student_dashboard_root(
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

    # Sprawdzenie, czy użytkownik jest uczniem
    if get_user_type(db, user_id) != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Invalid user type'
        )

    # Stanowiska odwiedzone przez użytkownika o danym id
    stands = get_stands_by_user_id(db, user_id)

    # Liczba stanowisk odwiedzonych przez użytkownika o danym id
    visited_stands_count = get_count_stands_visited_by_user(db, user_id)

    # Liczba wszystkich stanowisk
    all_stands_count = get_count_all_stands(db)

    return templates.TemplateResponse(
        'student.html',
        {'request': request,
         'stands': stands,
         'all_stands_count': all_stands_count,
         'visited_stands_count': visited_stands_count})


# Wyświetlenie panelu administratora
@router.post('/admin/{user_id}', response_class=HTMLResponse)
def admin_dashboard_root(
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

    return templates.TemplateResponse(
        'admin.html',
        {'request': request,
         'stands': stands,
         'user_id': user_id})
