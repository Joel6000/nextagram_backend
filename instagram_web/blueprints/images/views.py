from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests
import os
from models.images import Images
from models.donation import Donation
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from instagram_web.util.helpers import upload_images_to_s3, gateway
from decimal import Decimal

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')

@images_blueprint.route('/new', methods=['GET'])
@login_required
def new():
    return render_template('images/new.html')

@images_blueprint.route('/<images_id>/payment', methods=['GET'])
@login_required
def payment(images_id):
    token = gateway.client_token.generate()
    return render_template('images/payment.html', token=token, images_id=images_id)

@images_blueprint.route('/<images_id>/receive_payment', methods=['POST'])
@login_required
def pay(images_id):
    nonce= request.form["nonce"]
    amount= request.form["amount"]
    print("11111111111111111111111111111"+ nonce)
    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce,
        "options": {
        "submit_for_settlement": True
        }
    })
    if result.is_success:
        images= Images.get_by_id(images_id)
        donation = Donation (
            images=images,
            amount=Decimal(amount)
        )
        donation.save()
        requests.post(
		    f"https://api.mailgun.net/v3/{os.environ['MAILGUN_DOMAIN']}/messages",
		    auth=("api", os.environ['MAILGUN_APIKEY']),
		    data={
                "from": f"Tester <MailGun Test@{os.environ['MAILGUN_DOMAIN']}",
			    "to": ["joe_lim95@hotmail.com"],
			    "subject": "Donation",
			    "text": f"You donated ${amount}!"
            }
        )
        flash("Donation successful!")
    else:
        flash("Donation failed!")
    return redirect(url_for('users.show', username=current_user.name))

@images_blueprint.route('/images', methods=['GET'])
def images():
    pass

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
def show(id):
    pass

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