# -*- encoding:utf-8 -*-

import pathlib

class Template:
	def __init__(self, root):
		self.root = pathlib.Path('templates') / pathlib.Path(root)

		self.caches = {} # {name:content}

	def open(self, name):
		path = self.root / ('%s.template'%(name))

		content = self.caches.get(path)
		if content:
			return content

		content = path.read_text()
		self.caches[path] = content

		return content
