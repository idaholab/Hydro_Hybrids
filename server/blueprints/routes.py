from flask import Blueprint, jsonify, request
from celery.app.control import Control
from learning.learning import model
from tasks.app import app

tasks = Blueprint("tasks", __name__)

@tasks.route('/status/<task_id>', methods=["GET"])
def status(task_id):
    """This route returns the current state of the celery task"""
    task = model.AsyncResult(task_id)

    if task.state != 'FAILURE':
        response = {
            'state': task.state
        }
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'exception': str(task.info),  # this is the exception raised
        }

    return jsonify(response)

@tasks.route('/kill', methods=["GET"])
def kill():
    """This route kills the celery worker process corresponding to a provided task and also terminates the task"""
    client = Control(app)
    task_id = request.args.get('task_id')
    print(task_id, flush=True)
    client.revoke(task_id, terminate=True)
    return "OK"
