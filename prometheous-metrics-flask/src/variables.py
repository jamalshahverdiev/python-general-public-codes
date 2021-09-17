from flask import Flask
from os import environ, getcwd
from sys import argv, exit
from src.flask_logs import LogSetup
from prometheus_client import Counter, Summary, Histogram, Gauge

app = Flask(__name__)
db_timer = Histogram('slow', 'Slow Requests', ['endpoint'])
view_metric = Counter('view', 'Product view', ['product'])
buy_metric = Counter('buy', 'Product buy', ['product'])
root_counter = Counter(
    'requests', 'Number of requests served, by http code', ['http_code'])
root_gauge = Gauge('rate_requests', 'Rate of success requests')
parameters_metric = Counter(
    'request_with_params', 'Query string request parameters', ['name', 'surname', 'age'])
getlang_params_metric = Counter(
    'getlang_params', 'Getlang query string request parameters', ['language'])
saveviaapi_metric = Counter(
    'save_api_requests', 'Request content', ['method', 'endpoint'])
duration_getlang = Summary('duration_getlang_seconds',
                           'Time spent in the get_lang() function')
durationsaveviaapi = Summary('duration_saveviaapi_seconds',
                             'Time spent in the save_via_api() function')

durationviewproduct = Summary('duration_viewproduct_seconds',
                              'Time spent in the view_product() function')
durationbyproduct = Summary('duration_byproduct_seconds',
                            'Time spent in the buy_product() function')

durationparameters = Summary('duration_queryparams_seconds',
                             'Time spent in the query_params() function')

file_path_to_save = "{0}/output".format(getcwd())
responce_500 = 0
responce_200 = 0
rate_responce = 0
# Input variable to generate an internal 500 error at the desired rate
if len(argv) < 2:
    print("Usage: python app.py 50 # Input variable to generate an internal 500 error at the desired rate for metrics")
    exit(1)
else:
    success_rate = argv[1]

# Logging Setup - This would usually be stuffed into a settings module
# Default output is a Stream (stdout) handler, also try out "watched" and "file"
# Stream type of logging
# app.config["LOG_TYPE"] = os.environ.get("LOG_TYPE", "stream")
# app.config["LOG_LEVEL"] = os.environ.get("LOG_LEVEL", "INFO")

# Watched type of logging
# app.config['LOG_DIR'] = os.environ.get("LOG_DIR", "./")
# app.config['APP_LOG_NAME'] = os.environ.get("APP_LOG_NAME", "app.log")
# app.config['WWW_LOG_NAME'] = os.environ.get("WWW_LOG_NAME", "www.log")
# app.config["LOG_TYPE"] = os.environ.get("LOG_TYPE", "watched")
# app.config["LOG_LEVEL"] = os.environ.get("LOG_LEVEL", "INFO")

# File type of logging
app.config["LOG_TYPE"] = environ.get("LOG_TYPE", "file")
app.config["LOG_LEVEL"] = environ.get("LOG_LEVEL", "INFO")
app.config['LOG_DIR'] = environ.get("LOG_DIR", file_path_to_save)
app.config['APP_LOG_NAME'] = environ.get("APP_LOG_NAME", "app.log")
app.config['WWW_LOG_NAME'] = environ.get("WWW_LOG_NAME", "www.log")
app.config['LOG_MAX_BYTES'] = environ.get(
    "LOG_MAX_BYTES", 100_000_000)  # 100MB in bytes
app.config['LOG_COPIES'] = environ.get("LOG_COPIES", 5)

logs = LogSetup()
logs.init_app(app)
