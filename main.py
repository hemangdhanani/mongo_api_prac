from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

# to establish a connection
client = AsyncIOMotorClient(MONGO_URI)
db = client['Fast_API']  # db name
api_data = db["Api_Coll"] # collection or Table

app = FastAPI()

class studentdata(BaseModel):
    name: str
    phone: int
    city: str
    course: str


@app.post("/student/insert")
async def student_data_insert_helper(data: studentdata):
    result = await api_data.insert_one(data.dict())
    return {
        "message": "Data inserted successfully",
        "inserted_id": str(result.inserted_id)
    }

def data_helper(doc):
    doc['id'] = str(doc["_id"])
    del doc["_id"]
    return doc

@app.get("/euron/getdata")
async def get_student_data():
    items =[]
    cursor = api_data.find({})
    async for document in cursor:
        items.append(data_helper(document))
        # items.append(document.name)
    return items    
