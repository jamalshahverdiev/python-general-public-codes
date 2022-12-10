#!/usr/bin/env python
import requests, json, os.path, os
from separated_func_file import createGistStruct, replaceInFile, openFileToIterate, getGistNamesFromFile, deleteLine, postToPipeDrive, putDeletePipeDrive, getIdByTitle, createPostObjects

formattedFilePath = "{}/{}".format(os.path.dirname(os.path.abspath(__file__)), 'templates/output.txt')
userNames=['unixidzero']
gitHubSite='https://api.github.com'
data = {}
url = 'https://api.pipedrive.com/v1/deals'
headers = {'content-type': 'application/json'}
token = os.environ.get('PIPEDRIVE_API_TOKEN')
params = {'api_token': token }

for username in userNames:
    print("Started iteration for user: ", username)
    filePath = "{}/{}/{}.html".format(os.path.dirname(os.path.abspath(__file__)), 'templates', username)
    URL='{}/users/{}/gists'.format(gitHubSite,username)
    response = requests.get(url=URL)
    gists = response.json() 

    if os.path.isfile(filePath) and os.path.getsize(filePath) > 0:
        loglist = openFileToIterate(filePath, 'read', username)
        for realGistLine in createGistStruct(gists):
            gistName = realGistLine.split('__')[1]
            if gistName not in loglist:
                postObjects = createPostObjects(realGistLine)
                postToPipeDrive(data, postObjects[0], postObjects[1], url, params, headers)
                with open(filePath, 'a') as outFile:
                    outFile.write(realGistLine + '\n')
                    outFile.write('<br>' + '\n')
            if realGistLine not in loglist:
                idGist = realGistLine.split('__')[4]
                with open(filePath) as newfile:
                    for fileLine in newfile.readlines():
                        if idGist in fileLine:
                            replaceInFile(filePath, fileLine.rstrip(), realGistLine)
                            putDeletePipeDrive(data, fileLine.split('__')[1], 'open', url, params, headers)
                            print("GIST file updated with line:", realGistLine)
    else:
        with open(filePath, 'a') as outFile:
            for line in createGistStruct(gists):
                postObjects = createPostObjects(line)
                postToPipeDrive(data, postObjects[0], postObjects[1], url, params, headers)
                outFile.write(line + '\n')
                outFile.write('<br>' + '\n')
        print ("Created new GIST file for user: {}".format(username))

    if os.path.isfile(filePath) and os.path.getsize(filePath) > 0:
        unmatchedLines = []
        realGistLines = """{}""".format('\n'.join(createGistStruct(gists)[0:]))
        for fileGistLine in getGistNamesFromFile(filePath, 'readlines', username):
            if fileGistLine not in realGistLines:
                print("Gistname {} doesn't exists on GitHub".format(fileGistLine))
                putDeletePipeDrive(data, fileGistLine, 'deleted', url, params, headers)
                unmatchedLines.append(fileGistLine)
        deleteLine(filePath, formattedFilePath, unmatchedLines)
        print("This Gist names don't exists in gist api: ", unmatchedLines)
