from crewai import Agent, Task, Crew, Process
from textwrap import dedent
import sys
import os
import logging
from typing import Union
# from langchain_groq import ChatGroq

current_dir = os.path.abspath(__file__)
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
sys.path.append(parent_dir)
sys.path.append(grandparent_dir)

from prompts.job_application_prompts import HR_PROMPT, EDITOR_PROMPT, YOU_PROMPT
from tools.resume_tools import generate_resume_tool, pgcount_tool, save_resume_json

# llm=ChatGroq(temperature=0.4,
#              model_name="llama3-70b-8192",
#              api_key='')


# Set up logging with datetime format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'  # Added datetime format
)
logger = logging.getLogger(__name__)

class JobApplicationCrew:
    def __init__(self):
        pass

    def run(self):
        # Define the agents
        hiring_manager = Agent(
            name="Hiring Manager",
            role="Experienced hiring manager specializing in tech roles",
            goal="Evaluate candidate resumes and provide constructive feedback",
            backstory="You have years of experience hiring for top tech companies and know exactly what makes a strong candidate. You're skilled at providing detailed feedback and accurate ratings based on job requirements.",
            verbose=True,
            allow_delegation=False,
        )

        resume_editor = Agent(
            name="Resume Editor",
            role="Expert resume editor with tech industry knowledge",
            goal="Optimize resumes based on feedback to fit on one page and highlight key qualifications",
            backstory="You've helped countless tech professionals land their dream jobs by crafting perfect resumes.",
            verbose=True,
            allow_delegation=False,
            tools=[
                generate_resume_tool,
                pgcount_tool,
                save_resume_json
            ],
        )

        job_applicant = Agent(
            name="Job Applicant",
            role="Experienced software engineer seeking a new position",
            goal="Secure a job offer by iterating on your resume until it's highly rated",
            backstory="You're a skilled engineer looking to take the next step in your career. You're determined to present yourself in the best light possible.",
            verbose=True,
            allow_delegation=True,
        )

        evaluate_resume = Task(
            description=dedent(HR_PROMPT),
            agent=hiring_manager,
            expected_output="A comprehensive evaluation report including a numerical rating, strengths, areas for improvement, missing skills, resume feedback, and a final recommendation."
        )

        edit_resume = Task(
            description=dedent(EDITOR_PROMPT),
            agent=resume_editor,
            expected_output="An optimized, one-page resume in LaTeX format that addresses the hiring manager's feedback, highlights the candidate's most relevant qualifications, and fits within the specified page limit. The output should include the revised resume content and confirmation that it meets the one-page requirement."
        )

        optimize_application = Task(
            description=dedent(YOU_PROMPT),
            agent=job_applicant,
            expected_output="""A detailed report on the resume optimization process, including:
            1. The final resume rating (which should be 8.5 or higher)
            2. A summary of key improvements made to the resume through each iteration
            3. The final, optimized resume content
            4. Any additional insights or recommendations from the Hiring Manager for the application process
            5. A brief reflection on the iterative improvement process and lessons learned"""
        )

        crew = Crew(
            agents=[hiring_manager, resume_editor, job_applicant],
            tasks=[evaluate_resume, edit_resume, optimize_application],
            verbose=True,
            process=Process.sequential
        )

        result = crew.kickoff()
        
        logger.info(crew.usage_metrics)
        logger.info(f"Token Usage: {result.token_usage}")
        
        return result
    
def main():
    job_application_crew = JobApplicationCrew()
    final_result = job_application_crew.run()
    logger.info(final_result)