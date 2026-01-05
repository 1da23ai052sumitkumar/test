from fastapi import FastAPI,HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
import os
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from passlib.context import CryptContext
load_dotenv()

app = FastAPI(title="Test FastAPI Application")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

MONGODB_URL = os.getenv("MONGODB_URL")

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(MONGODB_URL)
    app.db = app.mongodb_client.test
    try:
        await app.mongodb_client.admin.command("ping")
        print("✅ Connected to MongoDB Atlas successfully")
    except Exception as e:
        print("❌ MongoDB connection failed:", e)

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()
    

class UserModel(BaseModel):
    username: str
    email: str
    password: str 
    
class loginModel(BaseModel):
    name:str
    password:str
    
@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}
    

@app.post("/api/signup")
async def signup(user: UserModel):
    existing_user = await app.db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = {
        "username": user.username,
        "email": user.email,
        "password": hash_password(user.password),
    }

    await app.db.users.insert_one(new_user)
    print("User signed up:", new_user["email"])
    return {"message": "Signup successful"}        

@app.post("/api/login")
async def login(user: loginModel):
    db_user = await app.db.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    print("User logged in:", db_user["email"])
    return {"message": "Login successful"}

@app.get("/api/debug")
async def debug():
    return {
        "db_name": app.db.name,
        "collections": await app.db.list_collection_names(),
        "count": await app.db.users.count_documents({})
    }
