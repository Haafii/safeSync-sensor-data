# from fastapi import FastAPI
# from pydantic import BaseModel
# from pymongo import MongoClient
# from typing import List
# from bson import ObjectId  # Import ObjectId to handle it

# # MongoDB setup
# client = MongoClient("mongodb+srv://hafi:Hafi1234@cluster0.wgiuymy.mongodb.net/safesync?retryWrites=true&w=majority&appName=Cluster0")  # Replace with your MongoDB URI
# db = client["safesync"]  # Database name
# collection = db["sensor_data"]  # Collection name

# # Create the FastAPI app instance
# app = FastAPI()

# # Define a model for the POST request body
# class SensorData(BaseModel):
#     latitude: float
#     longitude: float
#     speed: float
#     accelerometer_x: float
#     accelerometer_y: float
#     accelerometer_z: float
#     gyro_x: float
#     gyro_y: float
#     gyro_z: float

# # Define a Pydantic model that includes ObjectId as a string
# class SensorDataResponse(SensorData):
#     id: str  # Add the id field to the response model

# # Function to convert MongoDB ObjectId to string
# def convert_objectid_to_str(data):
#     if isinstance(data, ObjectId):
#         return str(data)
#     if isinstance(data, dict):
#         return {key: convert_objectid_to_str(value) for key, value in data.items()}
#     if isinstance(data, list):
#         return [convert_objectid_to_str(item) for item in data]
#     return data

# # Define a GET route
# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the FastAPI backend"}

# # Define a POST route to save sensor data to MongoDB
# @app.post("/sensor-data/")
# async def create_sensor_data(sensor_data: SensorData):
#     # Convert Pydantic model to dictionary
#     sensor_dict = sensor_data.dict()
    
#     # Insert data into MongoDB collection
#     result = collection.insert_one(sensor_dict)
    
#     # Return response with the inserted data and MongoDB id
#     response_data = convert_objectid_to_str(sensor_dict)
#     return {"message": "Sensor data saved", "data": response_data, "id": str(result.inserted_id)}

# # Define a GET route to fetch all sensor data from MongoDB
# @app.get("/sensor-data/", response_model=List[SensorDataResponse])
# async def get_sensor_data():
#     # Retrieve all documents from MongoDB collection
#     data = collection.find()
    
#     # Convert MongoDB documents to Pydantic models and convert ObjectId to string
#     return [SensorDataResponse(**convert_objectid_to_str(item)) for item in data]


from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List
from bson import ObjectId  # Import ObjectId to handle it

# MongoDB setup
client = MongoClient("mongodb+srv://hafi:Hafi1234@cluster0.wgiuymy.mongodb.net/safesync?retryWrites=true&w=majority&appName=Cluster0")  # Replace with your MongoDB URI
db = client["safesync"]  # Database name
collection = db["sensor_data"]  # Collection name

# Create the FastAPI app instance
app = FastAPI()

# Define a model for the POST request body
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

# Define a Pydantic model that includes ObjectId as a string
class SensorDataResponse(SensorData):
    id: str  # Add the id field to the response model

# Function to convert MongoDB ObjectId to string and map _id to id
def convert_objectid_to_str(data):
    if isinstance(data, ObjectId):
        return str(data)
    if isinstance(data, dict):
        # Ensure the _id field is renamed to id
        data["id"] = str(data["_id"])
        del data["_id"]  # Remove the _id field after mapping it to id
        return {key: convert_objectid_to_str(value) for key, value in data.items()}
    if isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    return data

# Define a GET route
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI backend"}

# Define a POST route to save sensor data to MongoDB
@app.post("/sensor-data/")
async def create_sensor_data(sensor_data: SensorData):
    # Convert Pydantic model to dictionary
    sensor_dict = sensor_data.dict()
    
    # Insert data into MongoDB collection
    result = collection.insert_one(sensor_dict)
    
    # Return response with the inserted data and MongoDB id
    response_data = convert_objectid_to_str(sensor_dict)
    return {"message": "Sensor data saved", "data": response_data, "id": str(result.inserted_id)}

# Define a GET route to fetch all sensor data from MongoDB
@app.get("/sensor-data/", response_model=List[SensorDataResponse])
async def get_sensor_data():
    # Retrieve all documents from MongoDB collection
    data = collection.find()
    
    # Convert MongoDB documents to Pydantic models and convert ObjectId to string
    return [SensorDataResponse(**convert_objectid_to_str(item)) for item in data]
