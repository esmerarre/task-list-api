from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from app.models.task import Task

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@task_bp.post("")
def create_task():
    request_body = request.get_json()
    title = request_body["title"]
    description = request_body["description"]
    completed_at = request_body["completed_at"]

    new_task = Task(title = title, description = description, completed_at= completed_at)
    db.session.add(new_task)
    db.session.commit()

    response = new_task.to_dict()
    
    # {
    #     "title": new_task.title,
    #     "description": new_task.description,
    #     "is_complete": True if new_task.completed_at == None else False
    #             }
    return response, 201





# Tasks should contain these attributes. The tests require the following columns to be named exactly as title, description, and completed_at.

# id: a primary key for each task
# title: text to name the task
# description: text to describe the task
# completed_at: a datetime that represents the date that a task is completed on. Can be nullable, and contain a null value. A task with a null value for completed_at has not been completed. When we create a new task, completed_at should be null AKA None in Python.
