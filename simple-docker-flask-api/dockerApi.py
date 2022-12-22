#!/usr/bin/env python3
from os import popen, system
from flask import request, jsonify
from src.variables import app, ipaddr, port_to_listen

@app.route('/getRunningContainers', methods = ['GET'])
def api_getcontainer():
    return jsonify(popen('docker ps | grep -v CONTAINER').readlines())

@app.route('/createcontainer', methods = ['POST'])
def api_createcontainer():

    if request.headers['Content-Type'] == 'text/plain':
        return "Text Message: " + request.data

    elif request.headers['Content-Type'] == 'application/json':
        if (request.json):
            imagename = str(request.json['imagename'])
            containername = str(request.json['containername'])
            daemonize = str(request.json['daemonize'])            
            exposedPort = str(request.json['exposedPort'])            
            cmd = ('docker run -d --name {} -p {}:80 {}'.format(containername, exposedPort, imagename))

            if imagename and containername:
                if system(cmd) == 0:
                    print("Docker executed successful!")
                    return (str(system('docker ps | grep {}'.format(containername))))
                else:
                    print("Docker run time happened somtheing wrong!")
        else:
            return "JSON content is wrong!!!"

    elif request.headers['Content-Type'] == 'application/octet-stream':
        f = open('./binary', 'wb')
        f.write(request.data)
        f.close()
        return "Binary message written!"

    else:
        return "415 Unsupported Media Type ;)"

@app.route('/getcontainer', methods = ['GET'])
def api_hello():
    if 'name' in request.args:
        return jsonify(popen('docker ps | grep {}$'.format(request.args['name'])).readlines())
    else:
        return 'To get Container status please use ?name= argument in the url.'

if __name__ == '__main__':
    app.run(host=ipaddr, port=port_to_listen, debug=True)
