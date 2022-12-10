from os import path, getcwd, listdir
from flask import request, render_template
from src.functions import ip_access, auth_required
from src.variables import app

@app.route('/activity', methods=['GET']) 
@ip_access
@auth_required
def usersActivity():
    if 'username' in request.args:
        filePath = "{}/{}/{}.html".format(getcwd(), 'templates', request.args['username'])
        if path.isfile(filePath):
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
    dirPathToSearch = "{}/{}".format(path.dirname(path.abspath(__file__)), 'templates/')
    extensionsToSearch = ['html']

    file_names = [fn for fn in listdir(dirPathToSearch)
                  if any(fn.endswith(ext) for ext in extensionsToSearch)]
    
    for name in file_names:
        formattedUserNames.append(name.replace('.html', ''))
    
    return str(formattedUserNames)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
