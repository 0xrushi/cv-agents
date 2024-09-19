import json
import subprocess
import os
import sys
import requests

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'  # Added datetime format
)
logger = logging.getLogger(__name__)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from resume.latex_utils import render_latex_to_pdf, escape_latex

def generate_latex_resume(json_data):
    """
    Generates LaTeX content for a resume based on provided JSON data.

    Args:
    json_data (dict): A dictionary containing resume information.

    Returns:
    str: The LaTeX content for the resume.
    """
    latex_content = r"""
\documentclass[a4paper,11pt]{article}

\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[pdftex]{hyperref}
\usepackage{fancyhdr}
\usepackage{fontawesome}
\usepackage{xcolor}
\usepackage{amsmath}

\pagestyle{fancy}
\fancyhf{}
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}

\urlstyle{same}

\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

\titleformat{\section}{
    \vspace{-4pt}\scshape\raggedright\large
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

\newcommand{\resumeItem}[1]{
  \item\small{
    {#1 \vspace{-2pt}}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-1pt}\item
  \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
    \textbf{#1} & #2 \\
    \textit{\small#3} & \textit{\small #4} \\
  \end{tabular*}\vspace{-5pt}
}

\newcommand{\resumeCertification}[2]{%
  \item
  \begin{tabular*}{0.97\textwidth}{@{}l@{\extracolsep{\fill}}r@{}}
    #1 & \text{#2} \\
  \end{tabular*}\vspace{-4pt}
}

\newcommand{\resumeSubItem}[2]{\resumeItem{#1: #2}\vspace{-4pt}}

\renewcommand{\labelitemii}{$\circ$}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0em, itemindent=0em, label={}, itemsep=0ex]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

\begin{document}

%----------HEADING-----------------
\begin{tabular*}{\textwidth}{l@{\extracolsep{\fill}}r}
\textbf{\href{}{\Large """ + escape_latex(json_data['basics']['name']) + r"""}} & Email: \href{mailto:""" + escape_latex(json_data['basics']['email']) + r"""}{\faEnvelope} """ + escape_latex(json_data['basics']['email']) + r""" \\
"""

    for profile in json_data['basics']['profiles']:
        if profile['network'].lower() == 'linkedin':
            latex_content += r"\href{" + profile['url'] + r"}{LinkedIn: " + escape_latex(profile['username']) + r"} \\"
        elif profile['network'].lower() == 'github':
            latex_content += r"\href{" + profile['url'] + r"}{GitHub: " + escape_latex(profile['username']) + r"} \\"
        elif profile['network'].lower() == 'blog':
            latex_content += r"\href{" + profile['url'] + r"}{Blog: " + escape_latex(profile['url'].split('//')[1]) + r"} \\"

    latex_content += r"\hspace{10pt} & Phone: " + escape_latex(json_data['basics']['phone']) + r"\\"

    latex_content += r"""\end{tabular*}

%-----------SKILLS-----------------
\section{Skills}
\resumeSubHeadingListStart
"""

    for skill in json_data['skills']:
        latex_content += r"\resumeSubItem{\textbf{" + escape_latex(skill['name']) + r"}}{" + escape_latex(', '.join(skill['keywords'])) + r"}" + "\n"

    latex_content += r"""\resumeSubHeadingListEnd

%-----------EXPERIENCE-----------------
\section{Work Experience}
\resumeSubHeadingListStart
"""

    for job in json_data['work']:
        latex_content += r"""
\resumeSubheading
{""" + escape_latex(job['name']) + r"""}{""" + job['startDate'] + r" – " + job['endDate'] + r"""}
{""" + escape_latex(job['position']) + r"""}{""" + escape_latex(job.get('location', '')) + r"""}
\resumeItemListStart
"""
        for highlight in job['highlights']:
            latex_content += r"\resumeItem{" + escape_latex(highlight) + r"}" + "\n"
        latex_content += r"\resumeItemListEnd" + "\n"

    latex_content += r"""\resumeSubHeadingListEnd

%-----------EDUCATION-----------------
\section{Education}
\resumeSubHeadingListStart
"""

    for edu in json_data['education']:
        latex_content += r"""
\resumeSubheading
{""" + escape_latex(edu['institution']) + r"""}{""" + edu['startDate'] + r" - " + edu['endDate'] + r"""}
{""" + escape_latex(edu['studyType']) + r" in " + escape_latex(edu['area']) + r"""}{""" + escape_latex(edu.get('location', '')) + r"""}
"""

    latex_content += r"""\resumeSubHeadingListEnd

\section{Projects}
\resumeSubHeadingListStart
"""

    for project in json_data['projects']:
        latex_content += r"\resumeSubItem{\textbf{" + escape_latex(project['name']) + r"}}{" + escape_latex(project['description']) + r"}" + "\n"

    latex_content += r"""\resumeSubHeadingListEnd

%-----------CERTIFICATIONS-----------------
\section{Certifications}
\resumeSubHeadingListStart
"""

    for cert in json_data['certificates']:
        latex_content += r"\resumeCertification{" + escape_latex(cert['name']) + r"}{" + cert['date'] + r"}{}{}" + "\n"

    latex_content += r"""\resumeSubHeadingListEnd
\end{document}
"""

    return latex_content

def render_resume(json_file_path, output_file_path):
    """
    Loads JSON data from a file, generates LaTeX content, and writes it to a file.

    Args:
    json_file_path (str): The path to the JSON file containing resume data.
    output_file_path (str): The path where the LaTeX file will be saved.
    """
    # Load JSON data
    with open(json_file_path, 'r') as json_file:
        resume_data = json.load(json_file)

    # Generate LaTeX content
    latex_content = generate_latex_resume(resume_data)

    # Write LaTeX content to file
    with open(output_file_path, 'w') as latex_file:
        latex_file.write(latex_content)

    print(f"LaTeX resume has been generated and saved to {output_file_path}")


def generate():
    """
    Generates a resume from a JSON file and converts it to PDF.
    """
    render_resume("outputs/json/resume.json", "outputs/latex/output_resume.tex")
    render_latex_to_pdf("outputs/latex/output_resume.tex", "outputs/pdf")

    try:
        pdf_path = "outputs/pdf/output_resume.pdf"
        
        backend_url = os.getenv('WEBSOCKET_SERVER_BACKEND_URL', 'http://127.0.0.1:8041')
        response = requests.post(
            f'{backend_url}/sendpdf',
            headers={"Content-Type": "application/json"},
            json={"path": pdf_path}
        )
        # Check response status if needed
        if response.status_code == 200:
            logger.info("PDF path sent successfully.")
        else:
            logger.info(f"Failed to send PDF path. Response: {response.text}")
    except Exception as e:
        logger.error(f"Exception when sending pdf {e}")
        
def generate_from_data(d: dict):
    """
    Generates a resume from a JSON d and converts it to PDF.
    """
    
    json_path = "outputs/json/temp_cache.json"
    with open(json_path, 'w') as f:
        json.dump(d, f, indent=2)
    
    logging.info(f"Saved input data to {json_path}")
    
    render_resume(json_path, "outputs/latex/output_resume.tex")
    _ = render_latex_to_pdf("outputs/latex/output_resume.tex", "outputs/pdf")

    try:
        pdf_path = "outputs/pdf/output_resume.pdf"
        backend_url = os.getenv('WEBSOCKET_SERVER_BACKEND_URL', 'http://127.0.0.1:8041')
        response = requests.post(
            f'{backend_url}/sendpdf',
            headers={"Content-Type": "application/json"},
            json={"path": pdf_path}
        )

        if response.status_code == 200:
            logger.info("PDF path sent successfully.")
        else:
            logger.info(f"Failed to send PDF path. Response: {response.text}")
    except Exception as e:
        logger.error(f"Exception when sending pdf {e}")

if __name__ == "__main__":
    generate()