import pickle
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import numpy as np
from datetime import datetime

# --- Configuration & Model Loading ---
MODEL_FILE = "best_flight_price_model_XGBoost_20260216_182739.pkl"
MODEL_VERSION = "1.0.0"

try:
    with open(MODEL_FILE, "rb") as f:
        model = pickle.load(f)
    print(f"✅ Model loaded successfully from {MODEL_FILE}")
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    model = None

# --- Pydantic Models (Schema) ---
class FlightInput(BaseModel):
    Airline: str
    Date_of_Journey: str
    Source: str
    Destination: str
    Route: str
    Dep_Time: str
    Arrival_Time: str
    Duration: str
    Total_Stops: str
    Additional_Info: str

class FlightResponse(BaseModel):
    predicted_price: float
    confidence_interval: dict
    input_data: dict
    feature_importance: dict = {}

# --- Prediction Logic ---
def predict_flight_price(data: FlightInput) -> FlightResponse:
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Convert input to DataFrame
    input_dict = data.dict()
    df = pd.DataFrame([input_dict])
    
    # Preprocessing (Add any specific preprocessing your model expects here)
    # For now, we assume the pipeline handles raw data or we pass the DF directly
    # Note: If your model expects specific encoded columns, they must be handled.
    # Since we lack the original preprocessing code, we try to pass the dataframe.
    
    try:
        # Prediction
        prediction = model.predict(df)
        predicted_price = float(prediction[0])
        
        # Mock confidence interval (replace with actual if model supports it)
        lower_bound = predicted_price * 0.9
        upper_bound = predicted_price * 1.1
        
        return FlightResponse(
            predicted_price=predicted_price,
            confidence_interval={"lower": lower_bound, "upper": upper_bound},
            input_data=input_dict,
            feature_importance={} # Can generate if needed
        )
    except Exception as e:
        print(f"Prediction Error: {e}")
        # If prediction fails, it might be due to missing preprocessing.
        # Fallback/Error handling
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

# --- FastAPI App ---
app = FastAPI(
    title="✈️ Flight Price Prediction API",
    description="API for predicting flight prices using optimized ML model",
    version=MODEL_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "service": "Flight Price Prediction API",
        "version": MODEL_VERSION,
        "status": "active" if model else "inactive",
        "model_loaded": model is not None
    }

@app.get("/health")
def health_check():
    if model is None:
        return JSONResponse(status_code=503, content={"status": "unhealthy", "message": "Model not loaded"})
    return {"status": "healthy", "model_loaded": True}

@app.post("/predict", response_model=FlightResponse)
def predict_endpoint(data: FlightInput):
    return predict_flight_price(data)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
