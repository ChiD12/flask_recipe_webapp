from Cooking.repo import rGetRecipe, rPostRecipe, rPostIngredient,rGetAllRecipes, rPostSteps, rSearchRecipe, rDeleteRecipe, rLogin, rChangePassword
from Cooking import app
from urllib.request import Request
import secrets
import os
import urllib.request
import Levenshtein




def sGetRecipe(recipeName):
    recipe = rGetRecipe(recipeName)
    print(recipe)
    ing = recipe.ingredients
    parsedIngredients =[]
    for ingredient in ing:
        parsedIngredients.append(ingredient.name)
    steps = recipe.steps
    parsedSteps =[]
    for step in steps:
        parsedSteps.append(step.text)
    dictRecipe = {"name": recipe.name, "image": recipe.image, "ingredients":parsedIngredients, "steps": parsedSteps,"date":recipe.date_posted}
    return dictRecipe

def sGetAllRecipes():
    recipes = rGetAllRecipes()
    dicts = []

    dicts = parseResults(recipes, dicts)

    print(dicts)
    return dicts

def sSearchRecipes(recipeName):
    recipes = rSearchRecipe(recipeName)
    dicts = []

    print(recipes)
    dicts = parseResults(recipes, dicts)
    dicts = sortByStringDist(dicts, recipeName)
    return dicts

def sPostRecipe(givenRecipe):
    givenRecipe['name'] = givenRecipe['name'].casefold()
    
    paths = downloadImage(givenRecipe['image'])
    
    #if there exists an image keep the relative path, absolute path and if the file was downloaded or not
    if(givenRecipe['image'] != ""):
        givenRecipe['image'] = paths[0]  
        givenRecipe['absoluteURL'] = paths[1]
        givenRecipe['isLocal'] = paths[2]

    createdRecipe = rPostRecipe(givenRecipe)
    createdRecipeID = createdRecipe.id

    print(createdRecipe)
    rPostIngredient(givenRecipe['ingredients'], createdRecipeID)
    rPostSteps(givenRecipe['steps'], createdRecipeID)


def sDeleteRecipe(recipeName):
    path = rDeleteRecipe(recipeName)
    if path != "don't delete":
        if os.path.exists(path):
            os.remove(path)

    return f"Deleted {recipeName} successfully"

def sLogin(info):
    user = rLogin(info)
    if user and user != None:
        if user.email == info['email'] and user.password == info['password']:
            return user
    return 

def sFindUser(email):
    user = rLogin({'email': email})
    info = {}
    if user and user != None:
            return user
    return 

def sChangePassword(user, newPass):
    rChangePassword(user, newPass)

def downloadImage(URL):
    print("got to service")
    path = "../static/img/"
    #gives the image a random 8 character name so there arent any name conflicts
    random = secrets.token_hex(8)
    _, ext = os.path.splitext(URL)
    fileName = random + ext

    relativePath = path + fileName
    absolutePath = os.path.join(app.root_path, 'static\img', fileName)
    print(URL)
    print(absolutePath)

    #if theres an issue downloading the image we just use a direct link to the image hosted on another site instead
    try:
        urllib.request.urlretrieve(URL, absolutePath)
        isLocal = True
    except:
        relativePath = URL
        isLocal = False

    paths = [relativePath, absolutePath, isLocal]

    return paths

#Given a list of Recipe objects, puts every ingredient and step into their own list, and returns a list of dictionaries
def parseResults(recipes, dicts):
    for recipe in recipes:
        ing = recipe.ingredients
        parsedIngredients =[]
        for ingredient in ing:
            parsedIngredients.append(ingredient.name)
        steps = recipe.steps
        parsedSteps =[]
        for step in steps:
            parsedSteps.append(step.text)
        dictRecipe = {"name": recipe.name, "image": recipe.image, "ingredients":parsedIngredients, "steps": parsedSteps,"date":recipe.date_posted, "id": recipe.id}
        dicts.append(dictRecipe)

    return dicts

def sortByStringDist(someList, base):
    for i in range(0,len(someList)):
        distance = Levenshtein.distance(someList[i]['name'], base)
        print(someList[i]['name'])
        print(distance)
        index = someList[i]
        j = i
        while j>0 and Levenshtein.distance(someList[j-1]['name'], base) > distance:
            someList[j] = someList[j-1]
            j = j-1
        someList[j] = index
        
    return someList




