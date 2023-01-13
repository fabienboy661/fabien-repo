from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017")

db = client.fabidb
collection_reservations = db.reservations
user_collection = db.users
collection_avions = db.avion
       