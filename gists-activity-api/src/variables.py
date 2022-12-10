from os import getcwd, path, environ
from flask import Flask
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
username = 'pipedrive'
password = 'pipedrive'
accessList = "{}/{}".format(getcwd(), 'templates/access_list.txt')
formattedFilePath = "{}/{}".format(path.dirname(path.abspath(__file__)), 'templates/output.txt')
userNames=['unixidzero']
gitHubSite='https://api.github.com'
data = {}
url = 'https://api.pipedrive.com/v1/deals'
headers = {'content-type': 'application/json'}
token = environ.get('PIPEDRIVE_API_TOKEN')
params = {'api_token': token }