from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from app.models.goal import Goal
from .route_utilities import validate_model, get_models_with_filters, delete_model
from datetime import datetime
import os
import requests

bp = Blueprint("goal_bp", __name__, url_prefix="/goals")


@bp.delete("/<goal_id>")
def delete_task(goal_id):
    goal_response = delete_model(Goal, goal_id)
    return goal_response