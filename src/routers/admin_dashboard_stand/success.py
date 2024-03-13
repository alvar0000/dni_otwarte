from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# Router aplikacji
router = APIRouter(
    tags=['Admin dashboard'],
    prefix='/dashboard/admin'
)

# Inicjalizacja szablonów Jinja2
templates = Jinja2Templates(directory='templates/admin_dashboard/stand')


# Wyświetlenie panelu sukcesu
@router.get('/{user_id}/stand/success', response_class=HTMLResponse)
def success_root(request: Request, user_id: int = None):
    return templates.TemplateResponse('success.html',
                                      {'request': request,
                                       'user_id': user_id})
