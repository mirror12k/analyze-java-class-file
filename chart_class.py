#!/usr/bin/env python3


import sys


from java_code_tools import *
import classfile



class JavaClassChart(object):
	def __init__(self, classfile, **opts):
		self.classfile = classfile	
		self.classname = classfile.this_class
		self.superclassname = classfile.super_class
		self.classReferences = set()
		self.stringReferences = set()

		if opts.get('strings', False):
			self.parseStrings()

		if opts.get('classes', False):
			self.parseClassReferences()


	def parseClassReferences(self):
		for const in self.classfile.constants:
			if const is not None and const.tagName == 'CONSTANT_Class':
				self.classReferences.add(const.classname)
		self.classReferences = sorted(self.classReferences)
	def parseStrings(self):
		for const in self.classfile.constants:
			if const is not None and const.tagName == 'CONSTANT_String':
				self.stringReferences.add(repr(const.string))
		self.stringReferences = sorted(self.stringReferences)

	def __str__(self):
		s = classTypeToCode(self.classfile.access_flags) + ' ' + classNameToCode(self.classname)
		if classNameToCode(self.superclassname) != 'java.lang.Object':
			s +=  ' extends ' + classNameToCode(self.superclassname)
		if len(self.classfile.interfaces) > 0:
			if classTypeToCode(self.classfile.access_flags) == 'class':
				s += ' implements '
			else:
				s += ' extends '
			s += ', '.join(classNameToCode(interface) for interface in self.classfile.interfaces)
		if len(self.classReferences) > 0:
			s += '\n\tclasses:\n'
			s += '\n'.join( '\t\t' + classNameToCode(classname) for classname in self.classReferences )
		if len(self.stringReferences) > 0:
			s += '\n\tstrings:\n'
			s += '\n'.join( '\t\t' + string for string in self.stringReferences )
		return s
			



def main(*args):
	if len(args) == 0:
		print("argument required")
	else:
		opts = {}
		i = 0
		while i < len(args):
			arg = args[i]
			if arg == '--strings' or arg == '-s':
				opts['strings'] = True
			elif arg == '--classes' or arg == '-c':
				opts['classes'] = True
			else:
				cf = classfile.openFile(arg)
				cf.linkClassFile()
				cf.inlineClassFile()

				chart = JavaClassChart(cf, **opts)
				print (chart)
			i += 1




if __name__ == '__main__':
	main(*sys.argv[1:])
