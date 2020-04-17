from Cooking.models import User, Recipe, Ingredient, Step
from Cooking import db
from flask import jsonify
from flask_marshmallow import Marshmallow


def rGetRecipe(recipeName):
    recipe = Recipe.query.filter_by(name=recipeName).first()
    return recipe


def rGetAllRecipes():
    recipes = Recipe.query.all()
    return recipes


def rPostRecipe(inputRecipe):
    if(inputRecipe['image'] == ""):
        rec = Recipe(name=inputRecipe['name'])
    else:
        rec = Recipe(name=inputRecipe['name'],image=inputRecipe['image'], path=inputRecipe['absoluteURL'], is_local =inputRecipe['isLocal'])
    db.session.add(rec)
    db.session.commit()
    createdRecipe = Recipe.query.filter_by(name=inputRecipe['name']).first()
    return createdRecipe


def rPostIngredient(inputIngredients, id):
    for ing in inputIngredients:
        currentIngredient = Ingredient(name=ing,Recipe_id=id)
        db.session.add(currentIngredient)
    db.session.commit()


def rPostSteps(inputSteps, id):
    for step in inputSteps:
        currentStep = Step(text=step,Recipe_id=id)
        db.session.add(currentStep)
    db.session.commit()


def rSearchRecipe(recipeName):
    #return all Recipes that start with the same first letter
    firstLetter = recipeName[0]+"%"
    sameFirstLetter = Recipe.query.filter(Recipe.name.like(firstLetter)).all()
    results = set(sameFirstLetter)

    #return all Recipes that include any word inside the searched term
    allWords = recipeName.split()
    for word in allWords:
        query = "%" + word + "%"
        sameWord =  Recipe.query.filter(Recipe.name.like(query)).all()
        makeSet = set(sameWord)
        results.update(makeSet)

    #return any Recipe that has a different first letter but the rest is identical
    replaceFirst="_"
    for i in range(1,len(recipeName)):
        replaceFirst = replaceFirst + recipeName[i]

    replaceFirstLetter = Recipe.query.filter(Recipe.name.like(replaceFirst)).all()
    results.update(set(replaceFirstLetter))

    results = list(results)

    return results


def rDeleteRecipe(recipeName):
    toDel = Recipe.query.filter_by(name=recipeName).first()
    
    if toDel.is_local == True:
        path = toDel.path
    else:
        path = "don't delete"
    
    Recipe.query.filter_by(name=recipeName).delete()
    db.session.commit()

    return path


def rLogin(info):
    user = User.query.filter_by(email=info['email']).first()
    return user

def rChangePassword(user, newPass):
    user.password = newPass
    db.session.commit()
