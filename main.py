from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, name, email):
        self.name = name
        self.email = email

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# endpoint to create new user
@app.route("/user", methods=["POST"])
def add_user():
    name = request.json['name']
    email = request.json['email']
    new_user = User(name, email)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)

# endpoint to show all users
@app.route("/user", methods=["GET"])
def get_user():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

# endpoint to get user detail by id
@app.route("/user/<id>", methods=["GET"])
def user_detail(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

# endpoint to update user
@app.route("/user/<id>", methods=["PUT"])
def update_user(id):
    user = User.query.get(id)
    name = request.json['name']
    email = request.json['email']

    user.name = name
    user.email = email

    db.session.commit()
    return user_schema.jsonify(user)

# endpoint to delete user
@app.route("/user/<id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
