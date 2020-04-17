Instructions to Run
1. go to the proper folder in terminal
2. run: pip install -r requirements.txt
3. run: python run.py



Notes on features

POST RECIPE

-Name is searched by name so each name must be unique or will return an error
-Image can be left empty and a default image will be placed, otherwise paste a url. The image will be attempted to be downloaded, if there are errors such as
the site blocking the library I am using then the URL to the image will be stored instead
-will accepts as many ingredients or steps given but must be at least one and no form can be left empty if created

DELETE RECIPE
-Only accessible when logged in
-uses search method to return similar names to one entered (more in search section)
-Clicking on the delete button in either the cards or the table will delete the recipe from the database
-This will also try to delete the corresponding image from the file structure, but this uses an absolute path so might not work on TA's computer

SEARCH 

-Finds all recipes that start with same name as search term, contain any words inside search term, or if they match the term with a different first letter
then are sorted by string distance

FORGOT PASSWORD(accessible from Login page)

-If there is an account with that email, will send an email to that email with a token to reset password(to be shown in demo as TA wont have access to my email)

If you absolutely must test this here are instructions to create another admin account through the terminal as there are no registration

1. go to the proper folder in terminal
2. go into the python interpreter by typing python
3. run the following commands:
    from Cooking import db
    from Cooking.models import Recipe, Ingredient, Step, User, Role, UserRoles
    user1 = User(
    username='user007', email='YOUR_EMAIL_HERE',
    password='password')
    user1.roles = [admin_role,]
    db.session.add(user1)
    db.session.commit()



