import peewee as pw
from models.user import User
from models.base_model import BaseModel

class Follow(BaseModel):
    follower= pw.ForeignKeyField(User, backref="followings")
    following= pw.ForeignKeyField(User, backref="followers")
    approved= pw.BooleanField(default=False)

    # def validate(self):
        
    #     followed = Follow.get_or_none(Follow.following == self.following)
    #     if followed:
    #         self.errors.append("Followed!")