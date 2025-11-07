from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from app.models.task import Task
from .route_utilities import validate_model, create_model, get_models_by_order, generate_slack_notification
from datetime import datetime


bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Task, request_body)

@bp.get("")
def get_all_tasks():
    return get_models_by_order(Task)


@bp.get("<task_id>") 
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return task.to_dict(include_goal_id = True)

@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.patch("/<task_id>/mark_complete")
def patch_complete_task(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now()
    db.session.commit()
    generate_slack_notification(task.title)

    return Response(status=204, mimetype="application/json")


@bp.patch("/<task_id>/mark_incomplete")
def patch_incomplete_task(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None
    db.session.commit()

    return Response(status=204, mimetype="application/json")


