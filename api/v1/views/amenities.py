#!/usr/bin/python3
"""
   a script that handles default RESTFul api actions
"""
from models import storage
from flask import jsonify, request, abort
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    """ Module display all amenities """
    objs = storage.all(Amenity)
    lst = []
    for obj in objs.values():
        lst.append(obj.to_dict())
    return jsonify(lst)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity(amenity_id):
    """ a function that display a particular amenity """
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Module deletes particular amenity """
    objct = storage.get(Amenity, amenity_id)
    if not objct:
        abort(404)
    storage.delete(objct)
    storage.save()
    return jsonify({}), '200'


@app_views.route('/amenities/', methods=['POST'],
                 strict_slashes=False)
def post_amenity():
    """ a function that post a new amenity """
    res = request.get_json()
    dic = {}
    if not res:
        abort(400, {'Not a JSON'})
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
    """ a fucntion that update a particular amenity """
    res = request.get_json()
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)
    if not res:
        abort(400, {'Not a JSON'})
    for key, value in res.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), '200'
