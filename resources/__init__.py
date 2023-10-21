from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from resources.db import db
from resources.config import Config
from resources.blocklist import BLOCKLIST
from models import UserModel

from resources.shorturl import blp as ShortUrlBlueprint
from resources.customurl import blp as CustomUrlBlueprint
from resources.redirection import blp as RedirectionBlueprint
from resources.qrcode import blp as QRBlueprint
from resources.analytics import blp as AnalyticsBlueprint
from resources.user import blp as UserBlueprint


def create_app(config_class=Config):
    
    app = Flask(__name__)

    app.config.from_object(config_class)

    db.init_app(app)
    api = Api(app)
    jwt = JWTManager(app)


    @app.before_first_request
    def create_tables():
        db.create_all()


    api.register_blueprint(UserBlueprint)
    api.register_blueprint(ShortUrlBlueprint)
    api.register_blueprint(CustomUrlBlueprint)
    api.register_blueprint(RedirectionBlueprint)
    api.register_blueprint(QRBlueprint)
    api.register_blueprint(AnalyticsBlueprint)


    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "Token has expired.", "error": "token_expired"}), 401

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return jsonify({"description": "The token is not fresh.", "error": "fresh_token_required"}), 401

    @jwt.revoked_token_loader
    def revoke_token_callback(jwt_header, jwt_payload):
        return jsonify({"description": "The token has been revoked", "error": "token_revoked"}), 401

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Signature verification failed.", "error": "invalid_token"}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"description": "Request does not contain access token.", "error": "authorization_required"}), 401

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        return {"is_admin": True} if identity == 1 else {"is_admin": False}

    @jwt.user_lookup_loader
    def user_loader_callback(jwt_header, jwt_payload):
        user_id = jwt_payload["sub"]  # Assuming the user ID is stored in the "sub" claim
        user = UserModel.query.get(user_id)
        return user


    return app