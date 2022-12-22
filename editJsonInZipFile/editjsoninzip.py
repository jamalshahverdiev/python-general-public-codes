#!/usr/bin/env python3
from argparse import ArgumentParser
from src.functions import main
from os import path
dir_path = path.dirname(path.realpath(__file__))

if __name__=="__main__":
        main(ArgumentParser, dir_path)

