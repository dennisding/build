# -*- encoding:utf-8 -*-

import uuid
import pathlib

from . import platform
from . import configs

BASE_UUID = uuid.UUID('1fa4a144-302f-4b31-8ba3-b97d6ae0b47f')

sourceSuffix = {'.cpp', '.c', '.cxx'}
headerSuffix = {'.h', '.hpp'}

class Project:
	def __init__(self, base, name):
		self.base = base
		self.name = name
		self.sourceRoot = ''
		self.includeRoot = ''
		self.projectType = 'Exe'

		# self.uuid = uuid.uuid4() # random uuid
		self.uuid = uuid.uuid3(BASE_UUID, name)

	def prepare(self, projects):
		# prepare argument
		self.prepareEnv()
		self.preparePlatforms()
		self.prepareConfigs()

		self.scanFiles()

	def preparePlatforms(self):
		for key, value in configs.items():
			if key not in self.platforms:
				self.platforms[key] = getattr(platforms, value)()

	def prepareConfigs(self):
		pass

	def prepareEnv(self):
		newRoot = self.base / pathlib.Path(self.root)
		self.root = newRoot.resolve()

		self.sourceRoot = self.root / self.sourceRoot
		self.includeRoot = self.root / self.includeRoot

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

	def getDict(self, name, platform, config):
		return {}

class LibProject(Project):
	projectType = 'Lib'

class ExeProject(Project):
	projectType = 'Exe'

class DllProject(Project):
	projectType = 'Dll'