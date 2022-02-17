# Flask
from flask import Flask, request, jsonify, url_for

app = Flask(__name__)
app.debug = True

# OS
import os, stat
import shutil
from werkzeug.utils import secure_filename
app.config['ROOT'] = os.path.dirname(os.path.abspath(__file__))

# CORS
from flask_cors import CORS
cors = CORS(app, expose_headers=["location", "task_id"])

# Helpers
import json
from helpers.validation import validate_schema, allowed_extensions
from helpers.errors import bad_request

# Model
from learning.refactor import model

# Routes
from blueprints.routes import tasks
app.register_blueprint(tasks, url_prefix="/tasks")

@app.route('/healthcheck', methods=['GET'])
def health():
    """This route enables the front-end to determine whether the server is alive and listening."""
    return "OK"


@app.route('/predict', methods=['POST'])
def predict():
    """This route validates incoming data from the Hydro+Storage Tool front-end,
    and subsequently passes the form data and profiles (.csv's) to the machine learning model.
    """
    form = request.form.to_dict()
    

    # Here is the dictionary of form data coming from the user
    data = json.loads(form.get('data'))

    try:
        energy_profile = request.files.get('electricity')
        price_profile = request.files.get('price')

        # Ensure only .csv files are allowed
        allowed_extensions(energy_profile.filename)
        allowed_extensions(price_profile.filename)

        # Ensure the .csv files are compliant with the required schema
        validate_schema(energy_profile, "electricity")
        validate_schema(price_profile, "price")

        try:
            os.mkdir(f"{app.config['ROOT']}/static/{data['uuid']}")
            os.mkdir(f"{app.config['ROOT']}/static/{data['uuid']}/upload")
            os.mkdir(f"{app.config['ROOT']}/static/{data['uuid']}/plots")
            os.mkdir(f"{app.config['ROOT']}/static/{data['uuid']}/csv")

            energy_profile.stream.seek(0)
            price_profile.stream.seek(0)


            energy_profile.save(os.path.join(f"{app.config['ROOT']}/static/{data['uuid']}/upload", secure_filename(energy_profile.filename)))
            price_profile.save(os.path.join(f"{app.config['ROOT']}/static/{data['uuid']}/upload", secure_filename(price_profile.filename)))

            os.chmod(f"{app.config['ROOT']}/static/{data['uuid']}", 0o777)
            os.chmod(f"{app.config['ROOT']}/static/{data['uuid']}/upload", 0o777)
            os.chmod(f"{app.config['ROOT']}/static/{data['uuid']}/plots", 0o777)
            os.chmod(f"{app.config['ROOT']}/static/{data['uuid']}/csv", 0o777)
        except Exception as e:
            shutil.rmtree(f"{app.config['ROOT']}/static/{data['uuid']}", ignore_errors=True)
            return bad_request(str(e))

        task = model.delay(data, secure_filename(energy_profile.filename), secure_filename(price_profile.filename))

    except Exception as e:
        shutil.rmtree(f"{app.config['ROOT']}/static/{data['uuid']}", ignore_errors=True)
        return bad_request(str(e))

    return jsonify({}), 202, {'location': url_for('tasks.status', task_id=task.task_id), 'task_id': task.task_id}

if __name__ == '__main__':
    app.run(host='0.0.0.0')