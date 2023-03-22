# simple-flask-blog
This is an example of simple blog with following features:
- Log in/Log out
- Registration
- Submitting a post
- Searching posts
- Pagination
- Tags
- Dedicated admin page to modify database entities

To lauch it run the following commands:
```
pip install requirements.txt
flask --app wsgi.py run
```
There should be .env file in the root directory with following configuration parameters:
```
SECRET_KEY
DEV_SQLALCHEMY_DATABASE_URI
PROD_SQLALCHEMY_DATABASE_URI
```