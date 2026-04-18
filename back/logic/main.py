from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from endpoints import Endpoints
import os

    
app = FastAPI()
endpoints = Endpoints(app)
endpoints.setup_endpoints()

frontend_path = os.path.join(os.path.dirname(__file__), "../../front")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")
