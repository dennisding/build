# -*- encoding:utf-8 -*-

import uuid
import pathlib

sourceSuffix = {'.cpp', '.c', '.cxx'}
headerSuffix = {'.h', '.hpp'}

class Project:
	def __init__(self, base, name):
		self.base = base
		self.name = name

		self.uuid = uuid.uuid4() # random uuid

	def prepare(self, projects):
		# prepare argument
		newRoot = self.base / pathlib.Path(self.root)
		self.root = newRoot.resolve()

		self.scanFiles()

	def scanFiles(self):
		self.sources = [] # sources
		self.headers = []

		def process(path):
			if not path.is_file():
				return

			if path.suffix in sourceSuffix:
				self.sources.append(path)
			elif path.suffix in headerSuffix:
				self.headers.append(path)

		self.walk(self.root, process)

	def walk(self, root, process):
		for child in root.iterdir():
			if child.is_file():
				process(child)
			else:
				self.walk(child, process)
