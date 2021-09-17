# from src.useful_funcs import return_mutliple_type_logs
from random import randrange
from flask import current_app, request
from werkzeug.utils import secure_filename
# from os import path
from json import load
from src.variables import (
    app,
    file_path_to_save,
    db_timer,
    view_metric,
    buy_metric,
    parameters_metric,
    getlang_params_metric,
    saveviaapi_metric,
    durationsaveviaapi,
    durationviewproduct,
    durationbyproduct,
    durationparameters,
    duration_getlang,
    responce_500,
    responce_200,
    rate_responce,
    success_rate,
    root_counter,
    root_gauge)
from prometheus_client import generate_latest
from time import sleep
from random import uniform


@app.route("/")
def main_endpoint():
    global responce_500
    global responce_200
    global rate_responce
    if randrange(1, 100) > int(success_rate):
        root_counter.labels(http_code='500').inc()
        responce_500 = responce_500 + 1
        rate_responce = responce_500 / (responce_500+responce_200) * 100
        root_gauge.set(rate_responce)
        return "Internal Server Error\\n", 500
    else:
        root_counter.labels(http_code='200').inc()
        responce_200 = responce_200 + 1
        rate_responce = responce_500 / (responce_500+responce_200) * 100
        root_gauge.set(rate_responce)
        # return_mutliple_type_logs(current_app)
        return "Response from / endpoint!"


@app.route('/view/<id>')
@durationviewproduct.time()
def view_product(id):
    view_metric.labels(product=id).inc()
    sleep(uniform(0, 5))
    return "View %s" % id


@app.route('/buy/<id>')
@durationbyproduct.time()
def buy_product(id):
    buy_metric.labels(product=id).inc()
    sleep(uniform(0, 5))
    return "Buy %s" % id


@app.route('/query_params', methods=['GET'])
@durationparameters.time()
def query_params():
    name = request.args['name']
    surname = request.args['surname']
    age = request.args['age']
    parameters_metric.labels(name=name, surname=surname, age=age).inc()
    return '''<h1>The Query String are...{}:{}:{}</h1>''' .format(name, surname, age)


@app.route('/save_via_api', methods=['GET', 'POST'])
@durationsaveviaapi.time()
def save_via_api():
    uploaded_file = request.files['document']
    data = load(request.files['data'])
    filename = secure_filename(uploaded_file.filename)
    uploaded_file.save("{}/new_{}".format(file_path_to_save, filename))
    print(data)
    saveviaapi_metric.labels(method=request.method,
                             endpoint=request.path).inc()
    sleep(uniform(0, 10))
    return 'success'


@app.route('/get_lang')
@duration_getlang.time()
def get_lang():
    # if key doesn't exist, returns None
    language = request.args.get('language')
    getlang_params_metric.labels(language=language).inc()
    return '''<h1>The language value is: {}</h1>'''.format(language)


@app.route('/database')
def database():
    with db_timer.labels('/database').time():
        # simulated database response time
        sleep(uniform(1, 3))
    return '<h1>Completed expensive database operation</h1>'


@app.route('/metrics')
def metrics():
    return generate_latest()
