from flask import current_app as app
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from models import CustomUrlModel, ShortUrlModel
from schemas import CustomUrlSchema, CustomUpdateSchema
from resources.db import db
from resources.utils import validate_url

blp = Blueprint("Customurl", "customurl", description="Operations on Custom-short URLs")

@blp.route("/customurl")
class ShortUrlList(MethodView):
    @blp.doc(description="This returns a list of all existing custom-short URLs and corresponding original URLs.")
    @blp.response(200, CustomUrlSchema(many=True))
    @jwt_required()
    def get(self):
        """Return list of custom-short URLs"""
        return CustomUrlModel.query.all()
    
    @blp.doc(description="This creates a new custom-short URL for a provided original URL.")
    @blp.arguments(CustomUrlSchema)
    @blp.response(201, CustomUrlSchema)
    @jwt_required()
    def post(self, urldata):
        """Create new short URL"""
        if not urldata["custom_url"].strip() or not urldata["original_url"].strip():
            abort(400, message="URL fields cannot be empty")
        elif not validate_url(urldata["original_url"]):
            abort(400, message="Invalid URL")
        if shorturl := ShortUrlModel.query.filter(
            ShortUrlModel.short_url.contains(urldata["custom_url"])
        ).first():
            abort(400, message="Similar short URL already exists")
        urldata["custom_url"] = app.config["DEFAULT_SERVER"] + urldata["custom_url"]
        url = CustomUrlModel(**urldata)
        try:
            db.session.add(url)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(400, message="This original URL already exists")
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="URL could not be shortened")
        return url
        

@blp.route("/customurl/<url_key>")
class ShortUrl(MethodView):
    @blp.doc(description="This returns a specific existing custom-short URL and corresponding original URL.")
    @blp.response(201, CustomUrlSchema)
    @jwt_required()
    def get(self, url_key):
        """Return specific short URL"""
        url = CustomUrlModel.query.filter(CustomUrlModel.custom_url.contains(url_key)).first()
        if not url:
            abort(404, message="URL not found")
        return url
        
    @blp.doc(description="This updates a specific existing custom-short URL.")
    @blp.arguments(CustomUpdateSchema)
    @jwt_required(fresh=True)
    def put(self, urldata, url_key):
        """Update specific custom-short URL"""
        url = CustomUrlModel.query.filter(CustomUrlModel.custom_url.contains(url_key)).first()
        shorturl = ShortUrlModel.query.filter(ShortUrlModel.short_url.contains(urldata["custom_url"])).first()
        if not url:
            abort(404, message="URL not found")
        elif not urldata["custom_url"].strip():
            abort(400, message="URL fields cannot be empty")
        elif url.custom_url == app.config["DEFAULT_SERVER"] + urldata["custom_url"]:
            abort(400, message="This custom-short URL already exists")
        elif shorturl and shorturl.short_url == app.config["DEFAULT_SERVER"] + urldata["custom_url"]:
            abort(400, message="Similar short URL already exists")
        try:
            url.custom_url = app.config["DEFAULT_SERVER"] + urldata["custom_url"]
            db.session.add(url)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback() 
            abort(500, message="URL could not be updated")
        return {"message": "URL updated successfully."}, 201
            
    @blp.doc(description="This deletes a specific existing custom-short URL and corresponding original URL.")
    @jwt_required(fresh=True)
    def delete(self, url_key):
        """Delete specific custom-short URL"""
        url = CustomUrlModel.query.filter(CustomUrlModel.custom_url.contains(url_key)).first()
        if not url:
            abort(404, message="URL not found")
        db.session.delete(url)
        db.session.commit()
        return {"message": "URL deleted successfully"}, 204
        
