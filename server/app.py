# Flask
import stat
import os
from blueprints.routes import tasks
from learning.refactor import model
from helpers.errors import bad_request
from helpers.validation import validate_schema, allowed_extensions
import json
from flask_cors import CORS
from werkzeug.utils import secure_filename
import shutil
from flask import Flask, request, jsonify, url_for

app = Flask(__name__)
app.debug = True

# OS
app.config['ROOT'] = os.path.dirname(os.path.abspath(__file__))

# CORS
cors = CORS(app, expose_headers=["location", "task_id"])

# Helpers

# Model

# Routes
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

        energy_profile.stream.seek(0)
        price_profile.stream.seek(0)

        Revenue_Plot, ROI_Plot, Payback_Plot, Battery_Degradation_Daily, Battery_Degradation_Annual, Financial_Performance_Daily, Financial_Performance_Annual = model(
            data, energy_profile, price_profile)
    except Exception as e:
        return bad_request(str(e))

    return {"plots": {"Revenue_Plot": Revenue_Plot, "ROI_Plot": ROI_Plot, "Payback_Plot": Payback_Plot},
            "csv": {"Battery_Degradation_Daily": Battery_Degradation_Daily, "Battery_Degradation_Annual": Battery_Degradation_Annual, "Financial_Performance_Daily": Financial_Performance_Daily, "Financial_Performance_Annual": Financial_Performance_Annual}
            }


if __name__ == '__main__':
    app.run(host='0.0.0.0')
