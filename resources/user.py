from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, create_access_token, create_refresh_token
from passlib.hash import pbkdf2_sha256
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models import UserModel
from schemas import UserSchema, LoginSchema
from resources.db import db
from resources.blocklist import BLOCKLIST

blp = Blueprint("Users", "users", description="Operations on Users")


@blp.route("/signup")
class SignUp(MethodView):
    @blp.doc(description="This creates a new user.")
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, userdata):
        """Create new User"""
        userdata["password"] = pbkdf2_sha256.hash(userdata["password"])
        user = UserModel(**userdata)
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(409, message="A user with similar credentials already exists")
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="User could not be created")
        return user
    
   
@blp.route("/login")
class Login(MethodView):
    @blp.doc(description="This logs a user in.")
    @blp.arguments(LoginSchema)
    @blp.response(201)
    def post(self, userdata):
        """Login User"""
        if "username" not in userdata and "email" not in userdata:
            abort(400, message="Enter Username or Email")
        elif "username" in userdata:
            user = UserModel.query.filter(UserModel.username == userdata["username"]).first()
        elif "email" in userdata:
            user = UserModel.query.filter(UserModel.email == userdata["email"]).first()
        if user and pbkdf2_sha256.verify(userdata["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            response = {"access_token": access_token, "refresh_token": refresh_token}
            return response
        abort(401, message = "Invalid credentials!")
        
        
@blp.route("/refresh")
class Refresh(MethodView):
    @blp.doc(description="This creates a non-fresh access token.")
    @jwt_required(refresh=True)
    def post(self):
        """Creates non-fresh access token"""
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user, fresh=False)
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": access_token}
        
        
@blp.route("/logout")
class Logout(MethodView):
    @blp.doc(description="This logs a user out.")
    @blp.response(200)
    @jwt_required()
    def post(self):
        """Logout User"""
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Logged out successfully"}
    

@blp.route("/user")
class User(MethodView):
    @blp.doc(description="This retrieves a list of all users.")
    @blp.response(200, UserSchema(many=True))
    @jwt_required()
    def get(self):
        """Returns a list of Users"""
        users = UserModel.query.all()
        return users
    

@blp.route("/user/<user_id>")
class User(MethodView):
    @blp.doc(description="This retrieves a specific user.")
    @blp.response(200, UserSchema)
    @jwt_required()
    def get(self, user_id):
        """Returns specific User"""
        user = UserModel.query.filter(UserModel.id == user_id).first()
        if not user:
            abort(404, message="User not found")
        return user
    
    @blp.doc(description="This deletes a specific user.")
    @jwt_required(fresh=True)
    def delete(self, user_id):
        """Deletes specific User"""
        current_user = get_jwt_identity()
        user = UserModel.query.filter(UserModel.id == user_id).first()
        if not user:
            abort(404, message="User not found")
        if current_user != user.id:
            abort(400, message="Action prohibited")
        try:
            db.session.delete(user)
            db.session.commit()
        except:
            db.session.rollback()
            abort(400, message="User could not be deleted")
        return {"message": "User deleted successfully"}, 200
    
        