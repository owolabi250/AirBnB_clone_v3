#!/usr/bin/python3
""" index file for flask """
from crypt import methods
from os import abort
from api.v1.views import app_views
from flask import jsonify
from flask import Flask, request, abort
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def states_get(state_id=None):
    """Status json"""
    dict_all = storage.all("State")
    list = []
    for states_values in dict_all.values():
        list.append(states_values.to_dict())
    return jsonify(list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states_get_id(state_id=None):
    """Status json"""
    dict_all = storage.all("State")
    list = []
    if state_id is not None:
        for states_values in dict_all.values():
            if states_values.id == state_id:
                return jsonify(states_values.to_dict())
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletes_state_by_id(state_id=None):
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    state_obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def states_post(state_id=None):
    """Status delete"""
    result = request.get_json()
    if result is None:
        abort(400, {"Not a JSON"})
    if 'name' not in result:
        abort(400, {"Missing name"})
    state_ins = State(name=result['name'])
    storage.new(state_ins)
    storage.save()
    return jsonify(state_ins.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_states(state_id):
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    if not request.get_json():
        abort(400, {"Not a JSON"})
    result = request.get_json()
    for key, value in result.items():
        if key in ['id', 'created_at', 'updated_at']:
            continue
        else:
            setattr(state_obj, key, value)
    storage.save()
    return jsonify(state_obj.to_dict()), 200
