from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user import User

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['POST'])
def signup():
    print(crsf)

    new_user=User(
        name=request.json.get('name'), email=request.json.get('email'), password=request.json.get('password')
    )

    if new_user.save():
        token= create_access_token(identity=new_user.id)
        return jsonify({"token":token})
    else:
        return jsonify([err for err in new_user.errors])
    return render_template('users/new.html')