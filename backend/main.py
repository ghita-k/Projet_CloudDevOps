from fastapi import FastAPI
from routes.tasks import router as task_router
from db import connect_to_mongo
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

app.include_router(task_router)


app.include_router(task_router)


# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
   print("ABOUT TO CONNECT TO DATABASE")
   await connect_to_mongo()

@app.get('/ok')
def read_ok():
    return {"status": "ok"}

@app.get("/test-db")
async def test_db():
    try:
        print("Attempting to connect to the database...")
        await connect_to_mongo()
        print("Connection successful!")
        return {"message": "Database connection successful!"}
    except Exception as e:
        print(f"Database connection failed: {str(e)}")
        return {"error": f"Database connection failed: {str(e)}"}


@app.get("/")
def root():
    return {"message": "Backend is running"}



