#!/usr/bin/python3
"""users route module"""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user_by_id(user_id=None):
    """Retrieves a User object:"""
    if not user_id:
        users = [user.to_dict() for user in storage.all(User).values()]
        return jsonify(users)

    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user_by_id(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    user.delete()
    storage.save()

    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_users():
    """Creates a User"""
    request_to_json = request.get_json()

    if not request_to_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "email" not in request_to_json:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if "password" not in request_to_json:
        return make_response(jsonify({"error": "Missing password"}), 400)

    user = User(**request_to_json)
    user.save()

    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_users(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    request_to_json = request.get_json()

    if not request_to_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, val in request_to_json.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, val)

    user.save()

    return jsonify(user.to_dict())
