from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from backend.extensions import db
from backend.models import User, Category, Record
from backend.schemas import UserSchema, UserLoginSchema, CategorySchema, RecordSchema

blp = Blueprint("api", "api", url_prefix="/")

@blp.route("/healthcheck")
def healthcheck():
    return jsonify({"status": "OK", "message": "Backend is functional"})

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        if db.session.execute(db.select(User).where(User.username == user_data["username"])).scalar():
            abort(409, message="A user with that username already exists.")

        user = User(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        db.session.add(user)
        db.session.commit()
        return user


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, user_data):
        user = db.session.execute(db.select(User).where(User.username == user_data["username"])).scalar()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=str(user.id))
            return jsonify({"access_token": access_token})

        abort(401, message="Invalid credentials.")


@blp.route("/user/<int:user_id>")
class UserResource(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = db.session.get(User, user_id)
        if not user:
            abort(404, message="User not found")
        return user

    @jwt_required()
    def delete(self, user_id):
        user = db.session.get(User, user_id)
        if not user:
            abort(404, message="User not found")
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}


@blp.route("/category")
class CategoryResource(MethodView):
    @jwt_required()
    @blp.response(200, CategorySchema(many=True))
    def get(self):
        return Category.query.all()

    @jwt_required()
    @blp.arguments(CategorySchema)
    @blp.response(200, CategorySchema)
    def post(self, category_data):
        if category_data.get("user_id"):
            user = db.session.get(User, category_data["user_id"])
            if not user:
                abort(404, message="User not found")

        category = Category(**category_data)
        db.session.add(category)
        db.session.commit()
        return category


@blp.route("/category/<int:category_id>")
class CategoryByIdResource(MethodView):
    @jwt_required()
    def delete(self, category_id):
        category = db.session.get(Category, category_id)
        if not category:
            abort(404, message="Category not found")
        db.session.delete(category)
        db.session.commit()
        return {"message": "Category deleted"}


@blp.route("/record")
class RecordResource(MethodView):
    @jwt_required()
    @blp.arguments(RecordSchema)
    @blp.response(200, RecordSchema)
    def post(self, record_data):
        user = db.session.get(User, record_data["user_id"])
        category = db.session.get(Category, record_data["category_id"])

        if not user:
            abort(400, message="User does not exist")
        if not category:
            abort(400, message="Category does not exist")

        record = Record(**record_data)
        db.session.add(record)
        db.session.commit()
        return record


@blp.route("/record/<int:record_id>")
class RecordByIdResource(MethodView):
    @jwt_required()
    @blp.response(200, RecordSchema)
    def get(self, record_id):
        record = db.session.get(Record, record_id)
        if not record:
            abort(404, message="Record not found")
        return record

    @jwt_required()
    def delete(self, record_id):
        record = db.session.get(Record, record_id)
        if not record:
            abort(404, message="Record not found")
        db.session.delete(record)
        db.session.commit()
        return {"message": "Record deleted"}