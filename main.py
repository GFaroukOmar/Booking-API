from fastapi import FastAPI
import models, database
from routes import users,booking,slots,services

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.include_router(users.router)
app.include_router(booking.router)
app.include_router(services.router)
app.include_router(slots.router)

# @app.get("/")
# def root():
#     return {"msg": "Booking API running"}
