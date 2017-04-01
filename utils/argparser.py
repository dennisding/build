# -*- encoding:utf-8 -*-

# build.py -DMACROS -e prj --exclude prj -e files
# -D define macros
# -e --exclude exclude project and file
#

import argparse

def parseArgs():
	parser = argparse.ArgumentParser(description = 'build system')
	# add definitions
	parser.add_argument('-D', dest = 'macros', \
			action = 'append', default = [])

	parser.add_argument('-p', '--platform', dest = 'platforms', \
				action = 'append', default = ['win'])

	parser.add_argument('name')
	parser.add_argument('source')
	parser.add_argument('target')

	return parser.parse_args()
