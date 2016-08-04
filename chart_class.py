#!/usr/bin/env python3


import sys


from java_code_tools import *
import classfile
import classbytecode



class JavaClassChart(object):
	def __init__(self, classfile, **opts):
		self.classfile = classfile	
		self.classname = classfile.this_class
		self.superclassname = classfile.super_class
		self.classReferences = set()
		self.stringReferences = set()
		self.constantReferencesByMethod = {}
		self.methodsList = set()
		self.fieldsList = set()

		if opts.get('strings', False):
			self.parseStrings()
		if opts.get('constants_by_method', False):
			self.parseConstantsByMethod()
		if opts.get('classes', False):
			self.parseClassReferences()
		if opts.get('methods', False):
			self.parseMethods()
		if opts.get('fields', False):
			self.parseFields()


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
	def parseConstantsByMethod(self):
		for method in self.classfile.methods:
			if not method.isAbstract():
				referencedConstants = set()
				for i in range(len(method.codeStructure['code'])):
					inst = method.codeStructure['code'][i]
					if type(inst) == str and inst in classbytecode.assemblyConstantReferenceListing:
						referencedConstants.add(stringConstantSimple(method.codeStructure['code'][i+1]))

				referencedConstants = sorted(referencedConstants)

				methodpointer = methodToMethodDescription(method)
				self.constantReferencesByMethod[methodpointer] = referencedConstants

	def parseMethods(self):
		for method in self.classfile.methods:
			self.methodsList.add(methodToMethodDescription(method))
		self.methodsList = sorted(self.methodsList)
	def parseFields(self):
		for field in self.classfile.fields:
			self.fieldsList.add(fieldToFieldDescription(field))
		self.fieldsList = sorted(self.fieldsList)

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
		if len(self.constantReferencesByMethod) > 0:
			s += '\n\tconstants by method:\n'
			for methodpointer in self.constantReferencesByMethod:
				s += '\n\t\t' + methodpointer + ':\n'
				s += '\n'.join( '\t\t\t' + str(const) for const in self.constantReferencesByMethod[methodpointer] )
		if len(self.methodsList) > 0:
			s += '\n\tmethods:\n'
			s += '\n'.join( '\t\t' + methodpointer for methodpointer in self.methodsList )
		if len(self.fieldsList) > 0:
			s += '\n\tfields:\n'
			s += '\n'.join( '\t\t' + field for field in self.fieldsList )

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
			elif arg == '--constants_by_method' or arg == '-cm':
				opts['constants_by_method'] = True
			elif arg == '--classes' or arg == '-c':
				opts['classes'] = True
			elif arg == '--methods' or arg == '-m':
				opts['methods'] = True
			elif arg == '--fields' or arg == '-f':
				opts['fields'] = True
			else:
				cf = classfile.openFile(arg)
				cf.linkClassFile()
				cf.inlineClassFile()
				cf.linkBytecode()

				chart = JavaClassChart(cf, **opts)
				print (chart)
			i += 1




if __name__ == '__main__':
	main(*sys.argv[1:])
