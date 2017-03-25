# -*- encoding:utf-8 -*-

import pathlib
import WinBuilder

class Builder:
	def __init__(self, args):
		self.args = args
		self.source = pathlib.Path(args.source).resolve()
		self.target = pathlib.Path(args.target).resolve()

		self.projects = {} # {name: projects}

	def build(self):
		self.findProjects()
		self.prepareProjects()
		self.genSolutions()

	def genSolutions(self):
		if 'win' in self.args.platforms:
			self.genWinSolution()
		elif 'android' in self.args.platforms:
			self.genAndroidSolution()

	def genWinSolution(self):
		builder = WinBuilder.WinBuilder(self)
		builder.build()

	def prepareProjects(self):
		for project in self.projects.values():
			project.prepare(self.projects)

	def findProjects(self):
		for child in self.source.iterdir():
			if not child.is_file():
				continue

			name = child.name
			if name.startswith('project_') and name.endswith('.py'):
				self.addProject(name[len('project_'): -len('.py')], child)

	def addProject(self, name, path):
		code = path.read_text()
		env = {}
		exec(code, env, env)

		self.projects[name] = env['Project'](path.parent, name)
