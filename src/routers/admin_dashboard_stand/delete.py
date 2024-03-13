from fastapi import APIRouter, Depends, Form, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from src.repository.admin_dashboard_stand.delete_stand import (get_stand_to_delete, get_visited_stands_to_delete,
                                                               delete_stand, delete_visited_stands, stand_exists,
                                                               visited_stands_exist)
from src.repository.dashboard import user_exists, get_user_type, get_all_stands
from src import database

# Router aplikacji
router = APIRouter(
    tags=['Admin dashboard'],
    prefix='/dashboard/admin'
)

# Inicjalizacja szablonów Jinja2
templates = Jinja2Templates(directory='templates/admin_dashboard/stand')


# Wyświetlenie panelu usuwania stanowiska
@router.get('/{user_id}/stand/delete', response_class=HTMLResponse)
def delete_root(
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

    stands = get_all_stands(db)

    return templates.TemplateResponse(
        'delete.html',
        {'request': request,
         'stands': stands,
         'user_id': user_id})


# Logika stojąca usuwaniem stanowiska
@router.post('/{user_id}/stand/delete/delete')
def delete(
        db=Depends(database.get_db),
        stand_id=Form(...),
        user_id: int = None
):

    stand = get_stand_to_delete(db, stand_id)
    visited_stands = get_visited_stands_to_delete(db, stand_id)

    delete_visited_stands(db, visited_stands)
    delete_stand(db, stand)

    if not stand_exists(db, stand) and not visited_stands_exist(db, visited_stands):
        return RedirectResponse(
            f'/dashboard/admin/{user_id}/stand/success',
            status_code=status.HTTP_302_FOUND
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to delete stand'
        )
