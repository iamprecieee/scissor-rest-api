from flask import current_app as app, send_file
from flask_smorest import Blueprint, abort
from flask.views import MethodView
import qrcode, io

from models import ShortUrlModel, CustomUrlModel

blp = Blueprint("QRcodes", "qrcodes", description="Generation of QRcodes for short or custom-short URLs")


@blp.route("/qr/<url_key>")
class QRcode(MethodView):
    @blp.doc(description="This generates QRcodes for short or custom-short URLs.")
    @blp.response(200)
    def get(self, url_key):
        """Generates QRcodes for each URL"""
        url = ShortUrlModel.query.filter(ShortUrlModel.short_url.contains(url_key)).first()
        if url is None:
            url = CustomUrlModel.query.filter(CustomUrlModel.custom_url.contains(url_key)).first()
        if not url:
            abort(404, message="URL not found")
        try:
            qr = qrcode.QRCode(
                version=2,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=5,
                border=1,
            )
            qr.add_data(app.config["DEFAULT_SERVER"] + url_key)
            qr.make(fit=True)
            img = qr.make_image(fill_color='lime', back_color='black')
            image_buffer = io.BytesIO()
            img.save(image_buffer)
            image_buffer.seek(0)
            return send_file(image_buffer, mimetype='image/png')
        except:
            abort(500, message="QRcode could not be created")