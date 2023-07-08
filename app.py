from flask import Flask, Blueprint, request, jsonify, abort
from handlers import get_all_users, create_user, get_one_user, update_one_user, delete_one_user

app = Flask(__name__)
bp = Blueprint("users", __name__)


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "message": str(error),
    }), 405


@bp.route("/", methods=["GET", "POST"])
def add_or_create_user():
    match request.method:
        case "GET":
            return get_all_users()
        case "POST":
            return create_user(request=request)
        case _:
            abort(405)


@bp.route("/<userid>/", methods=["GET", "PUT", "DELETE"])
def handle_user_with_id(userid):
    match request.method:
        case "GET":
            return get_one_user(userid)
        case "PUT":
            return update_one_user(userid=userid, request=request)
        case "DELETE":
            return delete_one_user(userid)
        case _:
            abort(405)


app.register_blueprint(bp, url_prefix="/users")

if __name__ == "__main__":
    app.run()
