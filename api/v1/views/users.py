#!/usr/bin/python3
"""This Script handles default RESTFul api actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
from datetime import datetime
import uuid


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def list_users():
    """ Module Retrieves list of all User objects """
    list_users = [obj.to_dict() for obj in storage.all("User").values()]
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """ Module Retrieves User object """
    users_obj = storage.all("User").values()
    user_obj = [usr.to_dict() for usr in users_obj if usr.id == user_id]
    if user_obj == []:
        abort(404)
    return jsonify(user_obj[0])


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Module Deletes User object"""
    users_obj = storage.all("User").values()
    user_obj = [usr.to_dict() for usr in users_obj if usr.id == user_id]
    if user_obj == []:
        abort(404)
    user_obj.remove(user_obj[0])
    for usr in users_obj:
        if obj.id == user_id:
            storage.delete(usr)
            storage.save()
    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def create_user():
    """ Module Creates User """
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'email' not in request.get_json():
        abort(400, 'Missing name')
    if 'password' not in request.get_json():
        abort(400, 'Missing password')
    obj_users = []
    user_new = User(email=request.json['email'],
                    password=request.json['password'])
    storage.new(user_new)
    storage.save()
    obj_users.append(user_new.to_dict())
    return jsonify(obj_users[0]), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """ Module Updates User object """
    users_obj = storage.all("User").values()
    user_obj = [usr.to_dict() for usr in users_obj if usr.id == user_id]
    if user_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    try:
        user_obj[0]['first_name'] = request.json['first_name']
    except Exception:
        pass
    try:
        user_obj[0]['last_name'] = request.json['last_name']
    except Exception:
        pass
    for usr in users_obj:
        if usr.id == user_id:
            try:
                if request.json['first_name'] is not None:
                    usr.first_name = request.json['first_name']
            except Exception:
                pass
            try:
                if request.json['last_name'] is not None:
                    usr.last_name = request.json['last_name']
            except Exception:
                pass
    storage.save()
    return jsonify(user_obj[0]), 200
