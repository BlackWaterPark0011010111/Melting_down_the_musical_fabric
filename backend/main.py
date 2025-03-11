import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from backend.routes import notes

app = FastAPI()

public_path = os.path.join(os.getcwd(), 'frontend', 'public')


if not os.path.exists(public_path):
    raise RuntimeError(f"Directory '{public_path}' does not exist")

app.mount("/static", StaticFiles(directory=public_path), name="static")

app.include_router(notes.router)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}