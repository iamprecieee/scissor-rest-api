from flask import Flask
from flask_smorest import Api

from resources.db import db
from resources.config import Config

from resources.shorturl import blp as ShortUrlBlueprint
from resources.customurl import blp as CustomUrlBlueprint
from resources.redirection import blp as RedirectionBlueprint
from resources.qrcode import blp as QRBlueprint
from resources.analytics import blp as AnalyticsBlueprint


def create_app(config_class=Config):
    
    app = Flask(__name__)
    
    app.config.from_object(config_class)
    
    db.init_app(app)
    api = Api(app)
    
    
    @app.before_first_request
    def create_tables():
        db.create_all()
            
            
    api.register_blueprint(ShortUrlBlueprint)
    api.register_blueprint(CustomUrlBlueprint)
    api.register_blueprint(RedirectionBlueprint)
    api.register_blueprint(QRBlueprint)
    api.register_blueprint(AnalyticsBlueprint)
    
    
    return app