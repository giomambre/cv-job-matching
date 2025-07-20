from fastapi import APIRouter, FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from web.utils import extract_pdf_text
from io import BytesIO

router = APIRouter()
@router.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@router.get("/success", response_class=HTMLResponse)
def success():
    return "<h2>Upload riuscito!</h2><a href='/'>Torna alla home</a>"

@router.post("/upload")
async def upload_cv(cvFile: UploadFile = File(...)):
    content = await cvFile.read()
    pdf_stream = BytesIO(content)
    text = extract_pdf_text(pdf_stream)
    if text == "":
        return RedirectResponse(url="/", status_code=303)
    return RedirectResponse(url="/success", status_code=303)