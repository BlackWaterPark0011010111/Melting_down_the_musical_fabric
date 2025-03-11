import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.routes import notes
from backend import auth
from backend.routes.notes import router
from backend.routes import users
app = FastAPI()

public_path = os.path.join(os.getcwd(), 'frontend', 'public')

if not os.path.exists(public_path):
    raise RuntimeError(f"Directory '{public_path}' does not exist")
 
app.mount("/static", StaticFiles(directory=public_path), name="static")

app.include_router(notes.router)
app.include_router(auth.router)
app.include_router(users.router)
@app.get("/")
async def root():
    return {"message": "Hello, World!"}
