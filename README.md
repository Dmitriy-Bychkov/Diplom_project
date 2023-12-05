# OB1 - Diploma project in the specialty "Python Developer"
--------------------------------------------------------------------
# The self-learning platform with test-exams for authorized users.

## Task description
Implement self-learning functionality for students. 
Create a platform that works only with authorized users. 
It is necessary to provide the functionality of sections and materials on the platform with tests for each material. 
Management of all entities must be implemented through the standard Django admin. 
The test response is checked using a separate backend request. 
Implement either the Rest API or SSR using Bootstrap. 
To implement the project, use the Django framework.

## The main technology stack
- Python 
- Django
- PostgreSQL
- Git
- Tests
- Bootstrap

## 1. Set Up your personal settings
- Create and fill out the .env configuration file in the root of the project with your personal data,
according to the sample, specified in .env.sample.

## 2. Install and acivate the virtual environment
- Install a new virtual environment if it doesn't exist:
    * pip install poetry
- Create a new Poetry virtual environment using the command:
    * poetry init
- Activate the virtual environment by running the command:
    * poetry shell
- Install all dependencies from the pyproject.toml file by running the command:
    * poetry install
  
## Project settings on your server
- Create a database in postgresql by running the commands:
  (the name of the database must match the name specified in the .env file)
    * psql -h localhost -U postgres
    * create database <your_database_name>;
    * \q
- Make migrations by running the commands:
    * python manage.py makemigrations
    * python manage.py migrate
- Create the superuser by running this command in the terminal:
    * python3 manage.py csu

## Project Tests
The global tests coverage of the project code is 78%.
- To run tests and check the coverage use this commands:
    * coverage run --source='.' manage.py test
    * coverage report

--------------------------------------------------------------------

# Run the project
- Run your server by using this command:
    * python manage.py runserver
- You can now log in to the Django administration system to manage your entities by clicking on this link:
    * http://127.0.0.1:8000/admin/

## The main working links
- The main page of the project
    * http://127.0.0.1:8000/
- The sections page
    * http://127.0.0.1:8000/sections_list/
- The materials page
    * http://127.0.0.1:8000/materials_list/
- The tests-exams page
    * http://127.0.0.1:8000/exams/exams_list/
- Sign up on the platform
    * http://127.0.0.1:8000/users/registration/
- Log in the platform
    * http://127.0.0.1:8000/users/
  
--------------------------------------------------------------------

### This project was developed by Dmitriy Bychkov using the PyCharm development environment
