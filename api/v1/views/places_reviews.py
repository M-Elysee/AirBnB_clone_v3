#!/usr/bin/python3
"""This Script handles default RESTFul api actions"""
from api.v1.views import app_views
from datetime import datetime
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
import uuid


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
@app_views.route('/places/<place_id>/reviews/', methods=['GET'])
def list_reviews_of_place(place_id):
    """ Module Retrieves list of all Review objects of a Place """
    obj_places = storage.all("Place").values()
    obj_place = [obj.to_dict() for obj in obj_places if obj.id == place_id]
    if obj_place == []:
        abort(404)
    list_reviews = [obj.to_dict() for obj in storage.all("Review").values()
                    if place_id == obj.place_id]
    return jsonify(list_reviews)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """ Module Creates a Review """
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    user_id = request.json['user_id']
    if 'text' not in request.get_json():
        abort(400, 'Missing text')
    obj_places = storage.all("Place").values()
    obj_place = [plc.to_dict() for plc in obj_places if plc.id == place_id]
    if obj_place == []:
        abort(404)
    all_users = storage.all("User").values()
    user_obj = [usr.to_dict() for usr in all_users if usr.id == user_id]
    if user_obj == []:
        abort(404)
    reviews = []
    new_review = Review(text=request.json['text'], place_id=place_id,
                        user_id=user_id)
    storage.new(new_review)
    storage.save()
    reviews.append(new_review.to_dict())
    return jsonify(reviews[0]), 201


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """ Module Retrieves a Review object """
    obj_reviews = storage.all("Review").values()
    obj_review = [rev.to_dict() for rev in obj_reviews if rev.id == review_id]
    if obj_review == []:
        abort(404)
    return jsonify(obj_review[0])


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """ Module Deletes a Review object"""
    obj_reviews = storage.all("Review").values()
    obj_review = [rev.to_dict() for rev in obj_reviews if rev.id == review_id]
    if obj_review == []:
        abort(404)
    obj_review.remove(obj_review[0])
    for obj in obj_reviews:
        if obj.id == review_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def updates_review(review_id):
    """ Module Updates a Review object"""
    obj_reviews = storage.all("Review").values()
    obj_review = [rev.to_dict() for rev in obj_reviews if rev.id == review_id]
    if obj_review == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'text' in request.get_json():
        obj_review[0]['text'] = request.json['text']
        for rev in obj_reviews:
            if rev.id == review_id:
                rev.text = request.json['text']
        storage.save()
    return jsonify(obj_review[0]), 200
