#!/usr/bin/env python3


import sys


from java_code_tools import *
import classfile
import classbytecode
import classloader



class JavaClassChart(object):
	def __init__(self, classfile, **opts):
		self.classfile = classfile	

		self.classname = classfile.this_class
		self.superclassname = classfile.super_class

		self.internalClasses = set()
		self.constantReferencesByMethod = {}
		self.methodsList = set()
		self.fieldsList = set()
		self.classReferences = set()
		self.stringReferences = set()

		self.searchMethodList = set()
		self.searchClassInstantiationList = set()

		if opts.get('strings', False):
			self.stringReferences = self.parseStrings()
		if opts.get('constants_by_method', False):
			self.constantReferencesByMethod = self.parseConstantsByMethod()
		if opts.get('classes', False):
			self.classReferences = self.parseClassReferences()
		if opts.get('classes_internal', False):
			self.internalClasses = self.parseInternalClasses()
		if opts.get('methods', False):
			self.methodsList = self.parseMethods()
		if opts.get('fields', False):
			self.fieldsList = self.parseFields()
		if opts.get('search_method', None) is not None:
			self.searchMethodList = self.searchMethod(opts['search_method'])
		if opts.get('search_new', None) is not None:
			self.searchClassInstantiationList = self.searchClassInstantiation(opts['search_new'])


	def parseClassReferences(self):
		result = set()
		for const in self.classfile.constants:
			if const is not None and const.tagName == 'CONSTANT_Class':
				result.add(const.classname)
		result = sorted(result)
		return result
	def parseInternalClasses(self):
		result = set()
		for const in self.classfile.constants:
			if const is not None and const.tagName == 'CONSTANT_Class':
				if const.classname[:len(self.classfile.this_class)+1] == self.classfile.this_class + '$':
					result.add(const.classname)
		result = sorted(result)
		return result
	def parseStrings(self):
		result = set()
		for const in self.classfile.constants:
			if const is not None and const.tagName == 'CONSTANT_String':
				result.add(repr(const.string))
		result = sorted(result)
		return result
	def parseConstantsByMethod(self):
		result = {}
		for method in self.classfile.methods:
			if not method.isAbstract():
				referencedConstants = set()
				for i in range(len(method.codeStructure['code'])):
					inst = method.codeStructure['code'][i]
					if type(inst) == str and inst in classbytecode.assemblyConstantReferenceListing:
						referencedConstants.add(stringConstantSimple(method.codeStructure['code'][i+1]))

				referencedConstants = sorted(referencedConstants)

				methodpointer = methodToMethodDescription(method)
				result[methodpointer] = referencedConstants
		return result

	def parseMethods(self):
		result = set()
		for method in self.classfile.methods:
			result.add(methodToMethodDescription(method))
		result = sorted(result)
		return result
	def parseFields(self):
		result = set()
		for field in self.classfile.fields:
			result.add(fieldToFieldDescription(field))
		result = sorted(result)
		return result
	def searchMethod(self, method):
		result = set()
		if method.rfind('.') == -1:
			classSearch = None
			methodSearch = method
		else:
			classSearch = method[:method.rfind('.')]
			methodSearch = method[method.rfind('.')+1:]

		for const in self.classfile.constants:
			if const is not None:
				if const.tagName == 'CONSTANT_Methodref' or const.tagName == 'CONSTANT_Fieldref' or const.tagName == 'CONSTANT_InterfaceMethodref':
					if const.methodname == methodSearch:
						if classSearch is None or classNameToCode(const.classname) == classSearch:
							result.add(stringConstantSimple(const))
		result = sorted(result)
		return result
	def searchClassInstantiation(self, classname):
		return self.searchMethod(classname + '.<init>')



	def hasSomething(self):
		''' returns true only if it has at least one parsed-item. allows easy filtering of irrelavent classes '''
		if len(self.classReferences) > 0:
			return True
		elif len(self.internalClasses) > 0:
			return True
		elif len(self.fieldsList) > 0:
			return True
		elif len(self.methodsList) > 0:
			return True
		elif len(self.constantReferencesByMethod) > 0:
			return True
		elif len(self.stringReferences) > 0:
			return True
		elif len(self.searchMethodList) > 0:
			return True
		elif len(self.searchClassInstantiationList) > 0:
			return True
		else:
			return False

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
		if len(self.internalClasses) > 0:
			s += '\n\tinternal classes:\n'
			s += '\n'.join( '\t\t' + classNameToCode(classname) for classname in self.internalClasses )
		if len(self.fieldsList) > 0:
			s += '\n\tfields:\n'
			s += '\n'.join( '\t\t' + field for field in self.fieldsList )
		if len(self.methodsList) > 0:
			s += '\n\tmethods:\n'
			s += '\n'.join( '\t\t' + methodpointer for methodpointer in self.methodsList )
		if len(self.constantReferencesByMethod) > 0:
			s += '\n\tconstants by method:\n'
			for methodpointer in self.constantReferencesByMethod:
				s += '\n\t\t' + methodpointer + ':\n'
				s += '\n'.join( '\t\t\t' + str(const) for const in self.constantReferencesByMethod[methodpointer] )
		if len(self.classReferences) > 0:
			s += '\n\tclasses referenced:\n'
			s += '\n'.join( '\t\t' + classNameToCode(classname) for classname in self.classReferences )
		if len(self.stringReferences) > 0:
			s += '\n\tstrings:\n'
			s += '\n'.join( '\t\t' + string for string in self.stringReferences )

		if len(self.searchMethodList) > 0:
			s += '\n\tmatching method references:\n'
			s += '\n'.join( '\t\t' + classNameToCode(method) for method in self.searchMethodList )
		if len(self.searchClassInstantiationList) > 0:
			s += '\n\tinstantiates class:\n'
			s += '\n'.join( '\t\t' + classNameToCode(method) for method in self.searchClassInstantiationList )

		return s




def main(*args):
	if len(args) == 0:
		print("argument required")
	else:
		loader = classloader.ClassFileLoader()
		opts = {
			'filter_empty' : False,
		}
		i = 0
		while i < len(args):
			arg = args[i]
			if arg == '--help' or arg == '-h':
				# displays help
				print('''
				lists general collected information about any given class files
				options as to what to search:
					-a --all : enables the following: --methods, --fields, --classes, and --strings
					-m --methods : displays all methods declared in the class
					-f --fields : displays all fields declared in the class
					-c --classes : displays all classes referenced in constants
					-s --strings : displays string references in the class (not utf8 constants, specifically string constants)
					-ci --classes_internal : displays all internal classes declared inside this class (uses constants, doesn't search files)
					-cm --constants_by_method : displays constants loaded by various methods
					-sm --search_method <[method class .] method name> : displays references to a specic method
					-new --search_new <class name> : displays references to instantiations of a specific class (looks for references to their "<init>" methods)
					-E --filter_empty : skips classes which haven't found any items requested in the search (useful with search options)
				''')
			elif arg == '--all' or arg == '-a':
				# enables the following: --methods, --fields, --classes, and --strings
				opts['methods'] = True
				opts['fields'] = True
				opts['classes'] = True
				opts['strings'] = True
				
			elif arg == '--methods' or arg == '-m':
				# displays all methods declared in the class
				opts['methods'] = True
			elif arg == '--fields' or arg == '-f':
				# displays all fields declared in the class
				opts['fields'] = True
			elif arg == '--classes' or arg == '-c':
				# displays all classes referenced in the constants
				opts['classes'] = True
			elif arg == '--strings' or arg == '-s':
				# displays string references in the class (not utf8 constants, specifically string constants)
				opts['strings'] = True
			elif arg == '--classes_internal' or arg == '-ci':
				# displays all internal classes declared inside this class (uses constants, doesn't search files)
				opts['classes_internal'] = True
			elif arg == '--constants_by_method' or arg == '-cm':
				# displays constants loaded by various methods
				opts['constants_by_method'] = True

			elif arg == '--search_method' or arg == '-sm':
				# displays references to a specic method
				opts['search_method'] = args[i+1]
				i += 1
			elif arg == '--search_new' or arg == '-new':
				# displays references to instantiations of a specific class (looks for references to their "<init>" methods)
				opts['search_new'] = args[i+1]
				i += 1
			elif arg == '--filter_empty' or arg == '-E':
				# skips classes which haven't found any items requested in the search
				opts['filter_empty'] = True
			elif arg == '--class_loader' or arg == '-cl':
				loader.setFilepath(args[i+1])
				i += 1
			else:
				cf = loader.loadClass(arg)
				cf.linkBytecode()
				chart = JavaClassChart(cf, **opts)
				if opts['filter_empty'] == False or chart.hasSomething():
					print (chart)
			i += 1




if __name__ == '__main__':
	main(*sys.argv[1:])
