from flask import current_app as app
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from models import ShortUrlModel
from schemas import ShortUrlSchema
from resources.db import db
from resources.utils import generate_short_url, validate_url

blp = Blueprint("Shorturls", "shorturls", description="Operations on Short URLs")

@blp.route("/shorturl")
class ShortUrlList(MethodView):
    @blp.doc(description="This returns a list of all existing short URLs and corresponding original URLs.")
    @blp.response(200, ShortUrlSchema(many=True))
    @jwt_required()
    def get(self):
        """Return list of short URLs"""
        shorturls = ShortUrlModel.query.all()
        return shorturls
        
    
    @blp.doc(description="This creates a new random short URL for a provided original URL.")
    @blp.arguments(ShortUrlSchema)
    @blp.response(201, ShortUrlSchema)
    @jwt_required()
    def post(self, urldata):
        """Create new short URL"""
        short = app.config["DEFAULT_SERVER"] + generate_short_url()
        if not urldata["original_url"].strip():
            abort(400, message="URL fields cannot be empty")
        elif not validate_url(urldata["original_url"]):
            abort(400, message="Invalid URL")
        url = ShortUrlModel(short_url=short, **urldata)
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
        

@blp.route("/shorturl/<url_key>")
class ShortUrl(MethodView):
    @blp.doc(description="This returns a specific existing short URL and corresponding original URL.")
    @blp.response(201, ShortUrlSchema)
    @jwt_required()
    def get(self, url_key):
        """Return specific short URL"""
        url = ShortUrlModel.query.filter(ShortUrlModel.short_url.contains(url_key)).first()
        if url is None:
            abort(404, message="URL not found")
        return url
            
    @blp.doc(description="This deletes a specific existing short URL and corresponding original URL.")
    @jwt_required(fresh=True)
    def delete(self, url_key):
        """Delete specific short URL"""
        url = ShortUrlModel.query.filter(ShortUrlModel.short_url.contains(url_key)).first()
        if url is None:
            abort(404, message="URL not found")
        db.session.delete(url)
        db.session.commit()
        return {"message": "URL deleted successfully"}, 204
