# -*- encoding:utf-8 -*-

from utils import project

class Project(project.Project):
	def __init__(self, base, name):
		super().__init__(base, name)

		self.root = '../src/freetype-2.7.1'

		self.macros = []
		self.depends = []

		self.plaotforms = {} # ios win android
		self.configs = {} # debug release, hybrid
