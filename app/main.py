from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from pathlib import Path


app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
HTML_DIR = BASE_DIR/'static'/'index.html'


@app.get("/", response_class = FileResponse)
def show_homepage():
    return FileResponse(HTML_DIR)

@app.post('/send')
def get_details(resume: str = Form(...) , jd: str = Form(...)):
    return [resume,jd]
    

