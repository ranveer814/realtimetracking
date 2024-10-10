import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import pandas as pd
from pydantic import BaseModel

app = FastAPI()

# Define the CSV file path
csv_file = 'data.csv'

# Check if the CSV file exists; if not, create one with headers
if not os.path.exists(csv_file):
    df = pd.DataFrame(columns=["Unique ID", "Name", "Longitude", "Latitude", "Floor"])
    df.to_csv(csv_file, index=False)

# Define the data model for incoming data
class LocationData(BaseModel):
    name: str
    uniqueID: str
    floor: int
    latitude: float  # Use float for latitude (double in Python)
    longitude: float  # Use float for longitude (double in Python)

@app.post("/submit-data")
async def submit_data(data: LocationData):
    try:
        # Extract the details from the incoming data
        unique_id = data.uniqueID
        name = data.name
        longitude = data.longitude
        latitude = data.latitude
        floor = data.floor
        
        # Append the data to the CSV file
        new_data = pd.DataFrame([[unique_id, name, longitude, latitude, floor]], 
                                 columns=["Unique ID", "Name", "Longitude", "Latitude", "Floor"])
        new_data.to_csv(csv_file, mode='a', header=False, index=False)
        
        # Return a success response
        return {"message": "Data received successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/get-csv")
async def get_csv():
    # Check if the file exists before serving
    if os.path.exists(csv_file):
        return FileResponse(csv_file, media_type='text/csv', filename='data.csv')
    else:
        raise HTTPException(status_code=404, detail="CSV file not found")

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
