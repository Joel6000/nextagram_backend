from models.base_model import BaseModel
from models.images import Images
import peewee as pw

class Donation(BaseModel):
    images = pw.ForeignKeyField(Images, backref='donations', on_delete="CASCADE")
    amount = pw.DecimalField(decimal_places=2)
