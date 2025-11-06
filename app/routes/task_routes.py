from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from app.models.task import Task
from .route_utilities import validate_model, get_models_with_filters, delete_model
from datetime import datetime
import os
import requests

bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()

    try:
        new_task = Task.from_dict(request_body)
    except:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_task)
    db.session.commit()

    response = new_task.to_dict()
    
    return response, 201

@bp.get("")
def get_all_tasks():
    query = db.select(Task)

    sort_param = request.args.get('sort', None)

    if sort_param == "desc":
        query = query.order_by(Task.title.desc())
    elif sort_param == "asc":
        query = query.order_by(Task.title.asc())

    tasks = db.session.scalars(query)

    tasks_response = []
    for task in tasks:
        task_dict = task.to_dict()
        tasks_response.append(task_dict)
    return tasks_response


@bp.get("<task_id>") 
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return task.to_dict()

@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    #task.completed_at = request_body["completed_at"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<task_id>")
def delete_task(task_id):
    task_response = delete_model(Task, task_id)
    return task_response


@bp.patch("/<task_id>/mark_complete")
def patch_complete_task(task_id):
    #Mark Complete on an Incomplete Task; Mark Complete on a Completed Task
    task = validate_model(Task, task_id)
   
    task.completed_at = datetime.now()
    db.session.commit()

    generate_slack_notification(task.title)

    return Response(status=204, mimetype="application/json")


@bp.patch("/<task_id>/mark_incomplete")
def patch_incomplete_task(task_id):
    #Mark Incomplete on a Completed Task; Mark Incomplete on an Incomplete Task
    task = validate_model(Task, task_id)

    task.completed_at = None
    db.session.commit()

    return Response(status=204, mimetype="application/json")


def generate_slack_notification(model_attribute):
    path = "https://slack.com/api/chat.postMessage"
    SLACK_TOKEN = os.environ.get("SLACK_BOT_TOKEN")

    headers = {
        "Authorization": f"Bearer {SLACK_TOKEN}"
    }
    json = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {model_attribute}"
    }

    slack_response = requests.post(path, headers=headers, json=json)



# Tasks should contain these attributes. The tests require the following columns to be named exactly as title, description, and completed_at.

# id: a primary key for each task
# title: text to name the task
# description: text to describe the task
# completed_at: a datetime that represents the date that a task is completed on. Can be nullable, and contain a null value. A task with a null value for completed_at has not been completed. When we create a new task, completed_at should be null AKA None in Python.


