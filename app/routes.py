from flask import render_template, flash, redirect, url_for, request, redirect, jsonify
from app import app, db
from app.forms import EditItemForm, DeleteItemForm, AddItemForm, AddCategoryForm
from app.models import Item, Category 

# --------------------------------------
# OAUTH IMPORTS
# --------------------------------------
from flask import session as login_session
import random 
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# --------------------------------------
# OAUTH VARIABLES: CLIENT_ID, APPLICATION_NAME
# --------------------------------------

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Item Application"

@app.route('/')
@app.route('/catalog/')
def index():
	categories = Category.query.all()
	items = Item.query.all()
	return render_template('index.html', title='Catalog App', categories=categories, items=items)

# --------------------------------------
# ROUTES
# --------------------------------------

# --------------------------------------
# Shows all categories, plus the items of the category that is selected
# --------------------------------------

@app.route('/catalog/<category_id>/items/')
def category(category_id): 
	categories = Category.query.all()
	category = Category.query.get(category_id)
	items = Item.query.filter_by(category=category)
	return render_template('category.html', title='Catalog App', categories=categories, items=items) 

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
def edit(item_id):
	form = EditItemForm()
	item = Item.query.get(item_id)
	if form.validate_on_submit(): 
		item.title = form.title.data
		item.description = form.description.data
		item.category = form.opts.data
		db.session.commit()
		flash('Your changes: (Title: {}, Description: {}, Category: {}) have been saved!'.format(item.title, item.description, item.category.title))
		return redirect(url_for('index'))
	elif request.method == 'GET':
		form.title.data = item.title 
		form.description.data = item.description
		form.opts.data = item.category
	return render_template('edit.html',title='Edit Item',form=form)

# --------------------------------------
# Shows the delete form of the item that is selected
# --------------------------------------

@app.route('/catalog/<item_id>/delete/', methods=['GET', 'POST'])
def delete(item_id):
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

@app.route('/catalog/add/', methods=['GET','POST'])
def add():
	form = AddItemForm()
	if form.validate_on_submit(): 
		db.session.add(Item(title=form.title.data, description=form.description.data, category=form.opts.data))
		db.session.commit()
		flash('Your item was added!')
		return redirect(url_for('index'))
	elif request.method == 'GET':
		return render_template('edit.html',title='Edit Item', form=form)

# --------------------------------------
# Shows the form to add a category 
# --------------------------------------

@app.route('/catalog/add_category/', methods=['GET', 'POST'])
def add_category(): 
	form = AddCategoryForm()
	if form.validate_on_submit(): 
		db.session.add(Category(title=form.title.data))
		db.session.commit()
		flash('Your category was added!')
		return redirect(url_for('index'))
	elif request.method == 'GET':
		return render_template('add_category.html', title='Add category', form=form)


# --------------------------------------
# LOGIN FUNCTIONALITY
# --------------------------------------

# --------------------------------------
# Shows the login page
# --------------------------------------

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

# --------------------------------------
# Oauth redirect function
# -------------------------------------- 

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print( "done!")
    return output


# --------------------------------------
# JSON APIS TO SHOW CATALOG INFORMATION
# --------------------------------------


# --------------------------------------
# JSON API that shows information about all items in the catalog
# --------------------------------------

@app.route('/catalog/items/JSON')
def itemsJSON():
    items = Item.query.all()
    return jsonify(items = [i.serialize for i in items])

# --------------------------------------
# JSON API that shows information about all items in one category 
# --------------------------------------

@app.route('/catalog/category/items/<category_id>/JSON')
def categoryItemsJSON(category_id):
    category = Category.query.get(category_id)
    items = Item.query.filter_by(category = category)
    return jsonify(categoryItems = [i.serialize for i in items ])


# --------------------------------------
# JSON API that shows information about a specific item
# --------------------------------------

@app.route('/catalog/item/<item_id>/JSON')
def itemJSON(item_id): 
    item = Item.query.get(item_id)
    return jsonify(item = item.serialize)

# --------------------------------------
# JSON API that shows information about a all categories
# --------------------------------------

@app.route('/catalog/categories/JSON')
def categoriesJSON():
    categories = Category.query.all()
    return jsonify(categories = [i.serialize for i in categories])   


