from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.database import engine, Base

from app.db import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to MechConnect FastAPI Backend API"}

from app.api.routes import auth, users, mechanics, services, vehicles, bookings, pickups, payments, ratings, feedback, admin, customers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["Users"])
app.include_router(customers.router, prefix=f"{settings.API_V1_STR}/customers", tags=["Customers"])
app.include_router(mechanics.router, prefix=f"{settings.API_V1_STR}/mechanics", tags=["Mechanics"])
app.include_router(services.router, prefix=f"{settings.API_V1_STR}/services", tags=["Services"])
app.include_router(vehicles.router, prefix=f"{settings.API_V1_STR}/vehicles", tags=["Vehicles"])
app.include_router(bookings.router, prefix=f"{settings.API_V1_STR}/bookings", tags=["Bookings"])
app.include_router(pickups.router, prefix=f"{settings.API_V1_STR}/pickups", tags=["Pickups"])
app.include_router(payments.router, prefix=f"{settings.API_V1_STR}/payments", tags=["Payments"])
app.include_router(ratings.router, prefix=f"{settings.API_V1_STR}/ratings", tags=["Ratings"])
app.include_router(feedback.router, prefix=f"{settings.API_V1_STR}/feedback", tags=["Feedback"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["Admin"])

# import os
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# dist_path = os.path.join(BASE_DIR, "../dist")

# app.mount("/assets", StaticFiles(directory=os.path.join(dist_path, "assets")), name="assets")

# @app.get("/{full_path:path}")
# def serve_frontend(full_path: str):
#     return FileResponse(os.path.join(dist_path, "index.html"))