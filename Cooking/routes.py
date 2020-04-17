from flask import render_template, url_for, request, redirect, flash
from Cooking import app, mail
from Cooking.models import User, Recipe
from Cooking.service import sGetRecipe, sPostRecipe, sGetAllRecipes, downloadImage, sSearchRecipes, sDeleteRecipe, sLogin, sFindUser, sChangePassword
from Cooking.forms import RecipeForm, LoginForm, RequestPasswordResetForm, ResetForm
from sqlalchemy import exc
import requests
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from urllib.parse import urlparse




@app.route('/', methods=['GET'])
def index():
    recipes = sGetAllRecipes()
    return render_template("home.html", recipes=recipes)


@app.route('/recipe/entry', methods=['GET', 'POST'])
def entry():
    form = RecipeForm()
    unique = True
    if form.validate_on_submit():
        print(f"Recipe Created for name:{form.name.data} image: {form.image.data} ingredients: {form.ingredients.data} {form.ingredients}")
        
        dictBuild = {'name':(request.form.getlist('name'))[0], 'image':(request.form.getlist('image'))[0], 
        'ingredients':(request.form.getlist('ingredients')), 'steps':(request.form.getlist('steps')) }
        print(dictBuild)
        
        #makes sure name is unique, if not DB will throw an error and we will send user back to form
        try:
            sPostRecipe(dictBuild)
        except exc.IntegrityError as e:
            print("not unique")
            print(e)
            unique = False
            return render_template("form_add_recipe.html", form=form, unique=unique)

        flash("Recipe Created Successfully", "success")
        return redirect(f'/recipe/{dictBuild["name"]}')
    
    return render_template("form_add_recipe.html", form=form, unique=unique)


@app.route('/recipe/<recipeName>')
def recipes(recipeName):
    recipe = sGetRecipe(recipeName)
    return render_template("recipegeneric.html", recipe=recipe)


@app.route('/search', methods=['POST'])
def Search():
    recipeName =request.form.getlist('search')[0].casefold()
    recipes = sSearchRecipes(recipeName)

    return render_template("search.html", recipes=recipes)


@app.route('/delete', methods=['GET', 'POST'])
@login_required
def deleteForm():
    if request.method == 'POST':
        #Populate the template with results from search
        if request.form.getlist('delete'):
            recipeName =request.form.getlist('delete')[0].casefold()
            recipes = sSearchRecipes(recipeName)
            return render_template("delete_return.html", recipes = recipes)

        #Recipe is chosen do actual delete
        elif request.form.getlist('deletethis'):
            recipeName =request.form.getlist('deletethis')[0].casefold()
            didItDelete = sDeleteRecipe(recipeName)
            flash(f'Recipe for {recipeName} has been deleted', 'success')
            return redirect(url_for('index'))
    
    #render a page with a search form
    return render_template("delete_form.html")

#only valid admin account is email:daniel.chid@gmail.com password:password1
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        info = {'email': form.email.data, 'password': form.password.data, "remember": form.remember.data}
        user = sLogin(info)

        if user and user != None:
            login_user(user, remember=form.remember.data)
            flash(f"Logged in as {form.email.data}", 'success')
            return redirect(url_for('index'))

        else:
            flash ('Login Unsuccessful, Invalid email or password', 'danger')

    return render_template("form_login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#route to request an email to reset password
@app.route('/reset_password', methods=['GET', 'POST'])
def request_reset():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        user = sFindUser(form.email.data)
        sendEmail(user)
        flash('Please check your Email', 'info')
        return redirect(url_for('login'))

    return render_template('form_request_reset.html', form=form)

#route that only works with valid token gotten via email
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash("Invalid Token")
        return redirect(url_for ('request_reset'))
    form = ResetForm()
    if form.validate_on_submit():
        sChangePassword(user, form.password.data)
        flash("Your password has been updated", 'success')
        return redirect(url_for('login'))

    return render_template('form_reset_password.html', form=form)

#rest api

#get all recipes
@app.route('/rest/all', methods=['GET', 'POST'])
def restgetAll():
    recipes = sGetAllRecipes()
    updateImageURL(recipes)
    dict = {'recipes': recipes}
    return dict


#Get Specific Recipe
@app.route('/rest/recipe/<recipeName>', methods=['GET', 'POST'])
def restRecipe(recipeName):
    recipeName = recipeName.casefold()
    recipe = sGetRecipe(recipeName)
    makeList = [recipe]
    updateImageURL(makeList)
    return makeList[0]
    
#use the search algorithm to return matches close to search term
@app.route('/rest/search/<recipeName>', methods=['GET', 'POST'])
def restSearch(recipeName):
    recipeName = recipeName.casefold()
    recipe = sSearchRecipes(recipeName)
    updateImageURL(recipe)
    return listToDict(recipe)


#support methods

def listToDict(lst):
    op = { i : lst[i] for i in range(0, len(lst) ) }
    return op


def sendEmail(user):
    token = user.get_reset_token()
    msg = Message("Daniels Recipes Password Reset", sender ="SOEN287Recipe@gmail.com", recipients =[user.email])

    msg.body = f'''To reset your password please click:
{url_for('reset_password', token = token, _external=True )}
This link lasts for two minutes
'''
    mail.send(msg)

#get the proper route to the image for rest api
def updateImageURL(recipes):
    for recipe in recipes:
        if recipe['image'][0] == '.':
            removeFirstTwo = ""
            for i in range(2,len(recipe['image'])):
                removeFirstTwo = removeFirstTwo + recipe['image'][i]
            recipe['image'] = urlparse(request.base_url).netloc + removeFirstTwo
            
    
    
            