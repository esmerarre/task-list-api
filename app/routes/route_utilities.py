from flask import abort, make_response, Response, request
from ..db import db
import os
import requests

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        response = {"message": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))

    return model

def get_models_by_order(cls, filters=None):
    query = db.select(cls)

    sort_param = request.args.get('sort', None)

    if sort_param == "desc":
        query = query.order_by(cls.title.desc())
    elif sort_param == "asc":
        query = query.order_by(cls.title.asc())

    models = db.session.scalars(query)

    model_response = []
    for model in models:
        model_dict =  model.to_dict()
        model_response.append(model_dict)

    return model_response

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
        
    except KeyError as error:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))
    
    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201

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