from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import login, stand, password_recovery, dashboard
from src.routers.registration import choose_type, student, teacher
from src.routers.admin_dashboard_stand import add, delete, update
from src.routers.registration import success as reg_success
from src.routers.admin_dashboard_stand import success as stand_success

# Inicjalizacja obiektu aplikacji
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dodanie routerów aplikacji
app.include_router(login.router)
app.include_router(stand.router)
app.include_router(password_recovery.router)
app.include_router(dashboard.router)
app.include_router(choose_type.router)
app.include_router(student.router)
app.include_router(teacher.router)
app.include_router(reg_success.router)
app.include_router(add.router)
app.include_router(delete.router)
app.include_router(update.router)
app.include_router(stand_success.router)
