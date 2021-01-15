from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import login_required, login_user, logout_user

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')

@users_blueprint.route('/loginpage', methods=['GET'])
def loginpage():
    return render_template('users/login.html')

@users_blueprint.route('/', methods=['POST'])
def create():
    new_user = User ( 
        name = request.form['username'] ,
        email = request.form['email'], 
        password = request.form['password'] 
    )

    if new_user.save():
        flash("Succesfully sign up!")
    else:
        for error in new_user.errors:
            flash(error)
    return redirect(url_for('users.new'))

@users_blueprint.route('/login', methods=['POST'])
def login():
    name= request.form.get('username')
    password= request.form.get('password') 

    check_user = User.get_or_none(User.name == name)
    if check_user:
        check_passsword_result= check_password_hash(check_user.password_hash, password)
        if check_passsword_result:
            flash("Succesfully log in!")
            login_user(check_user)
            return redirect(url_for('home'))
        else:
            flash("Login Failure")
            return redirect(url_for('users.loginpage'))

@users_blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash("Succesfully logout!")
    return redirect(url_for('users.loginpage'))

@users_blueprint.route('/<username>', methods=["GET"])
@login_required
def show(username):
    user= User.get_or_none(User.name == username)
    if user:
        return render_template('users/userpage.html', user=user)
    else:
        flash("Please login")
        return redirect(url_for('users.loginpage'))


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
