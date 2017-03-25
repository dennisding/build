# -*- encoding:utf-8 -*-

import pathlib

class Template:
	def __init__(self, root):
		self.root = pathlib.Path('template') / pathlib.Path(root)

	def open(self, name):
		path = self.root / '%s.template'%(name)

		return path.read_text()
