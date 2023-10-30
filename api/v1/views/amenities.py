#!/usr/bin/python3
""" This Script handles default RESTFul api actions """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    """ Module display all amenities """
    objcts = storage.all(Amenity)
    lst = []
    for objct in objcts.values():
        lst.append(objct.to_dict())
    return jsonify(lst), '200'

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

@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Module updates particular amenity """
    json_res = request.get_json()
    if not json_res:
        abort(400, {'Not a JSON'})
    objct = storage.get(Amenity, amenity_id)
    if not objct:
        abort(404)
    for json_key, item in json_res.items():
        if json_key not in ['id', 'created_at', 'updated_at']:
            setattr(objct, json_key, item)
    storage.save()
    return jsonify(objct.to_dict()), '200'

@app_views.route('/amenities/', methods=['POST'],
                 strict_slashes=False)
def post_amenity():
    """ Module post new amenity """
    json_res = request.get_json()
    dct = {}
    if not json_res:
        abort(404, {'Not a JSON'})
    if 'name' not in json_res:
        abort(400, {'Missing name'})
    dct['name'] = json_res['name']
    objct = Amenity(**dct)
    storage.new(objct)
    storage.save()
    return jsonify(objct.to_dict()), '201'

@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity(amenity_id):
    """ Module display particular amenity """
    objct = storage.get(Amenity, amenity_id)
    if not objct:
        abort(404)
    return jsonify(objct.to_dict()), '200'
