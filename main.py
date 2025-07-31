from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import agent

app = FastAPI(title="Open General Agent")

origins = [
    "http://localhost:3000", 
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agent.router)


@app.get("/")
async def root():
    return {"message": "Open General Agent API"}

