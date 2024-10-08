from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware  # Add this import
from pydantic import BaseModel
import json
import logging
import os
import sys
import requests
from typing import Dict

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

system_template = "Rewrite the sentences into a better looking descriptions for resume:"
prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)
model = ChatOpenAI()
parser = StrOutputParser()
chain = prompt_template | model | parser

current_dir = os.path.abspath(__file__)
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
sys.path.append(grandparent_dir)

from resume.latex_utils import render_latex_to_pdf
from resume.generator import render_resume

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResumeData(BaseModel):
    data: Dict
@app.post("/generate_resume")
async def generate_resume(resume_data: ResumeData):
    try:
        # Save input data to JSON
        json_path = "outputs/json/temp_cache.json"
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        with open(json_path, 'w') as f:
            json.dump(resume_data.data, f, indent=2)
        logger.info(f"Saved input data to {json_path}")

        # Generate LaTeX
        latex_path = "outputs/latex/output_resume.tex"
        os.makedirs(os.path.dirname(latex_path), exist_ok=True)
        render_resume(json_path, latex_path)

        # Convert LaTeX to PDF
        pdf_dir = "outputs/pdf"
        os.makedirs(pdf_dir, exist_ok=True)
        render_latex_to_pdf(latex_path, pdf_dir)

        pdf_path = "outputs/pdf/output_resume.pdf"
        return FileResponse(pdf_path, media_type='application/pdf', filename="resume.pdf")

    except Exception as e:
        logger.error(f"Error generating resume: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class TextRequest(BaseModel):
    text: str
class TextResponse(BaseModel):
    enhanced_text: str
@app.post("/enhance-text", response_model=TextResponse)
async def enhance_text(request: TextRequest):
    try:
        print(request.text)
        result = chain.invoke({"text": request.text})
        return TextResponse(enhanced_text=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8045)