from json import dumps
from requests import post
from os import getcwd

file_path_to_save = "{0}/output".format(getcwd())
data = {'test1': 1, 'test2': 2}

filename = "{0}/{1}".format(file_path_to_save, 'somefile.txt')
with open(filename, 'w') as f:
    f.write('this is a test file\nnew line appended\nThird line in file\nFourth line from file\nFifth line from file')

url = "http://10.100.100.100:8000/save_via_api"

files = [
    ('document', (filename, open(filename, 'rb'), 'application/octet')),
    ('data', ('data', dumps(data), 'application/json')),
]

r = post(url, files=files)
print(r)
