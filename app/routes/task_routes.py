from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from app.models.task import Task
from .route_utilities import validate_model

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@task_bp.post("")
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

@task_bp.get("")
def get_all_tasks():
    query = db.select(Task)

    query = query.order_by(Task.id)
    tasks = db.session.scalars(query)

    tasks_response = []
    for task in tasks:
        task_dict = task.to_dict()
        tasks_response.append(task_dict)
    return tasks_response

@task_bp.get("<task_id>") 
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return task.to_dict()

@task_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    #task.completed_at = request_body["completed_at"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@task_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


# Tasks should contain these attributes. The tests require the following columns to be named exactly as title, description, and completed_at.

# id: a primary key for each task
# title: text to name the task
# description: text to describe the task
# completed_at: a datetime that represents the date that a task is completed on. Can be nullable, and contain a null value. A task with a null value for completed_at has not been completed. When we create a new task, completed_at should be null AKA None in Python.
