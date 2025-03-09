from fastapi import FastAPI
from fastapi.responses import JSONResponse
from backend.routes import notes

app = FastAPI()

app.include_router(notes.router)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}