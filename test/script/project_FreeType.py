# -*- encoding:utf-8 -*-

from utils import project
from utils import platform
from utils import configs

class Project(project.LibProject):
	def __init__(self, base, name):
		super().__init__(base, name)

		self.root = '../src/freetype-2.7.1/src'

		self.macros = {} # {name:value}
		self.depends = []

		self.platforms = {} # ios win android
		self.configs = {} # debug release, hybrid

		self.sourceRoot = ''
		self.includeRoot = ''
