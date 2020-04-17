from Cooking import db, login_manager, app
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    image = db.Column(db.String(60), nullable=False, default="../static/img/default.jpg")
    path = db.Column(db.String(60), nullable=True, default="none")
    is_local = db.Column(db.Boolean(), default=True)
    ingredients = db.relationship('Ingredient', backref='ingredients', lazy=True)
    steps = db.relationship('Step', backref='steps', lazy=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"Recipe('{self.id}', '{self.name}','{self.image}','{self.ingredients}','{self.steps}','{self.date_posted}','{self.path}','{self.is_local}' )"


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    Recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable = False)

    def __repr__(self):
        return f"Ingredient('{self.name}')"

class Step(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(120), nullable=False)
    Recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable = False)

    def __repr__(self):
        return f"Steps('{self.text}')"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    roles = db.relationship('Role', secondary='user_roles')

    #methods to create a password reset token, lasts 2 minutes
    def get_reset_token(self,expires_sec=120):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.id}', '{self.name}', '{self.email}')"

#these two are tables for account roles but never ended up being used in project
# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))