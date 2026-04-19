from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from .endpoints import Endpoints
import os
from ._keep_alive import start_keep_alive

start_keep_alive()
    
app = FastAPI()
endpoints = Endpoints(app)
endpoints.setup_endpoints()

@app.get("/health-check")
def health_check():
    return {"status": "healthy"}

frontend_path = os.path.join(os.path.dirname(__file__), "../../front")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")
