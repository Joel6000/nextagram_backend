from models.base_model import BaseModel
import peewee as pw
import re
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from playhouse.hybrid import hybrid_property

class User(UserMixin,BaseModel):
    name = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique=False, null=False)
    password_hash = pw.TextField(null=False)
    password = None
    image_path=pw.TextField(null=True)
    private_profile=pw.BooleanField(default=False)
    
    @hybrid_property
    def followers(self):
        from models.follow import Follow
        followers= Follow.select(Follow.following).where(Follow.follower == self.id, Follow.approved == True)
        return User.select().where(User.id.in_(followers))

    @hybrid_property
    def followings(self):
        from models.follow import Follow
        followings= Follow.select(Follow.follower).where(Follow.following == self.id, Follow.approved == True)
        return User.select().where(User.id.in_(followings))

    @hybrid_property
    def follower_requests(self):
        from models.follow import Follow
        followers= Follow.select(Follow.following).where(Follow.follower == self.id, Follow.approved == False)
        return User.select().where(User.id.in_(followers))

    @hybrid_property
    def following_requests(self):
        from models.follow import Follow
        followings= Follow.select(Follow.follower).where(Follow.following == self.id, Follow.approved == False)
        return User.select().where(User.id.in_(followings))

    @hybrid_property
    def profile_image_url(self):
        if self.image_path:
            from app import app
            return app.config.get('S3_LOCATION') + self.image_path

    def validate(self):
        duplicate_username = User.get_or_none(User.name == self.name)
        if duplicate_username and duplicate_username.id!=self.id:
        # if duplicate_username:    
            self.errors.append("Username has been taken!")
        if self.email:
            duplicate_email= User.get_or_none(User.email == self.email)
            if duplicate_email and duplicate_email.id!=self.id:
            # if duplicate_email:
                self.errors.append("Email has been taken!")
        if self.password:
            if len(self.password) < 6:
                self.errors.append("Password requires more than 6 characters.")
            has_lower=re.search(r'[a-z]',self.password)
            has_upper=re.search(r'[A-Z]',self.password)
            has_special=re.search(r'[\[ \] \@ \# \$ \% \^ \& \* \( \)]', self.password)

            if has_lower and has_upper and has_special:
                self.password_hash= generate_password_hash(self.password)
            else:
                self.errors.append("Password either does not consists a single lower, upper and special characters!")
