# -*- encoding:utf-8 -*-

import uuid
import pathlib

from . import template

class ProjectBuilder:
	def __init__(self, name, project, builder):
		self.name = name
		self.project = project
		self.builder = builder

		self.prepare()

	def prepare(self):
		# self.filters = set()
		self.filters = {} # {filterId : None}
		self.sources = {} # {FileName : filters}
		self.includes = {} # {FileName : filters}

		self.processFiles(self.sources, 'Source Files', self.project.sources)
		self.processFiles(self.includes, 'Header Files', self.project.includes)

	def processFiles(self, types, prefix, files):
		for fileName in files:
			fileRelativePath = self.relativeTo(fileName, self.builder.outPath)
			filterName = self.relativeTo(fileName, self.project.sourceRoot).parent
			filterName = prefix / filterName

			#self.filters.add(filterName)
			self.filters[filterName] = None
			types[fileRelativePath] = filterName

	def relativeTo(self, source, target):
		sameParent = self.getSameParents(source, target)

		sourceRelative = source.relative_to(sameParent)
		targetRelative = target.relative_to(sameParent)

		# .. prefix
		parents = pathlib.Path()
		for index in range(len(targetRelative.parents)):
			parents = '..' / parents

		return parents / sourceRelative

	def getSameParents(self, path1, path2):
		part1, part2 = path1.parts, path2.parts

		result = []
		for index, part in enumerate(part1):
			if index >= len(part2):
				break

			if part != part2[index]:
				break

			result.append(part)

		return pathlib.Path(*result)

	def genFilterContent(self):
		maps = {}
		projectUuid = self.project.uuid
		maps['SourceFilesUuid'] = uuid.uuid3(projectUuid, 'Source Files')
		maps['IncludeFilesUuid'] = uuid.uuid3(projectUuid, 'Include Files')
		maps['ResourceFileUuid'] = uuid.uuid3(projectUuid, 'Resource Files')
		maps['Sources'] = self.genSources()
		maps['Includes'] = self.genIncludes()

		maps['Filters'] = self.genFilters()

		content = self.builder.template.open('filters')
		return content.format_map(maps)

	def genFilters(self):
		content = []

		template = self.builder.template.open('filter_filter')
		for filterId, _ in self.sortAndIter(self.filters):
			maps = {}
			maps['Uuid'] = uuid.uuid3(self.project.uuid, str(filterId))
			maps['FilterId'] = str(filterId)
			content.append(template.format_map(maps))

		return ''.join(content)

	def genSources(self):
		content = []
		template = self.builder.template.open('filter_compile')
		for fileName, filter in self.sortAndIter(self.sources):
			maps = {}
			maps['FileName'] = fileName
			maps['Filter'] = str(filter)
			content.append(template.format_map(maps))

		return ''.join(content)

	def sortAndIter(self, d):
		items = list(d.items())
		items.sort()
		for key, value in items:
			yield key, value

	def genIncludes(self):
		content = []
		template = self.builder.template.open('filter_include')
		for fileName, filter in self.sortAndIter(self.includes):
			maps = {}
			maps['FileName'] = fileName
			maps['Filter'] = filter
			content.append(template.format_map(maps))

		return ''.join(content)

	def genProjectContent(self):
		maps = {}
		maps['Uuid'] = self.project.uuid
		maps['ProjectName'] = self.project.name
		maps['Sources'] = self.getProjectSources()
		maps['Includes'] = self.getProjectIncludes()

		template = self.builder.template.open('project')

		return template.format_map(maps)

	def getProjectSources(self):
		content = []
		template = self.builder.template.open('project_source')
#		for fileName in self.sources:
		for fileName, filter in self.sortAndIter(self.sources):
			maps = {}
			maps['FileName'] = fileName
			content.append(template.format_map(maps))

		return ''.join(content)

	def getProjectIncludes(self):
		content = []
		template = self.builder.template.open('project_include')
		#for fileName in self.includes:
		for fileName, filter in self.sortAndIter(self.includes):
			maps = {}
			maps['FileName'] = fileName
			content.append(template.format_map(maps))

		return ''.join(content)

class SlnBuilder:
	def __init__(self, template, builder):
		self.template = template
		self.builder = builder

	def genSlnContent(self):
		template = self.template.open('sln')

		maps = {}
		maps['Projects'] = self.genSlnProjects()
		maps['ProjectConfigs'] = self.genSlnProjectConfigs()

		return template.format_map(maps)

	def genSlnProjects(self):
		content = []

		template = self.template.open('sln_project')
		for name, project in self.builder.iterProjects():
			maps = {}
			maps['Uuid'] = project.uuid
			maps['ProjectName'] = name

			content.append(template.format_map(maps))

		return ''.join(content)

	def genSlnProjectConfigs(self):
		content = []

		template = self.template.open('sln_config')
		for name, project in self.builder.iterProjects():
			maps = {}
			maps['Uuid'] = project.uuid
			content.append(template.format_map(maps))

		return ''.join(content)

class WinBuilder:
	def __init__(self, builder):
		self.builder = builder
		self.template = template.Template('vs2017')

	def build(self):
		self.prepare()

		self.buildProjects()
		self.buildSolution()

	def prepare(self):
		self.outPath = pathlib.Path(self.builder.args.target)
		self.outPath = self.outPath.resolve()

	def buildProjects(self):
		for name, project in self.builder.iterProjects():
			self.buildProject(name, project)

	def buildProject(self, name, project):
		builder = ProjectBuilder(name, project, self)

		self.genFilterFile(builder)
		self.genProjectFile(builder)

	def genProjectFile(self, builder):
		content = builder.genProjectContent()
		self.writeTo('%s.vcxproj'%(builder.name), content)

	def genFilterFile(self, builder):
		content = builder.genFilterContent()
		self.writeTo("%s.vcxproj.filters"%builder.name, content)

	def writeTo(self, name, content):
		outPath = self.outPath / name
		outPath.write_text(content)

	def buildSolution(self):
		builder = SlnBuilder(self.template, self.builder)
		content = builder.genSlnContent()

		self.writeTo('%s.sln'%(self.builder.args.name), content)
