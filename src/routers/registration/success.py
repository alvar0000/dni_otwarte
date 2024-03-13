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


# Wyświetlenie szablonu informującego o pomyślnym zarejestrowaniu użytkownika
@router.get('/success', response_class=HTMLResponse)
def register_success_root(request: Request):
    return templates.TemplateResponse('success.html', {'request': request})
