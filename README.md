# Catalog App 
**Udacity Fullstack Nanodegree**

## Description

The Catalog App is a RESTful web application using the Python framework Flask.

The application provides a list of items within a variety of categories as well as a user registration and authentication system through third-party provider Google. Registered users have the ability to post, edit and delete their own items and categories when logged in.

![image](https://user-images.githubusercontent.com/14871980/64073928-f5ad7800-cca4-11e9-89e6-d76020d08dc9.png)

## Skills used 

- Python 
- Flask + Packages
- SQLAlquemy 
- HTML 
- CSS
- Bootstrap 
- OAuth2 (Google)

## Executing this project 
1 - Make sure you have [Python](https://www.python.org/downloads/) installed.
2 -  Clone this repository 
3 - Create the file `.flaskenv` in the parent directory of the
application, paste the following lines of codes and sustitute the variables GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET with your Google API Keys. 

```
FLASK_APP = catalog.py
GOOGLE_CLIENT_ID = "YOUR_CLIENT_ID"
GOOGLE_CLIENT_SECRET = "YOUR_CLIENT_SECRET"
OAUTHLIB_INSECURE_TRANSPORT = 1
```

4 - Run Python virtual environment 
```
$ source venv/Scripts/activate
```

5 - Run application  
```
$ flask run
```
6 - Navigate to `localhost:5000` in the browser


## Environment
-- **Not mandatory** --
The environment files are stored in the venv folder. So with cloning this repository, the correct environment is set up for you. 

However, if you want to set it up yourself, here is how:

You need to set up: 

- Python Virtual Environment 
- Flask + Packages


### Setting up the virtual environment 

If you are using Python 3, virtual environment support is included. So in your application repository, run the command: 
```
$ python3 -m venv venv
```
In some operating systems you may need to use `python` instead of `python3`. 
With this command, Python runs the venv package, which creates a virtual environement named venv. The first venv is the name of the Python package, the second is the name that you are using for this particular environment.  

> If you are using any version of Python older than 3.4, virtual environments are not supported natively. Update your python version or use [Virtualenv](https://virtualenv.pypa.io/en/latest/) instead.

To activate your virtual environment, use the following commands
```
$ source venv/bin/activate
```` 
On Windows it looks like this: 
```
$ source venv\Scripts\activate
```

### Installing Flask and further packages

Python comes with a tool called `pip` which enables you to install packages from the Python Package Index (PyPI). 
> In Python 2.7 pip does not come bundled with Python and needs to be installed separately.

Install all packages by running the command: 

```
(venv) $ pip install requirements.txt
```

To seperately install the packages in the requirements.txt, run `pip install <packagename>`

For example, install flask by running the command: 

```
(venv) $ pip install flask
```

To see if Flask is installed either run the command `pip list` to see which packages have been installed or start the Python interpreter with `python` and importing flask by running `import flask`. If this does not provide you with an error, your flask installation was successful. 

#### Installed packages (requirements.txt)
The following packages should be installed in your virtual environment. Listed dependencies are installed automatically.  

| Package              | Version | Description| Dependencies|
|----------------------|---------|-----------|--------------|
| Flask                | 1.1.1  |  Flask automatically installs | itsdangerous, Jinja2, MarkupSafe, Werkzeug, Click|
| python-dotenv        | 0.10.3 |  Allows for environement variables to be automatically imported when the flask command is run.| 
| Flask-WTF            | 0.14.2 | For handeling forms. It is a thin wrapper around the WTForms package.|
| Flask-SQLAlchemy     | 2.4.0  | ORM for relational databases
| Flask-Migrate        | 2.5.2 | Flask wrapper for Alembic. A database migration framework for SQLAlchemy. |  alembic, Mako, python-dateutil, pythoneditor, six |
| requests | 2.22.0  | HTTP library | urllib3, idna, certifi, chardet, requests |
| pyOpenSSL | 19.0.0 | Python wrapper module around the OpenSSL library | asn1crypto-0.24.0, cffi-1.12.3, cryptography-2.7, pycparser-2.19 |
| oauthlib | 3.1.0 | OAuthLib is a framework which implements the logic of OAuth1 or OAuth2 |
| flask-login | 0.4.1 | Provides user session management | 
| pycodestyle | 2.5.0 | Checks [Python Style Guide requirements](https://www.python.org/dev/peps/pep-0008/) 




## JSON Endpoints 
The following JSON endpoints are provided.

|Endpoint                                    |  Description                         |
|--------------------------------------------|--------------------------------------|
|/catalog/items/JSON                         | Returns all items within the catalog |
|/catalog/category/items/<category_id>/JSON  | Returns all items within a category  |
|/catalog/item/<item_id>/JSON                | Returns a specific item              |
|/catalog/categories/JSON                    | Returns all categories               |

## Credits 
[Udacity Full Stack Web Developer Nano Degree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004)
[Create a Flask Application With Google Login by Real Python](https://realpython.com/flask-google-login/)
[Flask Mega-Tutorial by Miguel Grinberg](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)