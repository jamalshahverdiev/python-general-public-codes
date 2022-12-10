import os.path, shutil, json, requests
from flask import make_response, request, abort
from functools import wraps

username = 'pipedrive'
password = 'pipedrive'
accessList = "{}/{}".format(os.getcwd(), 'templates/access_list.txt')

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == username and auth.password == password:
            return f(*args, **kwargs)

        return make_response('Login and password required!', 400, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

    return decorated

def ip_access(f):
    @wraps(f)
    def wrapped(*args, **kwargs):

        with open(accessList, 'r') as filehandle:
            filecontents = filehandle.readlines()
            API_ALLOWED_IPS = list(map(lambda x:x.strip(),filecontents))

        for IP in API_ALLOWED_IPS:
            if str(request.remote_addr).startswith(IP) or str(request.remote_addr) == IP:
                return f(*args, **kwargs)
        return 'Your IP Is Not allowed ' + request.remote_addr
    return wrapped

def openFileToIterate(filePath, compareIf, username):
    logfile = open(filePath)
    if compareIf == 'readlines':
        loglist = logfile.readlines()
    else:
        loglist = logfile.read()
    logfile.close()
    return loglist

def createGistStruct(gistObject):
    gist_list = []
    for each_gist in gistObject:
        filename=list(each_gist['files'].keys())[0]
        gistFileName = each_gist['files'][filename]['filename']
        userId = each_gist['owner']['id']
        gistId = each_gist['id']
        gistUpdated = each_gist['updated_at'].replace('-', '_').replace(':', '_').replace('T', '_').replace('Z','')
        gistCreated = each_gist['created_at'].replace('-', '_').replace(':', '_').replace('T', '_').replace('Z','')
        gist_list.append("{}__{}__Updated_{}__Created_{}__{}".format(userId,gistFileName,gistUpdated,gistCreated,gistId))

    return gist_list

def getGistNamesFromFile(filePath, compareIf, username):
    gistNamesInFile = []
    for line in openFileToIterate(filePath, compareIf, username):
        if '<br>' not in line:
            gistNamesInFile.append(line.split('__')[1])
    return gistNamesInFile

def deleteLine(inputFile, outputFile, stringToMatchs):
    with open(inputFile) as oldfile, open(outputFile, 'w') as newfile:
        for line in oldfile:
            if not any(bad_word in line for bad_word in stringToMatchs):
                newfile.write(line)
    shutil.copyfile(outputFile, inputFile)
    os.remove(outputFile)

def replaceInFile(file_path, old_line, new_line):
    with open(file_path,'r+') as f:
        filedata = f.read()
        filedata = filedata.replace(old_line,new_line)
        f.seek(0)
        f.truncate(0)
        f.write(filedata)

def postToPipeDrive(dictObj, gistName, addTime, url, params, headers):
    dictObj['title'] = gistName
    dictObj['add_time'] = addTime
    dictObj['status'] = 'open'
    dictObj['org_id'] = 10000
    dictObj['value'] = 100
    return requests.post(url, 
                params=params, 
                data=json.dumps(dictObj, sort_keys=True, indent=3), 
                headers=headers
            )

def putDeletePipeDrive(dictObj, gistName, state, url, params, headers):
    idOfDeal = getIdByTitle(url, params, gistName)
    dictObj['id'] = idOfDeal
    dictObj['title'] = gistName
    if state == 'deleted':
        dictObj['status'] = 'deleted'
    else:
        dictObj['status'] = 'open'
    return requests.put('{}/{}'.format(url, idOfDeal), 
                    params=params, 
                    data=json.dumps(dictObj, sort_keys=True, indent=3), 
                    headers=headers
                )

def getIdByTitle(url, params, title):
    response = requests.get(url, params)
    for content in response.json()['data']:
        if content['title'] == title:
            return content['id']

def createPostObjects(lineObject):
    postDataList = []
    postDataList.append(lineObject.split('__')[1])
    timeValue = lineObject.split('__')[3].split('_')[1:]
    postDataList.append('{}-{}-{} {}:{}:{}'.format(timeValue[0], timeValue[1], timeValue[2], timeValue[3], timeValue[4], timeValue[5]))
    return postDataList