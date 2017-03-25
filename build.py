# encoding :utf-8 -*-

import pathlib

from utils import builder
from utils import argparser

def build():
	args = argparser.ArgParser()
	b = builder.Builder(args)
	b.build()

if __name__ == '__main__':
	build()