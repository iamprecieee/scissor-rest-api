from flask import jsonify
from flask_smorest import Blueprint
from flask.views import MethodView

from models import ShortUrlModel, CustomUrlModel

blp = Blueprint("Analytics", "analytics", description="Operations on user analytics data")


@blp.route("/analytics")
class UserAnalytics(MethodView):
    @blp.doc(description="This retrieves the click analytics for each URL.")
    @blp.response(200)
    def get(self):
        """Retrieves click data for short and custom-short URLs"""
        shorturls = ShortUrlModel.query.all()
        customurls = CustomUrlModel.query.all()
        data = {
            "labels": [shorturl.short_url for shorturl in shorturls] + [customurl.custom_url for customurl in customurls],
            "clicks": [shorturl.clicks for shorturl in shorturls] + [customurl.clicks for customurl in customurls]
        }
        return jsonify(data)

