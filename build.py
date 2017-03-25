# encoding :utf-8 -*-

from utils import builder
from utils import argparser

def build():
	args = argparser.parseArgs()
	b = builder.Builder(args)
	b.build()

if __name__ == '__main__':
	build()