#!/usr/bin/python3
"""This Script handles default RESTFul api actions"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/place/get_places.yml', methods=['GET'])
def get_places(city_id):
    """ Retrieves list of all Place objects of City object """
    cty = storage.get(City, city_id)

    if not cty:
        abort(404)

    plcs = [plc.to_dict() for plc in cty.places]

    return jsonify(plcs)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/place/get_place.yml', methods=['GET'])
def get_place(place_id):
    """ Retrieves Place object """
    plc = storage.get(Place, place_id)
    if not plc:
        abort(404)

    return jsonify(plc.to_dict())


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/place/post_place.yml', methods=['POST'])
def post_place(city_id):
    """ Creates Place object """
    cty = storage.get(City, city_id)

    if not cty:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    dta = request.get_json()
    usr = storage.get(User, dta['user_id'])

    if not usr:
        abort(404)

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    dta["city_id"] = city_id
    instance = Place(**dta)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/place/delete_place.yml', methods=['DELETE'])
def delete_place(place_id):
    """ Deletes a Place Object """

    plc = storage.get(Place, place_id)

    if not plc:
        abort(404)

    storage.delete(plc)
    storage.save()

    return make_response


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/place/put_place.yml', methods=['PUT'])
def put_place(place_id):
    """ Updates Place object """
    plc = storage.get(Place, place_id)

    if not plc:
        abort(404)

    dta = request.get_json()
    if not dta:
        abort(400, description="Not a JSON")

    ign = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    for key, value in dta.items():
        if key not in ign:
            setattr(plc, key, value)
    storage.save()
    return make_response(jsonify(plc.to_dict()), 200)


(jsonify({}), 200)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
@swag_from('documentation/place/post_search.yml', methods=['POST'])
def places_search():
    """ Retrieves all Place objects depending of JSON request """

    if request.get_json() is None:
        abort(400, description="Not a JSON")

    dta = request.get_json()

    if dta and len(dta):
        stas = dta.get('states', None)
        cities = dta.get('cities', None)
        amenities = dta.get('amenities', None)

    if not dta or not len(dta) or (
            not stas and
            not cities and
            not amenities):
        plcs = storage.all(Place).values()
        list_plcs = []
        for plc in plcs:
            list_plcs.append(plc.to_dict())
        return jsonify(list_plcs)

    list_plcs = []
    if stas:
        stas_obj = [storage.get(State, s_id) for s_id in stas]
        for sta in stas_obj:
            if sta:
                for cty in sta.cities:
                    if cty:
                        for plc in cty.plcs:
                            list_plcs.append(plc)

    if cities:
        cty_obj = [storage.get(City, c_id) for c_id in cities]
        for cty in city_obj:
            if cty:
                for plc in cty.plcs:
                    if plc not in list_plcs:
                        list_plcs.append(plc)

    if amenities:
        if not list_plcs:
            list_plcs = storage.all(plc).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        list_plcs = [plc for plc in list_plcs
                     if all([am in plc.amenities
                            for am in amenities_obj])]

    plcs = []
    for p in list_plcs:
        d = p.to_dict()
        d.pop('amenities', None)
        plcs.append(d)

    return jsonify(plcs)