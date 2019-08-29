from flask import render_template, flash, url_for, request, redirect, jsonify
from app import app, db
from app.forms import EditItemForm, DeleteItemForm, AddItemForm, \
                      AddCategoryForm
from app.models import Item, Category, User

# --------------------------------------
# OAUTH IMPORTS
# --------------------------------------
# Python standard libraries

import json
import os

# Third-party libraries

from flask_login import current_user, login_required, login_user, logout_user
from oauthlib.oauth2 import WebApplicationClient
import requests

# --------------------------------------
# OAUTH VARIABLES: CLIENT_ID, APPLICATION_NAME
# --------------------------------------
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# --------------------------------------
# ROUTES
# --------------------------------------


@app.route('/')
@app.route('/catalog/')
def index():
    categories = Category.query.all()
    items = Item.query.all()
    return render_template('index.html', title='Catalog App',
                           categories=categories, items=items)

# --------------------------------------
# Shows all categories, plus the items of the category that is selected
# --------------------------------------


@app.route('/catalog/<category_id>/items/')
def category(category_id):
    categories = Category.query.all()
    category = Category.query.get(category_id)
    items = Item.query.filter_by(category=category)
    return render_template('category.html', title='Catalog App',
                           categories=categories, items=items)

# --------------------------------------
# Shows the desciption of the item that is selected
# --------------------------------------


@app.route('/catalog/<category_id>/<item_id>/')
def item(category_id, item_id):
    item = Item.query.get(item_id)
    return render_template('item.html', title='Catalog App', item=item)

# --------------------------------------
# Shows the edit form of the item that is selected
# --------------------------------------


@app.route('/catalog/<item_id>/edit/', methods=['GET', 'POST'])
@login_required
def edit(item_id):
    # if 'username' not in login_session:
    # return redirect('/login')
    form = EditItemForm()
    item = Item.query.get(item_id)
    if form.validate_on_submit():
        item.title = form.title.data
        item.description = form.description.data
        item.category = form.opts.data
        db.session.commit()
        flash('Your changes: (Title: {}, Description: {}, Category: {}) \
              have been saved!'.format(item.title, item.description,
              item.category.title))
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.title.data = item.title
        form.description.data = item.description
        form.opts.data = item.category
        return render_template('edit.html', title='Edit Item', form=form)

# --------------------------------------
# Shows the delete form of the item that is selected
# --------------------------------------


@app.route('/catalog/<item_id>/delete/', methods=['GET', 'POST'])
@login_required
def delete(item_id):
    # Check if user is logged in:
    # if 'username' not in login_session:
    # return redirect('/login')
    form = DeleteItemForm()
    item = Item.query.get(item_id)
    if form.validate_on_submit():
        db.session.delete(item)
        db.session.commit()
        flash('This item was deleted.')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('delete.html', title='Delete Item', form=form)

# --------------------------------------
# Shows the form to add an item
# --------------------------------------


@app.route('/catalog/add/', methods=['GET', 'POST'])
@login_required
def add():
    # Check if user is logged in:
    # if 'username' not in login_session:
    # return redirect('/login')
    form = AddItemForm()
    if form.validate_on_submit():
        db.session.add(Item(title=form.title.data,
                       description=form.description.data,
                       category=form.opts.data))
        db.session.commit()
        flash('Your item was added!')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('edit.html', title='Edit Item', form=form)

# --------------------------------------
# Shows the form to add a category
# --------------------------------------


@app.route('/catalog/add_category/', methods=['GET', 'POST'])
@login_required
def add_category():
    # Check if user is logged in:
    # if 'username' not in login_session:
    # return redirect('/login')
    form = AddCategoryForm()
    if form.validate_on_submit():
        db.session.add(Category(title=form.title.data))
        db.session.commit()
        flash('Your category was added!')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('add_category.html', title='Add category',
                               form=form)


# --------------------------------------
# LOGIN FUNCTIONALITY
# --------------------------------------

# --------------------------------------
# Shows the login page
# --------------------------------------


@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

# --------------------------------------
# Oauth callback function
# --------------------------------------


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        # picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400
    # Create a user in your db with the information provided
    # by Google
    user = User(
        id=unique_id, name=users_name, email=users_email
    )

    # Doesn't exist? Add it to the database
    if not User.query.get(unique_id):
        db.session.add(user)
        db.session.commit()

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))

# --------------------------------------
# Logout
# --------------------------------------


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

# --------------------------------------
# JSON API that shows information about all items in the catalog
# --------------------------------------


@app.route('/catalog/items/JSON')
def itemsJSON():
    items = Item.query.all()
    return jsonify(items=[i.serialize for i in items])

# --------------------------------------
# JSON API that shows information about all items in one category
# --------------------------------------


@app.route('/catalog/category/items/<category_id>/JSON')
def categoryItemsJSON(category_id):
    category = Category.query.get(category_id)
    items = Item.query.filter_by(category=category)
    return jsonify(categoryItems=[i.serialize for i in items])


# --------------------------------------
# JSON API that shows information about a specific item
# --------------------------------------


@app.route('/catalog/item/<item_id>/JSON')
def itemJSON(item_id):
    item = Item.query.get(item_id)
    return jsonify(item=item.serialize)

# --------------------------------------
# JSON API that shows information about a all categories
# --------------------------------------


@app.route('/catalog/categories/JSON')
def categoriesJSON():
    categories = Category.query.all()
    return jsonify(categories=[i.serialize for i in categories])
