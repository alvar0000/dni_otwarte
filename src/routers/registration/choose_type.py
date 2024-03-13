from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


# Router aplikacji
router = APIRouter(
    tags=['Registration'],
    prefix='/register'
)


# Inicjalizacja szablonów Jinja2
templates = Jinja2Templates(directory="templates/register")


# Wyświetlenie szablonu, pozwalającego na wybranie typu użytkownika (uczeń, nauczyciel)
@router.get('/', response_class=HTMLResponse)
def register_root(request: Request):
    return templates.TemplateResponse('choose_type.html', {'request': request})
