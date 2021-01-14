from app import app
from flask import render_template, redirect, url_for, request, flash
from instagram_web.blueprints.users.views import users_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from models import *

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/")
def home():
    return render_template('home.html')

# @app.route("/users/new", methods=['POST'])
# def sign_up():
#     new_user = user.User ( 
#         name = request.form['username'] ,
#         email = request.form['email'], 
#         password = request.form['password'] 
#     )

#     if new_user.save():
#         flash("Succesfully sign up!")
#     else:
#         if user.User (name == new_user.name) :
#             flash("Username has been taken!")
#         if len(new_user.password) < 6:     
#             flash("Password requires more than 6 characters.")
#     return redirect(url_for('sign_up'))