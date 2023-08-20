from flask import jsonify
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from flask.views import MethodView

from models import ShortUrlModel, CustomUrlModel

blp = Blueprint("Analytics", "analytics", description="Operations on user analytics data")


@blp.route("/analytics")
class UserAnalytics(MethodView):
    @blp.doc(description="This retrieves the click analytics for each URL.")
    @blp.response(200)
    @jwt_required()
    def get(self):
        """Retrieves click data for short and custom-short URLs"""
        shorturls = ShortUrlModel.query.all()
        customurls = CustomUrlModel.query.all()
        data = {
            "short": [[{"URL":shorturl.short_url}, {"Clicks":shorturl.clicks}] for shorturl in shorturls],
            "custom":[[{"URL":customurl.custom_url} , {"Clicks":customurl.clicks}] for customurl in customurls]
        }
        return jsonify(data)

