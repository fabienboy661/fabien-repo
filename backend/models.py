from datetime import datetime
from pydantic import BaseModel, Field
from bson.objectid import ObjectId as BsonObjectID

class PydanticObjectId(BsonObjectID):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not isinstance(v, BsonObjectID):
            raise TypeError("Object ID ERRor")
        return str(v)

class NewReservation(BaseModel):
    email: str
    destination: str
    classe: str
    nombre: int
    name: str
    date: str

class NewAvion(BaseModel):
    name: str
    type: str
    numberplc: int
    numbre: int
    
class Reservation(NewReservation):
    id: PydanticObjectId = Field(..., alias="_id")
    
class Avion(NewAvion):
    id: PydanticObjectId = Field(..., alias="_id")
    
class User(BaseModel):
    username: str
    password: str