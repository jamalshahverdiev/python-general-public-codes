#!/usr/bin/env python
import os.path
from flask import Flask, request, render_template
from separated_func_file import ip_access, auth_required
from os import system

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/activity', methods=['GET']) 
@ip_access
@auth_required
def usersActivity():
    if 'username' in request.args:
        filePath = "{}/{}/{}.html".format(os.getcwd(), 'templates', request.args['username'])
        if os.path.isfile(filePath):
            fileToRender = filePath.split('/')[-1]
            return render_template(fileToRender)
        else:
            return "Cannot find entered username", 404 
    else:
        return "Required parameter: username", 404


@app.route('/users', methods=['GET'])
@ip_access
@auth_required
def getAllUsers():
    formattedUserNames = []
    dirPathToSearch = "{}/{}".format(os.path.dirname(os.path.abspath(__file__)), 'templates/')
    extensionsToSearch = ['html']

    file_names = [fn for fn in os.listdir(dirPathToSearch)
                  if any(fn.endswith(ext) for ext in extensionsToSearch)]
    
    for name in file_names:
        formattedUserNames.append(name.replace('.html', ''))
    
    return str(formattedUserNames)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
