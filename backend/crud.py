from fastapi import HTTPException
from backend.db import collection_reservations, user_collection, collection_avions
from backend.models import NewReservation, Reservation, User, Avion
from bson.objectid import ObjectId
from bson.errors import InvalidId

async def create_reservation(reservation):
    document = dict(reservation)
    await collection_reservations.insert_one(document)
    
async def create_avion(avion):
    document = dict(avion)
    await collection_avions.insert_one(document)
    
async def fetch_reservations():
    reservations = []
    cursor = collection_reservations.find({})
    async for document in cursor:
        reservation = Reservation(**document)
        reservations.append(reservation)
    return reservations

async def fetch_avions():
    avions = []
    cursor = collection_avions.find({})
    async for document in cursor:
        avion = Avion(**document)
        avions.append(avion)
    return avions

async def fetch_users():
    users = []
    cursor = user_collection.find({})
    async for document in cursor:
        user = User(**document)
        users.append(user)
    return users 

async def delete_reservation(id):
    try:
        document = await collection_reservations.find_one({"_id": ObjectId(id)})
    except InvalidId:
        raise HTTPException(status_code=422, detail="Id incorrect")
    if not document:
        raise HTTPException(status_code=404, detail="Reservation not found")
    document = await collection_reservations.find_one_and_delete({"_id": ObjectId(id)})
    return document

async def delete_avion(id):
    try:
        document = await collection_avions.find_one({"_id": ObjectId(id)})
    except InvalidId:
        raise HTTPException(status_code=422, detail="Id incorrect")
    if not document:
        raise HTTPException(status_code=404, detail="Plan not found")
    document = await collection_avions.find_one_and_delete({"_id": ObjectId(id)})
    return document

async def delete_user(username):
    try:
        document = await user_collection.find_one({"username": username})
    except InvalidId:
        raise HTTPException(status_code=422, detail="Id incorrect")
    if not document:
        raise HTTPException(status_code=404, detail="Reservation not found")
    document = await user_collection.find_one_and_delete({"username": username})
    return document

async def update_user(username):
    try:
        document = await user_collection.find_one({"username": username})
    except InvalidId:
        raise HTTPException(status_code=422, detail="user incorrect")
    if not document:
        raise HTTPException(status_code=404, detail="Reservation not found")
    document = await user_collection.find_one_and_update({"username": username})
    return document

async def create_user(user):
    user = dict(user)
    document = await user_collection.find_one({"username": user["username"]})
    if document:
        raise HTTPException(status_code=409, detail="Username existe deja")
    await user_collection.insert_one(user)