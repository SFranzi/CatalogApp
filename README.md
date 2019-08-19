# Catalog App 
**Udacity Fullstack Nanodegree**

## Description

The Catalog App is a RESTful web application using the Python framework Flask.

The application provides a list of items within a variety of categories as well as a user registration and authentication system through third-party provider Google. Registered users have the ability to post, edit and delete their own items and categories. 

## Skills used 

- PYthon 
- HTML 
- CSS
- Bootstrap 
- Flask + Packages
- SQLAlquemy 
- OAuth2 

## Executing this project 

1. Clone this repository 
2. Install required environment
3. Run virtual environement
4. Run application with `flask run`
5. Navigate to `localhost:5000` in the browser
6. Add categories and items to populate database

## Environment 

To run this code you will need the following environement: 

- Python [Installation](https://www.python.org/downloads/)
- Virtual Environment 
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

To install all required packages run `pip install requirements.txt`. 
The following packages should be installed in your virtual environment. 

| Package              |    Version | Description
-----------------------|------------|------------

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
