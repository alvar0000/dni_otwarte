from fastapi import Request, Depends, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from .. import database, tokens, schemas
from ..repository.stand import get_stand, get_owner, add_visited_stand, has_visited, get_user_type
from ..tokens import oauth2_scheme

# Router aplikacji
router = APIRouter(
    tags=['Stand'],
    prefix='/stand',
)


# Inicjalizacja szablonów Jinja2
templates = Jinja2Templates(directory="templates/stand")


# Wyświetlenie szablony zawierającego informacje o stanowisku o danym id
@router.post('/{stand_id}', response_class=HTMLResponse)
def show_stand(
        request: Request,
        db: Session = Depends(database.get_db),
        stand_id: int = None,
        current_user: schemas.TokenData = Depends(tokens.get_current_user)
):

    # Jeżeli użytkownik jest uczniem, to zarejestruj, że odwiedził dane stanowisko
    if get_user_type(db, current_user) == 1 and not has_visited(db, current_user, stand_id):
        add_visited_stand(db, current_user, stand_id)

    # Uzyskanie parametrów stanowiska
    stand = get_stand(db, stand_id)
    owner = get_owner(db, stand_id)

    # Przygotowanie danych do przesłania do szablonu
    template_data = {
        'request': request,
        'name': stand[0].name,
        'description': stand[0].description,
        'owner_name': owner.name
    }

    # Wyświetlenie odpowiedniego szablonu na podstawie tego,
    # czy dane stanowisko jest powiązane z jakąś salą, czy nie
    if stand[0].room_id is None:
        return templates.TemplateResponse('no_room.html', template_data)
    else:
        template_data['room_id'] = stand[0].room_id
        template_data['schedule_url'] = stand[1].schedule_url
        return templates.TemplateResponse('with_room.html', template_data)
