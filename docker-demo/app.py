
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Industry Classification API")

class BusinessRequest(BaseModel):
    business_name: str

def classify_business(name: str) -> str:
    name = name.lower()

    if "fedex" in name or "ups" in name:
        return "TRANSPORTATION & LOGISTICS"
    elif "microsoft" in name or "google" in name:
        return "TECHNOLOGY"
    elif "boeing" in name or "airbus" in name:
        return "AEROSPACE"
    else:
        return "UNKNOWN"

@app.get("/")
def home():
    return {"message": "Industry Classifier API is running"}

@app.post("/classify")
def classify(request: BusinessRequest):
    industry = classify_business(request.business_name)

    return {
        "business_name": request.business_name,
        "industry": industry
    }
