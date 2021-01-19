from models.base_model import BaseModel
from models.user import User
import peewee as pw
from playhouse.hybrid import hybrid_property

class Images(BaseModel):
    user = pw.ForeignKeyField(User, backref='images', on_delete="CASCADE")
    photo_url=pw.TextField(null=True)

    @hybrid_property
    def images_url(self):
        if self.photo_url:
            from app import app
            return app.config.get('S3_LOCATION') + self.photo_url