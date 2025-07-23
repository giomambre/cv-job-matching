from fastapi import APIRouter, File, UploadFile, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from web.utils import *
from io import BytesIO

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def home():
    with open("web/index.html", "r", encoding="utf-8") as f:
        return f.read()

@router.get("/success", response_class=HTMLResponse)
def success(request: Request):
    results = request.session.get("results")
    if not results:
        return "<h2>Nessun risultato trovato.</h2><a href='/'>Torna alla home</a>"
    html = "<h2>Upload riuscito!</h2><ul>"
    for job in results:
        html += f"<li><b>{job['Company']} - {job['Role']}</b>: {job['Description']}</li>"
    html += "</ul><a href='/'>Torna alla home</a>"
    return html

@router.post("/upload")
async def upload_cv(request: Request, cvFile: UploadFile = File(...)):
    content = await cvFile.read()
    pdf_stream = BytesIO(content)
    text = extract_pdf_text(pdf_stream)
    if text == "":
        return RedirectResponse(url="/", status_code=303)
    results = find_top_matches(text)
    # Salva i risultati nella sessione
    request.session["results"] = results
    return RedirectResponse(url="/success", status_code=303)