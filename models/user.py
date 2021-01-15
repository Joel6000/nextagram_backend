from models.base_model import BaseModel
import peewee as pw
import re
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

class User(UserMixin,BaseModel):
    name = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique=False, null=False)
    password_hash = pw.TextField(null=False)
    password = None
    
    def validate(self):
        duplicate_username = User.get_or_none(User.name == self.name)
        if duplicate_username:
            self.errors.append("Username has been taken!")
        if len(self.password) < 6:
            self.errors.append("Password requires more than 6 characters.")
        has_lower=re.search(r'[a-z]',self.password)
        has_upper=re.search(r'[A-Z]',self.password)
        has_special=re.search(r'[\[ \] \@ \# \$ \% \^ \& \* \( \)]', self.password)

        if has_lower and has_upper and has_special:
            self.password_hash= generate_password_hash(self.password)
        else:
            self.errors.append("Password either does not consists a single lower, upper and special characters!")
