from flask import Flask, Blueprint, request, jsonify
from db import get_mongo_client

app = Flask(__name__)
bp = Blueprint("users", __name__)
client = get_mongo_client(db="CoriderDB", collection="users")


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "message": str(error),
    }), 405


@bp.route("/", methods=["GET", "POST"])
def add_or_create_user():
    match request.method:
        case "GET":
            return "Get all users"
        case "POST":
            return "Post new user"


@bp.route("/<int:userid>/", methods=["GET", "PUT", "DELETE"])
def handle_user_with_id(userid):
    match request.method:
        case "GET":
            return "Get one user"
        case "PUT":
            return "Update one user"
        case "DELETE":
            return "Delete one user"


app.register_blueprint(bp, url_prefix="/users")

if __name__ == "__main__":
    app.run()
