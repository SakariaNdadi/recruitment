# Activate virtual environment
pipenv shell

# Install dependencies
pipenv install

# Collect Staticfiles
python manage.py collectstatic


# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser --username admin --email admin@email.com --noinput
python manage.py changepassword admin admin


# Load initial data
python manage.py loaddata apps/company/fixtures/data.json
python manage.py loaddata apps/recruitment/fixtures/data.json

# Run the server
# python manage.py runserver
