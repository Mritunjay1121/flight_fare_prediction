# from flask import Flask
# from housing.logger import logging
# import sys
# from housing.exception import FlightfareException
# app=Flask(__name__)

# @app.route("/",methods=['GET','POST'])
# def index():
#     # logging.info("WE are testing")


#     try:
#         raise Exception("We are testing exception") 
#     except Exception as e:
#         housing=FlightfareException(e,sys)
#         logging.info(housing.error_message)
#         logging.info("We are testing logging")
#     return "I have arrived"


# if __name__=="__main__":
#     app.run(debug=True)
    

from flask import Flask, request
import sys

import pip
from housing.util.util import read_yaml_file, write_yaml_file
from matplotlib.style import context
from housing.logger import logging
from housing.exception import FlightfareException
import os, sys
import json
from housing.config.configuration import Configuartion
from housing.constant import CONFIG_DIR, get_current_time_stamp
from housing.pipeline.pipeline import Pipeline
from housing.entity.flight_fare_predictor import FlighFarePredictor, FlightFareData
from flask import send_file, abort, render_template


ROOT_DIR = os.getcwd()
LOG_FOLDER_NAME = "flight_fare_logs"
PIPELINE_FOLDER_NAME = "housing"
SAVED_MODELS_DIR_NAME = "saved_models"
MODEL_CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, "model.yaml")
LOG_DIR = os.path.join(ROOT_DIR, LOG_FOLDER_NAME)
PIPELINE_DIR = os.path.join(ROOT_DIR, PIPELINE_FOLDER_NAME)
MODEL_DIR = os.path.join(ROOT_DIR, SAVED_MODELS_DIR_NAME)


from housing.logger import get_log_dataframe

FLIGHT_DATA_KEY = "flight_data"
PRICE_VALUE_KEY = "Price"

app = Flask(__name__)


@app.route('/artifact', defaults={'req_path': 'housing'})
@app.route('/artifact/<path:req_path>')
def render_artifact_dir(req_path):
    os.makedirs("housing", exist_ok=True)
    # Joining the base and the requested path
    print(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        if ".html" in abs_path:
            with open(abs_path, "r", encoding="utf-8") as file:
                content = ''
                for line in file.readlines():
                    content = f"{content}{line}"
                return content
        return send_file(abs_path)

    # Show directory contents
    files = {os.path.join(abs_path, file_name): file_name for file_name in os.listdir(abs_path) if
             "artifact" in os.path.join(abs_path, file_name)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('files.html', result=result)


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return str(e)


@app.route('/view_experiment_hist', methods=['GET', 'POST'])
def view_experiment_history():
    experiment_df = Pipeline.get_experiments_status()
    context = {
        "experiment": experiment_df.to_html(classes='table table-striped col-12')
    }
    return render_template('experiment_history.html', context=context)


@app.route('/train', methods=['GET', 'POST'])
def train():
    message = ""
    pipeline = Pipeline(config=Configuartion(current_time_stamp=get_current_time_stamp()))
    if not Pipeline.experiment.running_status:
        message = "Training started."
        pipeline.start()
    else:
        message = "Training is already in progress."
    context = {
        "experiment": pipeline.get_experiments_status().to_html(classes='table table-striped col-12'),
        "message": message
    }
    return render_template('train.html', context=context)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    context = {
        FLIGHT_DATA_KEY: None,
        PRICE_VALUE_KEY: None
    }

    if request.method == 'POST':
        Total_Stops = float(request.form['Total_Stops'])
        Journey_day = float(request.form['Journey_day'])
        Journey_month = float(request.form['Journey_month'])
        Dep_hour = float(request.form['Dep_hour'])
        Dep_min = float(request.form['Dep_min'])
        Arrival_hour = float(request.form['Arrival_hour'])
        Arrival_min = float(request.form['Arrival_min'])
        Duration_hours = float(request.form['Duration_hours'])
        Duration_mins = float(request.form['Duration_mins'])
        Airline = request.form['Airline']
        Source = request.form['Source']
        Destination = request.form['Destination']




        flightfareData_data = FlightFareData(Total_Stops=Total_Stops,
                                   Journey_day=Journey_day,
                                   Journey_month=Journey_month,
                                   Dep_hour=Dep_hour,
                                   Dep_min=Dep_min,
                                   Arrival_hour=Arrival_hour,
                                   Arrival_min=Arrival_min,
                                   Duration_hours=Duration_hours,
                                   Duration_mins= Duration_mins,
                                   Airline=Airline,
                                   Source=Source,
                                   Destination=Destination)
        flight_df = flightfareData_data.get_housing_input_data_frame()
        flight_predictor = FlighFarePredictor(model_dir=MODEL_DIR)
        price_value = flight_predictor.predict(X=flight_df)
        context = {
            FLIGHT_DATA_KEY: flightfareData_data.get_housing_data_as_dict(),
            PRICE_VALUE_KEY: price_value,
        }
        return render_template('predict.html', context=context)
    return render_template("predict.html", context=context)


@app.route('/saved_models', defaults={'req_path': 'saved_models'})
@app.route('/saved_models/<path:req_path>')
def saved_models_dir(req_path):
    os.makedirs("saved_models", exist_ok=True)
    # Joining the base and the requested path
    print(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('saved_models_files.html', result=result)


@app.route("/update_model_config", methods=['GET', 'POST'])
def update_model_config():
    try:
        if request.method == 'POST':
            model_config = request.form['new_model_config']
            model_config = model_config.replace("'", '"')
            print(model_config)
            model_config = json.loads(model_config)

            write_yaml_file(file_path=MODEL_CONFIG_FILE_PATH, data=model_config)

        model_config = read_yaml_file(file_path=MODEL_CONFIG_FILE_PATH)
        return render_template('update_model.html', result={"model_config": model_config})

    except  Exception as e:
        logging.exception(e)
        return str(e)


@app.route(f'/logs', defaults={'req_path': f'{LOG_FOLDER_NAME}'})
@app.route(f'/{LOG_FOLDER_NAME}/<path:req_path>')
def render_log_dir(req_path):
    os.makedirs(LOG_FOLDER_NAME, exist_ok=True)
    # Joining the base and the requested path
    logging.info(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        log_df = get_log_dataframe(abs_path)
        context = {"log": log_df.to_html(classes="table-striped", index=False)}
        return render_template('log.html', context=context)

    # Show directory contents
    files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('log_files.html', result=result)


if __name__ == "__main__":
    app.run(port=5000)