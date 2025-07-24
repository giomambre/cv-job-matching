from fastapi import APIRouter, File, UploadFile, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from web.utils import *
from io import BytesIO
import json
import logging
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def home():
    with open("web/index.html", "r", encoding="utf-8") as f:
        return f.read()

@router.get("/success", response_class=HTMLResponse)
def success(request: Request):
    results = request.session.get("results")
    if not results:
        return "<h2>No results found.</h2><a href='/'>Back to home</a>"
    html = "<h2>Upload successful!</h2><ul>"
    for job in results:
        html += f"<li><b>{job['Company']} - {job['Role']}</b>: {job['Description']}</li>"
    html += "</ul><a href='/'>Back to home</a>"
    return html

@router.post("/upload")
async def upload_cv(request: Request, cvFile: UploadFile = File(...)):
    """Legacy upload endpoint for backward compatibility"""
    try:
        content = await cvFile.read()
        pdf_stream = BytesIO(content)
        text = extract_pdf_text(pdf_stream)
        
        if text == "":
            return RedirectResponse(url="/", status_code=303)
            
        results = find_top_matches(text)
        request.session["results"] = results
        return RedirectResponse(url="/success", status_code=303)
    except Exception as e:
        print(f"Error processing upload: {e}")
        return RedirectResponse(url="/", status_code=303)
# In api.py
@router.get("/test")
async def test_endpoint():
    return {"message": "Endpoint di test funzionante!"}

@router.post("/api/analyze")
async def analyze_cv_api(cvFile: UploadFile = File(...)):
    """Modern API endpoint for CV analysis"""

    try:
        # Validate file type
        allowed_types = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
        if cvFile.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail="Invalid file type. Please upload a PDF or DOCX file."
            )
        
        # Validate file size (10MB limit)
        content = await cvFile.read()
        if len(content) > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(
                status_code=400, 
                detail="File size too large. Maximum size is 10MB."
            )
        
        # Extract text from PDF
        pdf_stream = BytesIO(content)
        text = extract_pdf_text(pdf_stream)
        
        if not text or text.strip() == "":
            raise HTTPException(
                status_code=400, 
                detail="Could not extract text from the uploaded file. Please ensure it's a valid PDF or DOCX file."
            )
        
        # Find job matches
        results = find_top_matches(text, k=9)
        return JSONResponse(content={
            "success": True,
            "message": "CV analyzed successfully",
            "results": results,
            "total_matches": len(results)
        })
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in CV analysis: {e}")
        raise HTTPException(
            status_code=500, 
            detail="An error occurred while processing your CV. Please try again."
        )

@router.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(content={
        "status": "healthy",
        "message": "CV Job Matcher API is running"
    })
