#!/usr/bin/python3
""" a script containing the blueprint of our apis """
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {'states': State, 'users': User, 'amenities': Amenity,
           'cities': City, 'places': Place, 'reviews': Review}


@app_views.route('/status', strict_slashes=False)
def status():
    """ an ok status return function """
    return jsonify(status='OK')


@app_views.route('/stats', strict_slashes=False)
def stats():
    """ a fucntion that display stats of our database """
    count = {key: storage.count(val) for key, val in classes.items()}
    return jsonify(count)
