from fastapi import FastAPI
from database import Base, engine
from api import person_controller
from api import auth_controller

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Village Survey API")

app.include_router(auth_controller.router)
app.include_router(person_controller.router)
