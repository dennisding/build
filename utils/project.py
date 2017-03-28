# -*- encoding:utf-8 -*-

import uuid
import pathlib

sourceSuffix = {'.cpp', '.c', '.cxx'}
headerSuffix = {'.h', '.hpp'}

class Project:
	def __init__(self, base, name):
		self.base = base
		self.name = name
		self.sourceRoot = ''
		self.includeRoot = ''

		self.uuid = uuid.uuid4() # random uuid
		self.uuid = str(self.uuid).upper()

	def prepare(self, projects):
		# prepare argument
		self.prepareEnv()

		self.scanFiles()
		self.genFilters()

	def prepareEnv(self):
		newRoot = self.base / pathlib.Path(self.root)
		self.root = newRoot.resolve()

		self.sourceRoot = self.root / self.sourceRoot
		self.includeRoot = self.root / self.includeRoot

	def genFilters(self):
		pass

	def scanFiles(self):
		self.sources = [] # sources
		self.includes = []

		def process(path):
			if not path.is_file():
				return

			if path.suffix in sourceSuffix:
				self.sources.append(path)
			elif path.suffix in headerSuffix:
				self.includes.append(path)

		self.walk(self.root, process)

	def walk(self, root, process):
		for child in root.iterdir():
			if child.is_file():
				process(child)
			else:
				self.walk(child, process)

class LibProject(Project):
	projectType = 'Lib'

class ExeProject(Project):
	projectType = 'Exe'
