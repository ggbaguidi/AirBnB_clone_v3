#!/usr/bin/python3
"""cities module"""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<string:state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def get_cities_by_state_id(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<string:city_id>", methods=['GET'],
                 strict_slashes=False)
def get_city_by_id(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route("/cities/<string:city_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_city_by_id(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    city.delete()
    storage.save()

    return jsonify({})


@app_views.route("/states/<string:state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def post_cities_by_state_id(state_id):
    """Creates a City"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)
    request_to_json = request.get_json()

    if not request_to_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request_to_json:
        return make_response(jsonify({"error": "Missing name"}), 400)

    city = City(**request_to_json, state_id=state_id)
    city.save()

    return make_response(jsonify(city.to_dict()), 201)


@app_views.route("/cities/<string:city_id>", methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)
    request_to_json = request.get_json()
    if not request_to_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, val in request_to_json.items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(city, key, val)

    city.save()
    return jsonify(city.to_dict())
