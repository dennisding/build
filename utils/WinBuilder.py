# -*- encoding:utf-8 -*-

import template

class WinBuilder:
	def __init__(self, builder):
		self.builder = builder
		self.template = template.Template('vs2017')

	def build(self):
		pass
