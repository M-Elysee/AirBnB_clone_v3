#!/usr/bin/python3
""" a script that handles default RESTFul api actions """
from models import storage
from flask import jsonify, request, abort
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    objs = storage.all(Amenity)
    lst = []
    for obj in objs.values():
        lst.append(obj.to_dict())
    return jsonify(lst), '200'


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity(amenity_id):
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict()), '200'


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), '200'


@app_views.route('/amenities/', methods=['POST'],
                 strict_slashes=False)
def post_amenity():
    res = request.get_json()
    dic = {}
    if not res:
        abort(404, {'Not a JSON'})
    if 'name' not in res:
        abort(400, {'Missing name'})
    dic['name'] = res['name']
    obj = Amenity(**dic)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), '201'


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    res = request.get_json()
    if not res:
        abort(400, {'Not a JSON'})
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)
    for key, value in res.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), '200'
