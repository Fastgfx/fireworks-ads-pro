from fastapi import FastAPI, HTTPException, UploadFile, File, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from pymongo import MongoClient
from bson import ObjectId
import bcrypt
import jwt
import os
import uuid
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List
import json

app = FastAPI(title="Fireworks Advertising API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = MongoClient(MONGO_URL)
db = client.fireworks_advertising

# JWT configuration
JWT_SECRET = "fireworks_secret_key_2025"
JWT_ALGORITHM = "HS256"
security = HTTPBearer()

# File upload configuration
UPLOAD_DIR = Path("/app/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Pydantic models
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    business_name: str
    phone: str
    account_type: str = "regular"  # regular or wholesale

class UserLogin(BaseModel):
    email: str
    password: str

class CustomizationData(BaseModel):
    product_id: str
    business_name: str
    phone_number: str
    logo_url: Optional[str] = None
    logo_position: Optional[dict] = None

class QuoteRequest(BaseModel):
    user_email: str
    business_name: str
    product_name: str
    customization_data: dict
    quantity: int
    message: Optional[str] = None

# Products data
PRODUCTS = [
    {
        "id": "feather-flag-1",
        "name": "Custom Feather Flag - Premium",
        "category": "Feather Flags",
        "description": "High-quality outdoor feather flag perfect for fireworks businesses. Weather resistant and eye-catching.",
        "base_price": 89.99,
        "wholesale_price": 69.99,
        "image_url": "https://images.pexels.com/photos/9557118/pexels-photo-9557118.jpeg",
        "customizable": True,
        "sizes": ["Small (8ft)", "Medium (10ft)", "Large (12ft)"]
    },
    {
        "id": "feather-flag-2", 
        "name": "Custom Feather Flag - Standard",
        "category": "Feather Flags",
        "description": "Cost-effective feather flag solution for promotional events and store fronts.",
        "base_price": 59.99,
        "wholesale_price": 45.99,
        "image_url": "https://images.pexels.com/photos/7956683/pexels-photo-7956683.jpeg",
        "customizable": True,
        "sizes": ["Small (6ft)", "Medium (8ft)", "Large (10ft)"]
    },
    {
        "id": "custom-banner-1",
        "name": "Vinyl Banner - Heavy Duty",
        "category": "Custom Banners", 
        "description": "Durable vinyl banner perfect for outdoor advertising. Customizable with your logo and text.",
        "base_price": 129.99,
        "wholesale_price": 99.99,
        "image_url": "https://images.pexels.com/photos/32275555/pexels-photo-32275555.jpeg",
        "customizable": True,
        "sizes": ["3x6 ft", "4x8 ft", "6x10 ft", "Custom Size"]
    },
    {
        "id": "custom-banner-2",
        "name": "Mesh Banner - Wind Resistant", 
        "category": "Custom Banners",
        "description": "Wind-resistant mesh banner ideal for windy locations. Great visibility with reduced wind load.",
        "base_price": 149.99,
        "wholesale_price": 119.99,
        "image_url": "https://images.unsplash.com/photo-1533069027836-fa937181a8ce?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwxfHxhZHZlcnRpc2luZyUyMGJhbm5lcnN8ZW58MHx8fHwxNzQ4MzY5NDgzfDA&ixlib=rb-4.1.0&q=85",
        "customizable": True,
        "sizes": ["4x8 ft", "6x10 ft", "8x12 ft"]
    },
    {
        "id": "no-smoking-sign-1",
        "name": "No Smoking Sign - Aluminum",
        "category": "No Smoking Signs",
        "description": "Professional aluminum no smoking sign. Required for fireworks retail locations.",
        "base_price": 24.99,
        "wholesale_price": 18.99,
        "image_url": "https://images.pexels.com/photos/29517828/pexels-photo-29517828.jpeg",
        "customizable": False,
        "sizes": ["8x10 inches", "12x16 inches", "18x24 inches"]
    },
    {
        "id": "no-smoking-sign-2",
        "name": "No Smoking Sign - Plastic",
        "category": "No Smoking Signs", 
        "description": "Durable plastic no smoking sign for indoor and outdoor use.",
        "base_price": 15.99,
        "wholesale_price": 11.99,
        "image_url": "https://images.unsplash.com/photo-1494083630901-b3f0cfe59c27?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHwzfHxubyUyMHNtb2tpbmclMjBzaWduc3xlbnwwfHx8fDE3NDgzNjk0Nzh8MA&ixlib=rb-4.1.0&q=85",
        "customizable": False,
        "sizes": ["6x8 inches", "8x10 inches", "12x16 inches"]
    }
]

# Helper functions
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# API Routes
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "Fireworks Advertising API"}

@app.post("/api/auth/register")
async def register_user(user: UserRegister):
    # Check if user already exists
    existing_user = db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    
    # Create user document
    user_doc = {
        "id": str(uuid.uuid4()),
        "email": user.email,
        "password": hashed_password,
        "business_name": user.business_name,
        "phone": user.phone,
        "account_type": user.account_type,
        "wholesale_approved": False if user.account_type == "wholesale" else True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = db.users.insert_one(user_doc)
    
    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user_doc["id"],
            "email": user.email,
            "business_name": user.business_name,
            "account_type": user.account_type,
            "wholesale_approved": user_doc["wholesale_approved"]
        }
    }

@app.post("/api/auth/login")
async def login_user(user: UserLogin):
    # Find user
    db_user = db.users.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Check password
    if not bcrypt.checkpw(user.password.encode('utf-8'), db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": db_user["id"],
            "email": db_user["email"],
            "business_name": db_user["business_name"],
            "account_type": db_user["account_type"],
            "wholesale_approved": db_user["wholesale_approved"]
        }
    }

@app.get("/api/auth/me")
async def get_current_user(current_user_email: str = Depends(verify_token)):
    user = db.users.find_one({"email": current_user_email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user["id"],
        "email": user["email"],
        "business_name": user["business_name"],
        "account_type": user["account_type"],
        "wholesale_approved": user["wholesale_approved"]
    }

@app.get("/api/products")
async def get_products():
    return {"products": PRODUCTS}

@app.get("/api/products/{product_id}")
async def get_product(product_id: str):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    # Validate file type
    allowed_extensions = {".jpg", ".jpeg", ".png", ".pdf", ".ai"}
    file_extension = Path(file.filename).suffix.lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="File type not allowed. Please upload JPG, PNG, PDF, or AI files.")
    
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Return file URL (in production, this would be a proper URL)
    file_url = f"/uploads/{unique_filename}"
    
    return {
        "filename": unique_filename,
        "original_filename": file.filename,
        "file_url": file_url,
        "file_size": file_path.stat().st_size
    }

@app.post("/api/customizations")
async def save_customization(
    customization: CustomizationData,
    current_user_email: str = Depends(verify_token)
):
    customization_doc = {
        "id": str(uuid.uuid4()),
        "user_email": current_user_email,
        "product_id": customization.product_id,
        "business_name": customization.business_name,
        "phone_number": customization.phone_number,
        "logo_url": customization.logo_url,
        "logo_position": customization.logo_position,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = db.customizations.insert_one(customization_doc)
    
    return {
        "id": customization_doc["id"],
        "message": "Customization saved successfully"
    }

@app.get("/api/customizations")
async def get_user_customizations(current_user_email: str = Depends(verify_token)):
    customizations = list(db.customizations.find({"user_email": current_user_email}))
    
    # Convert ObjectId to string and remove _id
    for customization in customizations:
        customization.pop("_id", None)
    
    return {"customizations": customizations}

@app.post("/api/quotes")
async def request_quote(quote: QuoteRequest):
    quote_doc = {
        "id": str(uuid.uuid4()),
        "user_email": quote.user_email,
        "business_name": quote.business_name,
        "product_name": quote.product_name,
        "customization_data": quote.customization_data,
        "quantity": quote.quantity,
        "message": quote.message,
        "status": "pending",
        "created_at": datetime.utcnow()
    }
    
    result = db.quotes.insert_one(quote_doc)
    
    return {
        "id": quote_doc["id"],
        "message": "Quote request submitted successfully. We'll contact you within 24 hours."
    }

@app.get("/api/quotes")
async def get_user_quotes(current_user_email: str = Depends(verify_token)):
    quotes = list(db.quotes.find({"user_email": current_user_email}))
    
    # Convert ObjectId to string and remove _id
    for quote in quotes:
        quote.pop("_id", None)
    
    return {"quotes": quotes}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)