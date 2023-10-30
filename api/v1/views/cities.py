#!/usr/bin/python3
"""
   a script that handles default RESTFul api actions
"""
from models import storage
from flask import jsonify, request, abort
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def city(city_id):
    """ gets a particular city """
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities(state_id):
    """ sends all cities in a state """
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    lst = []
    for city in obj.cities:
        lst.append(city.to_dict())
    return jsonify(lst)


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ deletes a particular city """
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), '200'


@app_views.route('/states/<string:state_id>/cities/', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """ post a new city """
    res = request.get_json()
    dic = {}
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    if not res:
        abort(400, {'Not a JSON'})
    if 'name' not in res:
        abort(400, {'Missing name'})
    dic['name'] = res['name']
    dic['state_id'] = state_id
    city_obj = City(**dic)
    storage.new(city_obj)
    storage.save()
    return jsonify(city_obj.to_dict()), '201'


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """ a fucntion that updates a particular city """
    res = request.get_json()
    if not res:
        abort(400, {'Not a JSON'})
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    for key, value in res.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), '200'
