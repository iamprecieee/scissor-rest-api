from marshmallow import Schema, fields

class PlainShortUrlSchema(Schema):
    id = fields.Int(dump_only=True)
    original_url = fields.Str(required=True)
    short_url = fields.Str(dump_only=True)
    date_created = fields.DateTime(dump_only=True)
    clicks = fields.Int(dump_only=True)
    
class PlainCustomUrlSchema(Schema):
    id = fields.Int(dump_only=True)
    original_url = fields.Str(required=True)
    custom_url = fields.Str(required=True)
    date_created = fields.DateTime(dump_only=True)
    clicks = fields.Int(dump_only=True)
    
class ShortUrlSchema(PlainShortUrlSchema):
    pass

class CustomUrlSchema(PlainCustomUrlSchema):
    pass

class CustomUpdateSchema(Schema):
    custom_url = fields.Str()