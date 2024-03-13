from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# Router aplikacji
router = APIRouter(
    tags=['Password recovery'],
    prefix='/recover_password'
)

# Inicjalizacja szablonów Jinja2
templates = Jinja2Templates(directory="templates/password_recovery")


# Wyświetlenie szablonu, gdzie podaje się nr. telefonu, na który ma zostać wysłany kod weryfikacyjny
@router.get('/', response_class=HTMLResponse)
async def password_recovery_root(request: Request):
    return templates.TemplateResponse('phone_nr.html', {'request': request})


# Wyświetlenie szablonu, gdzie podaje się kod weryfikacyjny
@router.get('/code', response_class=HTMLResponse)
async def get_code_root(request: Request):
    return templates.TemplateResponse('code.html', {'request': request})


# Wyświetlenie szablonu, gdzie podaje się nowe hasło
@router.get('/new', response_class=HTMLResponse)
async def new_password_root(request: Request):
    return templates.TemplateResponse('new.html', {'request': request})


# Wyświetlenie szablonu informującego o pomyślnej zmianie hasła
@router.get('/success', response_class=HTMLResponse)
async def success_root(request: Request):
    return templates.TemplateResponse('success.html', {'request': request})
