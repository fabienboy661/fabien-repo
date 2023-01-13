from fastapi import FastAPI, Depends, HTTPException
from fastapi_login import LoginManager
from backend.models import NewReservation, Reservation, User, Avion, NewAvion
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from backend.db import user_collection, collection_reservations
from backend.crud import create_reservation, fetch_avions, delete_avion, create_avion, fetch_reservations, update_user, delete_reservation, delete_user, create_user, fetch_users
from fastapi.middleware.cors import CORSMiddleware
from backend.db import client
from bson.objectid import ObjectId

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

SECRET = "seper-secret-key"
manager = LoginManager(SECRET, "/login")

@manager.user_loader()
async def query_user(username):
    document = await user_collection.find_one({"username": username})
    return document
    
@app.post("/create_reservation")
async def new_reservation(reservation: NewReservation):
    await create_reservation(reservation)
    return reservation

@app.post("/create_avion")
async def new_avion(avion: NewAvion):
    await create_avion(avion)
    return avion

@app.get("/get_all_reservations")
async def get_reservations():
    reservations = await fetch_reservations()
    return reservations

@app.get("/get_all_avions")
async def get_avions_by_name():
    avions = await fetch_avions()
    return avions
    
    
@app.delete("/delete_reservation/{id}")
async def delete(id: str):
    item = await delete_reservation(id)
    return Reservation(**item)

@app.delete("/delete_avion/{id}")
async def delete(id: str):
    item = await delete_avion(id)
    return Avion(**item)
   
@app.put("/update_avion/{id}")


@app.delete("/delete_user/{username}")
async def delete(username: str):
    item = await delete_user(username)
    return User(**item)    

# User Login & auth
@app.post("/register")
async def new_user(user: User):
    await create_user(user)
    return user

@app.post("/login")
async def login(data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password
    
    user = await query_user(username)
    if not user: 
        raise InvalidCredentialsException
    if user["password"] != password:
        raise InvalidCredentialsException
    
    access_token = manager.create_access_token(data={"sub": username})
    return {"access_token": access_token}

@app.get("/get_all_users")
async def get_users():
    users = await fetch_users()
    return users