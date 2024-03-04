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
python manage.py makemigrations
python manage.py migrate
python manage.py createcachetable cache_table

## Create superuser
python manage.py createsuperuser

## Visualising the models
### If you want to see the models and how they interact
python manage.py graph_models -a > my_project.dot
### Paste the contents of the file generated on this online editor
https://edotor.net/

# Load initial data
python manage.py loaddata apps/company/fixtures/data.json
python manage.py loaddata apps/recruitment/fixtures/data.json

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