# LOCAL DEPLOYMENT
pipenv shell
pipenv install
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata apps/company/fixtures/data.json
python manage.py loaddata apps/recruitment/fixtures/data.json
python manage.py create_groups_permissions --app=company
python manage.py runserver