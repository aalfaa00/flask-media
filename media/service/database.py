from datetime import datetime
from email.policy import default
import uuid
from flask_mongoengine import MongoEngine
from marshmallow import Schema, fields


db = MongoEngine()

class MediaService(db.Document):
    uid = db.UUIDField(binary=False)
    created_at = db.DateTimeField(default=datetime.now())
    assigned = db.BooleanField(default=False)
    file = db.FileField(upload_to="upload/files/")
    file_url = db.StringField()
    

class MediaServiceSchema(Schema):
    file_url = fields.String()
    class Meta:
        model = MediaService
        fields = ['uid', 'created_at', 'assigned', 'file_url']