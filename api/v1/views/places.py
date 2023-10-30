#!/usr/bin/python3
"""This Script handles default RESTFul api actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from datetime import datetime
from models import storage
from models.city import City
from models.place import Place
import uuid


@app_views.route('/cities/<city_id>/places', methods=['GET'])
@app_views.route('/cities/<city_id>/places/', methods=['GET'])
def list_places_of_city(city_id):
    """ Module Retrieves list of all Place objects in city"""
    obj_cities = storage.all("City").values()
    obj_city = [obj.to_dict() for obj in obj_cities if obj.id == city_id]
    if obj_city == []:
        abort(404)
    places_list = [obj.to_dict() for obj in storage.all("Place").values()
                   if city_id == obj.city_id]
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """ Module Retrieves Place object """
    obj_places = storage.all("Place").values()
    place_obj = [obj.to_dict() for obj in obj_places if obj.id == place_id]
    if place_obj == []:
        abort(404)
    return jsonify(place_obj[0])


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """ Module Deletes Place object """
    obj_places = storage.all("Place").values()
    place_obj = [obj.to_dict() for obj in obj_places
                 if obj.id == place_id]
    if place_obj == []:
        abort(404)
    place_obj.remove(place_obj[0])
    for plc in obj_places:
        if plc.id == place_id:
            storage.delete(plc)
            storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>', methods=['PUT'])
def updates_place(place_id):
    """ Module Updates Place object """
    obj_places = storage.all("Place").values()
    obj_place = [plc.to_dict() for plc in obj_places if plc.id == place_id]
    if obj_place == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' in request.get_json():
        obj_place[0]['name'] = request.json['name']
    if 'description' in request.get_json():
        obj_place[0]['description'] = request.json['description']
    if 'number_rooms' in request.get_json():
        obj_place[0]['number_rooms'] = request.json['number_rooms']
    if 'number_bathrooms' in request.get_json():
        obj_place[0]['number_bathrooms'] = request.json['number_bathrooms']
    if 'max_guest' in request.get_json():
        obj_place[0]['max_guest'] = request.json['max_guest']
    if 'price_by_night' in request.get_json():
        obj_place[0]['price_by_night'] = request.json['price_by_night']
    if 'latitude' in request.get_json():
        obj_place[0]['latitude'] = request.json['latitude']
    if 'longitude' in request.get_json():
        obj_place[0]['longitude'] = request.json['longitude']
    for plc in obj_places:
        if plc.id == place_id:
            if 'name' in request.get_json():
                plc.name = request.json['name']
            if 'description' in request.get_json():
                plc.description = request.json['description']
            if 'number_rooms' in request.get_json():
                plc.number_rooms = request.json['number_rooms']
            if 'number_bathrooms' in request.get_json():
                plc.number_bathrooms = request.json['number_bathrooms']
            if 'max_guest' in request.get_json():
                plc.max_guest = request.json['max_guest']
            if 'price_by_night' in request.get_json():
                plc.price_by_night = request.json['price_by_night']
            if 'latitude' in request.get_json():
                plc.latitude = request.json['latitude']
            if 'longitude' in request.get_json():
                plc.longitude = request.json['longitude']
    storage.save()
    return jsonify(obj_place[0]), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """ Module Creates Place object """
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    obj_cities = storage.all("City").values()
    obj_city = [plc.to_dict() for plc in obj_cities
                if plc.id == city_id]
    if obj_city == []:
        abort(404)
    obj_places = []
    place_new = Place(name=request.json['name'],
                      user_id=request.json['user_id'], city_id=city_id)
    obj_users = storage.all("User").values()
    obj_user = [usr.to_dict() for usr in obj_users
                if usr.id == place_new.user_id]
    if obj_user == []:
        abort(404)
    storage.new(place_new)
    storage.save()
    obj_places.append(place_new.to_dict())
    return jsonify(obj_places[0]), 201
    x