# System Overview
The recruitment system is a comprehensive platform designed to streamline the hiring process for organizations. It leverages modern technologies such as Docker, Redis, and PostgreSQL to provide a scalable, efficient, and secure solution. 

At its core, the system facilitates the entire recruitment lifecycle, from job posting and candidate sourcing to interview scheduling, evaluation, and onboarding. Users, including recruiters, hiring managers, and candidates, interact with the system through a user-friendly interface, which offers intuitive navigation and robust functionality.

Key features of the recruitment system include:

1. **Job Management:** Recruiters can create, manage, and post job openings, specifying job details, requirements, and qualifications.

2. **Candidate Management:** The system allows recruiters to track and manage candidate applications, including resume parsing, candidate screening, and communication management.

3. **Interview Management:** Recruiters can schedule interviews, coordinate with hiring teams, and collect feedback through the system, streamlining the interview process.

4. **Assessment and Evaluation:** The system provides tools for evaluating candidates, including assessment tests, interview feedback, and candidate scoring mechanisms.

5. **Collaboration:** Hiring teams can collaborate effectively within the system, sharing candidate profiles, scheduling meetings, and exchanging feedback.

6. **Analytics and Reporting:** The system offers analytics and reporting capabilities, providing insights into recruitment metrics, such as time-to-hire, candidate pipeline, and hiring effectiveness.

7. **Integration:** Integration with external services, such as job boards, HR systems, and background check providers, enhances the system's functionality and interoperability.

The recruitment system is built on a robust architecture, utilizing Docker for containerization, Redis for caching and session management, and PostgreSQL for data storage. This architecture ensures scalability, reliability, and performance, enabling the system to handle large volumes of job postings, candidate applications, and user interactions.

Overall, the recruitment system streamlines and automates the hiring process, improving efficiency, reducing time-to-hire, and enhancing the overall candidate experience. Its modern technology stack, coupled with intuitive features and robust architecture, makes it a valuable asset for organizations looking to optimize their recruitment efforts.








# Make sure you have the latest version of python install

# Install virtual environment
### If you do not have pipenv installed
pip install pipenv

# Install dependencies
pipenv install

# While in your virtual environment 
## Collect Staticfiles
python manage.py collectstatic


## Apply migrations
- python manage.py makemigrations
- python manage.py migrate
- python manage.py createcachetable cache_table

## Create superuser
python manage.py createsuperuser

## Visualising the models
### If you want to see the models and how they interact
python manage.py graph_models -a > my_project.dot
### Paste the contents of the file generated on this online editor
https://edotor.net/

# Load initial data
- python manage.py loaddata apps/company/fixtures/data.json
- python manage.py loaddata apps/recruitment/fixtures/data.json

# Run the server
## Settings
### For local environment
python manage.py runserver --settings=rms.settings.dev

### To set environment so you do not keep adding settings flag
### For Linux/Mac
export DJANGO_SETTINGS_MODULE=rms.settings.dev
### For Windows
set DJANGO_SETTINGS_MODULE=rms.settings.dev

### To access the admin panel go to: 127.0.0.1:8000/admin
