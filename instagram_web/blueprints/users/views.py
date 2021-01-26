from models.user import User
from models.follow import Follow
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from instagram_web.util.google_oauth import oauth
from instagram_web.util.helpers import upload_profile_to_s3
from flask_login import login_required, login_user, logout_user, current_user
from flask import Blueprint, render_template, request, redirect, url_for, flash

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')

#Sign up page
@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')

#Login page
@users_blueprint.route('/loginpage', methods=['GET'])
def loginpage():
    return render_template('users/login.html')

#Requests page
@users_blueprint.route('/requests', methods=['GET'])
def requests():
    follow = Follow.get_or_none(Follow.following == current_user.id)
    return render_template('users/requests.html', follow=follow)

#Google login button
@users_blueprint.route("/google_login")
def google_login():
    redirect_uri = url_for('users.authorize', _external = True)
    return oauth.google.authorize_redirect(redirect_uri)

#Google login page function
@users_blueprint.route("/authorize/google")
def authorize():
    oauth.google.authorize_access_token()
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.get_or_none(User.email == email)
    if user:
        login_user(user)
        return redirect(url_for('users.show', username=user.name))
    else:
        return redirect(url_for('users.new'))

#Sign up func
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

#Login func
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
    else:
        flash("No such user")
        return redirect(url_for("users.loginpage"))

#Logout func
@users_blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash("Succesfully logout!")
    return redirect(url_for('users.loginpage'))

#Follow function
@users_blueprint.route('/follow/<id>', methods=["POST"])
@login_required
def follow(id):

    user = User.get_or_none(User.id == id)

    if user.private_profile == True:
        follow = Follow (
            follower= current_user.id,
            following= user.id
        )
        if follow.save():
            flash(f'Follow request sent to {user.name}!')
        else:
            for error in follow.errors:
                flash(error)
    else:
        follow = Follow (
            follower= current_user.id,
            following= user.id,
            approved= True
        )
        if follow.save():
            flash(f'Succesfully followed {user.name}!')
        else:
            for error in follow.errors:
                flash(error)
    return redirect(url_for('users.show', username=user.name))

#Unfollow function
@users_blueprint.route('/unfollow/<uid>/<id>', methods=["POST"])
@login_required
def unfollow(uid, id):

    user = User.get_or_none(User.id == uid)
    unfollow=Follow.get_by_id(id)

    if unfollow.delete_instance(recursive=True):
        flash("Unfollowed!")
        return redirect(url_for('users.show', username= user.name))
    else:
        flash("Error!")
        return redirect(url_for('users.show', username= user.name))

#Approve function
@users_blueprint.route('/approve/<id>', methods=['POST'])
@login_required
def approve(id):

    approve=Follow(
        id=id, 
        approved=True
    )

    if approve.save(only=[Follow.approved]):
        flash("Approval approved!")
        return redirect(url_for('users.show', username=current_user.name))
    else:
        flash("Error")
        return redirect(url_for('users.show', username=current_user.name))

#User page
@users_blueprint.route('/<username>', methods=["GET"])
@login_required
def show(username):
    user= User.get_or_none(User.name == username)
    if user:
        follow = Follow.get_or_none(Follow.following == user.id)
        return render_template('users/userpage.html', user=user, follow=follow)
    else:
        flash("Please login")
        return redirect(url_for('users.loginpage'))

#Edit User Profile
@users_blueprint.route('/user/<int:id>/edit', methods=["POST"])
@login_required
def edit_info(id):
    
    user = User.get_or_none(User.id == id)
    if user:
        if current_user.id == int(id):
    
            name= request.form.get("edit_name")
            email= request.form.get("edit_email")
            password= request.form.get("edit_password")
            user.private_profile= True if request.form.get("checkbox") == "on" else False
            
            if len(name) > 0:
                user.name = name

            if len(password) > 0:
                user.password = password
            
            if len(email) > 0 :
                user.email = email

            if user.save():
                flash("Details updated")
                return redirect(url_for('users.show', username = user.name))
            else:
                for error in user.errors:
                    flash(error)
                return redirect(url_for('home'))
            

@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"

#Edit page
@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    user = User.get_or_none(User.id == id)
    if user:
        if current_user.id == int(id):
            return render_template('users/editinfo.html', user=user)
    else:
        flash("Please login")
        return redirect(url_for('users.loginpage'))

@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass

#Upload profile image func
@users_blueprint.route('/<id>/upload', methods=['POST'])
@login_required
def upload(id):
    user= User.get_or_none(User.id ==id)
    if user:
        if current_user.id == int(id):
            # Upload Image
            if "user_file" not in request.files:
                flash("No file selected")
                return redirect(url_for('users.show', username=user.name))

            file= request.files["user_file"]

            file.filename = secure_filename(file.filename)

            image_path = upload_profile_to_s3(file, user.name)
            
            user.image_path= image_path

            if user.save():
                flash("Upload sucess!")
                return redirect(url_for('users.show', username=user.name))
            else:
                flash("Upload failed!")
                return redirect(url_for('users.show', username=user.name))
        else:
            flash("Unable to edit other profiles")
            return redirect(url_for('users.show', username=user.name))
    else:
        flash("No such user!")
        return redirect(url_for('home'))
                