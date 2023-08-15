from flask import redirect
from flask_smorest import Blueprint, abort
from flask.views import MethodView

from models import ShortUrlModel, CustomUrlModel
from resources.db import db

blp = Blueprint("Redirects", "redirects", description="Redirection of short or custom-short URLs")


@blp.route("/<url_key>")
class Redirect(MethodView):
    @blp.doc(description="This redirects the short or custom-short URL to the original URL.")
    @blp.response(200)
    def get(self, url_key):
        """Redirects short or custom-short URL"""
        url = ShortUrlModel.query.filter(ShortUrlModel.short_url.contains(url_key)).first()
        if url is None:
            url = CustomUrlModel.query.filter(CustomUrlModel.custom_url.contains(url_key)).first()
        if not url:
            abort(404, message="URL not found")
        url.clicks += 1
        db.session.commit()
        return redirect(url.original_url)
    