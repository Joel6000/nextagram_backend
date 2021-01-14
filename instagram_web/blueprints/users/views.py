from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from werkzeug.security import check_password_hash

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')

@users_blueprint.route('/login', methods=['GET'])
def login():
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

def login():
    name = User.request.form['username'] ,
    password = User.request.form['password'] 

    check_user = User.get_or_none(User.name == name)
    password_hased = User.password_hash
    check_passsword_result= check_passsword_hash(password_hased, password)

    if check_user == True and check_passsword_result== True:
        flash("Succesfully log in!")
    else:
        flash("Login Failure")
    return redirect(url_for('users.login'))


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
