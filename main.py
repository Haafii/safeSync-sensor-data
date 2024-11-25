import os
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List
from bson import ObjectId

# MongoDB setup
client = MongoClient("mongodb+srv://hafi:Hafi1234@cluster0.wgiuymy.mongodb.net/safesync?retryWrites=true&w=majority&appName=Cluster0")
db = client["safesync"]
collection = db["sensor_data"]

app = FastAPI()

class SensorData(BaseModel):
    latitude: float
    longitude: float
    speed: float
    accelerometer_x: float
    accelerometer_y: float
    accelerometer_z: float
    gyro_x: float
    gyro_y: float
    gyro_z: float

class SensorDataResponse(SensorData):
    id: str

def convert_objectid_to_str(data):
    if isinstance(data, ObjectId):
        return str(data)
    if isinstance(data, dict):
        data["id"] = str(data["_id"])
        del data["_id"]
        return {key: convert_objectid_to_str(value) for key, value in data.items()}
    if isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    return data

@app.post("/sensor-data/")
async def create_sensor_data(sensor_data: SensorData):
    sensor_dict = sensor_data.dict()
    result = collection.insert_one(sensor_dict)
    response_data = convert_objectid_to_str(sensor_dict)
    return {"message": "Sensor data saved", "data": response_data, "id": str(result.inserted_id)}

@app.get("/sensor-data/", response_model=List[SensorDataResponse])
async def get_sensor_data():
    data = collection.find()
    return [SensorDataResponse(**convert_objectid_to_str(item)) for item in data]

# Ensure that FastAPI binds to the correct port
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
