#!/usr/bin/python3
"""
   a script that handles default RESTFul api actions
"""
from models import storage
from flask import jsonify, request, abort
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """ a function that display all states """
    objs = storage.all(State)
    lst = []
    for obj in objs.values():
        lst.append(obj.to_dict())
    return jsonify(lst)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def state(state_id):
    """ a function that display a particular state """
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ a function that deletes a particular state """
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), '200'


@app_views.route('/states/', methods=['POST'],
                 strict_slashes=False)
def post_state():
    """ a function that post a new state """
    res = request.get_json()
    dic = {}
    if not res:
        abort(400, {'Not a JSON'})
    if 'name' not in res:
        abort(400, {'Missing name'})
    dic['name'] = res['name']
    obj = State(**dic)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), '201'


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """ a function that updates a given state """
    res = request.get_json()
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    if not res:
        abort(400, {'Not a JSON'})
    for key, value in res.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), '200'
