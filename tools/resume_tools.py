import json
import subprocess
import os
from typing import Union
import sys
from crewai_tools import tool
import requests
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'  # Added datetime format
)
logger = logging.getLogger(__name__)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from resume.generator import generate
from resume.latex_utils import render_latex_to_pdf, escape_latex
from tools.tools_utils import count_pages_and_lines, generate_comparison_pdf

@tool("save_resume_json")
def save_resume_json(resume_data: Union[str, dict]) -> str:
    """
    Saves the provided resume data as JSON to a file 'outputs/json/resume.json'.
    
    Args:
    resume_data (Union[str, dict]): A string representation of the resume JSON data or a Python dictionary.
    
    Returns:
    str: A message indicating success or failure of the save operation.
    """
    try:
        if isinstance(resume_data, str):
            resume_json = json.loads(resume_data)
        
        elif isinstance(resume_data, dict):
            resume_json = resume_data
        else:
            return "Error: Input must be a JSON string or a Python dictionary."
        
        try: 
            response = requests.post(
                'http://127.0.0.1:8041/sendjson',
                headers={"Content-Type": "application/json"},
                json=resume_json
            )

            if response.status_code == 200:
                logger.info("JSON sent successfully to the frontend")
            else:
                logger.info(f"Failed to send JSON. {response.text}")
        except Exception as e:
            logger.error(f"Exception when sending JSON {e}")

        with open('outputs/json/resume.json', 'w') as f:
            json.dump(resume_json, f, indent=2)
        return "Resume JSON successfully saved to 'outputs/json/resume.json'."
    except json.JSONDecodeError:
        return "Error: The provided string data is not valid JSON."
    except IOError:
        return "Error: Unable to write to 'data/resume.json'. Please check file permissions."
    except Exception as e:
        return f"Error: An unexpected error occurred: {str(e)}"

@tool("generate_resume")
def generate_resume_tool(resume_content: str) -> str:
    """
    Generates a LaTeX document from the given resume content and converts it to PDF.

    Args:
    resume_content (str): The content of the resume in a structured format.

    Returns:
    None: A latex file of the resume outputs/latex/output_resume.tex and a generated pdf version of resume at outputs/pdf/output_resume.pdf are saved
    """
    generate()
        

@tool("line count on extra page")
def pgcount_tool(pdf_path: str) -> str:
    """
    Counts the number of pages and extra lines on the second page of a PDF.

    Args:
    pdf_path (str): The path to the generated resume pdf file.

    Returns:
    str: A message indicating the number of pages and extra lines, or an error message.
    """
    print(f"Counting lines from pdf file {pdf_path}")
    try:
        pages, extra_lines = count_pages_and_lines(pdf_path)
        
        if pages == 1 and extra_lines >= 50:
            return "The resume fits on one page perfectly."
        elif pages == 1 and extra_lines < 50:
            return f"The resume fits on one page but its too short. Consider adding {50-extra_lines} more lines."
        elif pages > 1:
            return f"The resume is {pages} pages long with {extra_lines} extra lines on the second page. Pleasse remove some irrelavant work experiences to make the resume short."
        else:
            return "Error: Unable to determine page count."
    except Exception as e:
        return f"Error: {str(e)}"


@tool("pdf_comparison_tool")
def pdf_comparison_tool(pdf_file1: str, pdf_file2: str, output_pdf: str) -> str:
    """
    Generates a PDF file that contains a side-by-side comparison of two PDF files.
    
    Args:
    pdf_file1 (str): The path to the first PDF file.
    pdf_file2 (str): The path to the second PDF file.
    output_pdf (str): The path where the comparison PDF will be saved.
    
    Returns:
    str: A message indicating the result of the comparison generation.
    """
    try:
        generate_comparison_pdf(pdf_file1, pdf_file2, output_pdf)
        return f"Comparison PDF successfully generated and saved to {output_pdf}"
    except Exception as e:
        return f"Error generating comparison PDF: {str(e)}"