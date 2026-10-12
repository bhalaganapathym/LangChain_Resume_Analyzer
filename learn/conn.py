from pathlib import Path
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
# the Path() Converts that path string into a flexible, modern object from Python pathlib library
# this facilitates .resolve() which removes the relative paths such as . and ..
# .parent - strips the own file name and gives only the parent directory

HTML_FDIR = BASE_DIR / 'static' / 'index.html'

"""
We use the / operator with pathlib objects instead of a hardcoded string like "/static/index.html" for two main reasons:
 ==> cross-platform safety
 ==> intelligent path building.

"""

@app.post("/greet")
async def greet(f_name: str = Form(...), l_name: str = Form(...)):
    full_name = f"{f_name} {l_name}"
    return {"message":f"Hello, {full_name} !"}

@app.get("/", response_class = FileResponse)
async def show_homepage():
    return FileResponse(HTML_FDIR)
