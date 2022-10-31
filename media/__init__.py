import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from media.service.views import media
from media.service.database import db
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
import py_eureka_client.eureka_client as eureka_client



def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY'),
           
        )
    else:
        app.config.from_mapping(test_config)
        
    app.config['MONGODB_SETTINGS'] = {
        'db': 'MediaService',
        'host': 'localhost',
        'port': 27017
    }
    
    
    upload_folder=os.path.join(app.instance_path, 'uploads/%d-%m-%Y/')
    app.config['UPLOAD_FOLDER'] = upload_folder
    # os.makedirs('uploads')

    db.app = app
    db.init_app(app)
    

    your_rest_server_port = 8888
    eureka_client.init(eureka_server="http://your-eureka-server-peer1,http://your-eureka-server-peer2",
                    app_name="your_app_name",
                    instance_port=your_rest_server_port)
    
   
    app.register_blueprint(media)
        
    return app

