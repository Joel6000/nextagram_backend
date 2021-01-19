from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.images import Images
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from instagram_web.util.helpers import upload_images_to_s3

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')

@images_blueprint.route('/new', methods=['GET'])
@login_required
def new():
    return render_template('images/new.html')

@images_blueprint.route('/images', methods=['GET'])
def images():
    return 

@images_blueprint.route('/', methods=['POST'])
def create():
    pass

@images_blueprint.route('/login', methods=['POST'])
def login():
    pass

@images_blueprint.route('/logout', methods=['POST'])
def logout():
    pass

@images_blueprint.route('/<id>', methods=["GET"])
def show():
    return 

@images_blueprint.route('/user/<int:id>/edit', methods=["POST"])
def edit_info(id):
    pass
    
@images_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"

@images_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass

@images_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass

@images_blueprint.route('/<id>/upload', methods=['POST'])
@login_required
def upload(id):
    # Upload Image

    if "images_file" not in request.files:
        flash("No file selected")
        return redirect(url_for('users.show', username=current_user.name))

    file= request.files["images_file"]

    file.filename = secure_filename(file.filename)

    image_path = upload_images_to_s3(file, current_user.name)
    images_upload= Images(
            photo_url= image_path,
            user=current_user.id
    )

    if images_upload.save():
        flash("Upload sucess!")
        return redirect(url_for('users.show', username=current_user.name))
    else:
        flash("Upload failed!")
        return redirect(url_for('users.show', username=current_user.name))