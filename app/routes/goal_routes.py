from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from app.models.goal import Goal
from app.models.task import Task
from .route_utilities import validate_model, create_model, get_models_by_order
from datetime import datetime
import os
import requests

bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model(Goal, request_body)

@bp.get("")
def get_all_goals():
    return get_models_by_order(Goal)

@bp.get("/<goal_id>") 
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    goal_dict =  {"id": goal.id, "title": goal.title}

    return goal_dict

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

@bp.post("/<goal_id>/tasks")
def creat_tasks_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    task_id_list = request_body.get("task_ids", [])
    
    for task_obj in list(goal.tasks):
        task_obj.goal = None

    for task_id in task_id_list:
        task = validate_model(Task, task_id)
        task.goal = goal
    db.session.commit()

    response = {"id": goal.id, "task_ids": task_id_list}

    return response, 200

@bp.get("/<goal_id>/tasks")
def get_tasks_for_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    response = goal.to_dict(include_tasks = True, include_goal_id_in_tasks = True)
    return response