from db import get_mongo_client
from flask import jsonify
from bson.objectid import ObjectId

users = get_mongo_client(db="CoriderDB", collection="users")


def get_all_users():
    all_users = []

    for user in users.find():
        user["_id"] = str(user["_id"])
        all_users.append(user)

    return jsonify({"users": all_users}), 200


def create_user(request):
    data = request.data
    if not data:
        return jsonify({"message": "Bad Request: The Request Body Cannot Be Empty"}), 400
    user = request.json
    if len(user) == 0:
        return jsonify({"message": "Bad Request: The Request Body Cannot Be Empty"}), 400

    fields = ["name", "email", "password"]
    keys = user.keys()

    if not all(key in keys for key in fields):
        return jsonify({"message": "Bad Request: All Fields Are Not Provided."}), 400

    inserted_id = users.insert_one(user).inserted_id
    return jsonify({"message": "User Inserted Successfully", "id": str(inserted_id)}), 201


def get_one_user(userid: str):
    if not ObjectId.is_valid(userid):
        return jsonify({"message": "Bad Request: Invalid Object ID"}), 400
    if users.count_documents({"_id": ObjectId(userid)}) == 0:
        return jsonify({"message": "User Not Found"}), 404

    user = users.find_one({"_id": ObjectId(userid)})
    user["_id"] = str(user["_id"])
    return jsonify({"user": user}), 200


def update_one_user(userid: str, request):
    data = request.data
    if not data:
        return jsonify({"message": "Bad Request: The Request Body Cannot Be Empty"}), 400
    user = request.json
    if len(user) == 0:
        return jsonify({"message": "Bad Request: The Request Body Cannot Be Empty"}), 400
    if not ObjectId.is_valid(userid):
        return jsonify({"message": "Bad Request: Invalid Object ID"}), 400
    if users.count_documents({"_id": ObjectId(userid)}) == 0:
        return jsonify({"message": "User Not Found"}), 404

    users.update_one({"_id": ObjectId(userid)}, {"$set": user})
    user = users.find_one({"_id": ObjectId(userid)})
    user["_id"] = str(user["_id"])
    return jsonify({"message": f"User With ID {userid} - Updated Successfully", "user": user}), 200


def delete_one_user(userid: str):
    if not ObjectId.is_valid(userid):
        return jsonify({"message": "Bad Request: Invalid Object ID"}), 400
    if users.count_documents({"_id": ObjectId(userid)}) == 0:
        return jsonify({"message": "User Not Found"}), 404

    users.delete_one({"_id": ObjectId(userid)})
    return jsonify({"message": f"User With ID {userid} - Deleted Successfully"}), 200
