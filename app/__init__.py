# app/__init__.py

from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort
from flask_restful import Api
from flask import Flask
from flask_marshmallow import Marshmallow
# local import
from instance.config import app_config
from extension import db

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('../instance/config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    register_extensions(app)
    ma = Marshmallow(app)
    api = Api(app)
    from backendApi import FeatureResource as featureDataResource
    from backendApi import FeatureMetaDataResource as metaDataResource
    api.add_resource(featureDataResource, '/api/v1/feature', '/api/v1/feature/<int:feature_id>')
    api.add_resource(metaDataResource, '/api/v1/meta')
    from views import pages
    app.register_blueprint(pages)
    return app

def register_extensions(app):
    db.init_app(app)