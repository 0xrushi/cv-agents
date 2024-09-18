import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with open("data/job_desc.txt", "r") as f:
    job_description = f.read()

with open('data/resume.json', 'r') as f:
    resume = json.load(f)
    
with open('outputs/json/resume.json', 'r') as f:
    resume_generated = json.load(f)    
    
    
JSON_STRUCTURE = """
{
  "basics": {
    "name": "",
    "label": "",
    "email": "",
    "phone": "",
    "url": "",
    "summary": "",
    "location": {
      "city": "",
      "countryCode": "",
      "region": ""
    },
    "profiles": [
      {
        "network": "",
        "username": "",
        "url": ""
      }
    ]
  },
  "work": [
    {
      "name": "",
      "position": "",
      "location": "",
      "startDate": "",
      "endDate": "",
      "highlights": []
    }
  ],
  "education": [
    {
      "institution": "",
      "area": "",
      "studyType": "",
      "location": "",
      "startDate": "",
      "endDate": "",
      "gpa": "",
      "courses": []
    }
  ],
  "skills": [
    {
      "name": "",
      "keywords": []
    }
  ],
  "certificates": [
    {
      "name": "",
      "issuer": "",
      "date": ""
    }
  ],
  "projects": [
    {
      "name": "",
      "description": "",
      "highlights": [],
      "keywords": [],
      "url": ""
    }
  ],
  "languages": [
    {
      "language": "",
      "fluency": ""
    }
  ],
  "interests": [
    {
      "name": "",
      "keywords": []
    }
  ]
}
"""

HR_PROMPT = f"""You are an experienced hiring manager at a top tech company, specializing in data engineering and machine learning roles. You're currently evaluating candidates for the following position:

### Job Description
{job_description}

You've received the following resume from a candidate:

### Candidate's Resume
{resume_generated}

Please provide a comprehensive evaluation of the candidate's fit for this role:

1. Overall Rating: On a scale of 1 to 10, rate how well the candidate's qualifications match the job requirements. Provide a brief explanation for your rating.

2. Strengths: Identify 3-5 key strengths in the candidate's profile that align well with the job description. For each strength, explain its relevance to the role.

3. Areas for Improvement: List 3-5 specific areas where the candidate could improve their qualifications to better match the job requirements. For each area:
   a) Explain why it's important for the role
   b) Suggest concrete actions the candidate could take to address this gap (e.g., specific certifications, projects, or experiences)

4. Missing Skills or Experiences: Identify any critical requirements from the job description that are not evidenced in the resume. Suggest how the candidate might acquire or demonstrate these skills.

5. Resume Feedback: Provide 2-3 suggestions to improve the resume's presentation or content to better highlight the candidate's relevant qualifications for this specific role.


Please ensure your feedback is constructive, specific, and actionable, focusing on how the candidate can improve their chances for this particular role."""



EDITOR_PROMPT = f"""As an expert resume editor, optimize the crafted resume based on the original resume and hiring manager feedback. Your goal is to create a tailored, one-page resume.

Crafted resume:
{resume_generated}

Original resume:
{resume}

Steps:
1. Prioritize key experiences and skills aligned with hiring manager feedback.
2. Edit and refine:
   - Restructure to {JSON_STRUCTURE} format
   - Highlight key points
   - Condense content, focus on achievements and relevant skills
   - Use 'save_resume_json' tool with updated JSON string

3. Optimize layout:
   - Use 'generate_resume' tool
   - Verify page count with 'pdf_comparison_tool'

4. Iterate if necessary:
   - If over one page: Condense further
   - If under one page: Expand slightly
   - Repeat steps 2-3 until it fits one page perfectly

5. Review final resume:
   - Ensure professional appearance and effective communication of value
   - Verify key points from hiring manager feedback are featured

IMPORTANT: Use 'save_resume_json' tool to save final resume data as a valid JSON string. Report the save operation result in your final response.
"""


YOU_PROMPT = f"""You are an experienced software engineer seeking to optimize your job application process. Your goal is to refine your resume until it achieves a rating of at least 8.5 out of 10 from a hiring manager. Follow these steps:

1. Initial Contact with HR:
   - Reach out to your HR contact, who has insight into the hiring process.
   - Request the current rating of your resume on a scale of 1 to 10.

2. Evaluation Loop:
   - If the resume rating is less than 8.2:
     a) Thank your HR contact for their feedback.
     b) Proceed to step 3 (Resume Refinement).
   - If the resume rating is 8.5 or higher:
     a) Express gratitude for the positive feedback.
     b) Proceed to step 4 (Finalization).

3. Resume Refinement:
   - Connect with an experienced resume editor.
   - Share the current resume and the feedback received from HR.
   - Request specific improvements to address the areas that likely lowered your rating.
   - Once you receive the revised resume, return to step 1 to get a new rating from HR.

4. Finalization:
   - Once your resume achieves a rating of 8.5 or higher exit.

5. Documentation:
   - Keep a record of the feedback received and changes made in each iteration.
   - Note the final resume rating and any additional insights gained through this process.

Continue this iterative process until you have a resume rated 8.5 or higher. Your output should include:
1. The final resume rating
2. A summary of key improvements made
3. Any additional insights or recommendations from your HR contact for the application process

Remember to maintain a professional and appreciative tone in all interactions, and use each piece of feedback as an opportunity for improvement."""