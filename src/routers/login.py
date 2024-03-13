from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from .. import database, models, tokens
from sqlalchemy.orm import Session
from ..hashing import Hash
from ..repository.login import get_user_type


# Router aplikacji
router = APIRouter(
    tags=['Authentication']
)

# Inicjalizacja szablonów Jinja2
templates = Jinja2Templates(directory="templates/login")


# Wyświetlenie szablonu ze stroną logowania
@router.get('/login', response_class=HTMLResponse)
async def login_root(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


# Logika stojąca za logowaniem
@router.post('/login', response_class=HTMLResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    # Pobranie użytkownika z bazy
    user = db.query(models.Visitor).filter(form_data.username == models.Visitor.phone_nr).first()

    # Sprawdzenie, czy użytkownik istnieje
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with phone number {form_data.username} not found'
        )

    # Weryfikacja hasła
    if not Hash.verify(user.password, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Invalid password'
        )

    # Uzyskanie typu użytkownika
    user_type = get_user_type(db, user).lower()

    # Wygenerowanie i zwrócenie tokenu JWT
    access_token = tokens.create_access_token(data={'sub': user.phone_nr})

    # Url panelu
    url = f'/dashboard/{user_type}/{user.id}/'

    # Przeniesienie na odpowiedni panel użytkownika
    return RedirectResponse(url=url, headers={'Authorization': f'Bearer {access_token}'})
