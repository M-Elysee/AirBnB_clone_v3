#!/usr/bin/python3
"""places_amenities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from datetime import datetime
import uuid
from os import getenv

if getenv('HBNB_TYPE_STORAGE') == 'db':
    @app_views.route('/places/<place_id>/amenities', methods=['GET'])
    @app_views.route('/places/<place_id>/amenities/', methods=['GET'])
    def list_amenities_of_place(place_id):
        """ Module Retrieves list of all Amenity objects of Place """
        obj_places = storage.all("Place").values()
        obj_place = [plc.to_dict() for plc in obj_places if plc.id == place_id]
        if obj_place == []:
            abort(404)
        ls_amenities = []
        for plc in obj_places:
            if plc.id == place_id:
                for amenity in plc.amenities:
                    ls_amenities.append(amenity.to_dict())
        return jsonify(ls_amenities)

    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['POST'])
    def create_place_amenity(place_id, amenity_id):
        """ Module Creates Amenity """
        obj_places = storage.all("Place").values()
        obj_place = [plc.to_dict() for plc in obj_places if plc.id == place_id]
        if obj_place == []:
            abort(404)

        obj_amenities = storage.all("Amenity").values()
        obj_amenity = [amnt.to_dict() for amnt in obj_amenities
                       if amnt.id == amenity_id]
        if obj_amenity == []:
            abort(404)

        amenities = []
        for plc in obj_places:
            if plc.id == place_id:
                for amnt in obj_amenities:
                    if amnt.id == amenity_id:
                        plc.amenities.append(amnt)
                        storage.save()
                        amenities.append(amnt.to_dict())
                        return jsonify(amenities[0]), 200
        return jsonify(amenities[0]), 201

    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['DELETE'])
    def delete_place_amenity(place_id, amenity_id):
        """ Module Deletes Amenity object """
        obj_places = storage.all("Place").values()
        obj_place = [plc.to_dict() for plc in obj_places if plc.id == place_id]
        if obj_place == []:
            abort(404)

        obj_amenities = storage.all("Amenity").values()
        obj_amenity = [amnt.to_dict() for amnt in obj_amenities
                       if amnt.id == amenity_id]
        if obj_amenity == []:
            abort(404)
        obj_amenity.remove(obj_amenity[0])

        for plc in obj_places:
            if plc.id == place_id:
                if plc.amenities == []:
                    abort(404)
                for amnt in plc.amenities:
                    if amnt.id == amenity_id:
                        storage.delete(amnt)
                        storage.save()
        return jsonify({}), 200


    @app_views.route('/amenities/<amenity_id>', methods=['GET'])
    def get_place_amenity(amenity_id):
        """ Module Retrieves Amenity object """
        obj_amenities = storage.all("Amenity").values()
        obj_amenity = [amnt.to_dict() for amnt in obj_amenities
                    if amnt.id == amenity_id]
        if obj_amenity == []:
            abort(404)
        return jsonify(obj_amenity[0])