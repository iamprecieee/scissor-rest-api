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
    
class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    
class PlainLoginSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str()
    email = fields.Str()
    password = fields.Str(required=True)
class ShortUrlSchema(PlainShortUrlSchema):
    user_id = fields.Int(required=True, load_only=True)

class CustomUrlSchema(PlainCustomUrlSchema):
    user_id = fields.Int(required=True, load_only=True)

class UserSchema(PlainUserSchema):
    pass

class LoginSchema(PlainLoginSchema):
    pass

class CustomUpdateSchema(Schema):
    custom_url = fields.Str()