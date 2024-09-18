from src.agents.job_application_crew import main
import shutil
if __name__ == "__main__":
    shutil.copy('data/resume.json', 'outputs/json/resume.json')
    main()
