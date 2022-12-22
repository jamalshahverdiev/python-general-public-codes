#!/usr/bin/env python3
from os import popen

def returnArg(arg):
    my_dict = {"containerID": arg.split()[0], "imageName": arg.split()[1], "exposedPort": arg.split()[-2], "containerName": arg.split()[-1]}
    print(my_dict)
    return my_dict

for line in list(popen("docker ps | grep -v CONTAINER").readlines()):
    returnArg(line)
