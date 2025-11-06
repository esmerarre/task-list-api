from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from app.models.goal import Goal
from .route_utilities import validate_model, get_models_with_filters
from datetime import datetime
import os
import requests

bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal.from_dict(request_body)
    except:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_goal)
    db.session.commit()

    response = new_goal.to_dict()
    
    return response, 201

@bp.get("")
def get_all_goals():
    query = db.select(Goal)

    sort_param = request.args.get('sort', None)

    if sort_param == "desc":
        query = query.order_by(Goal.title.desc())
    elif sort_param == "asc":
        query = query.order_by(Goal.title.asc())

    goals = db.session.scalars(query)

    goals_response = []
    for goal in goals:
        goal_dict = goal.to_dict()
        goals_response.append(goal_dict)
    return goals_response

@bp.get("/<goal_id>") 
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return goal.to_dict()

@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

