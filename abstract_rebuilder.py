#!/usr/bin/env python3


import sys


from java_code_tools import *
import classfile
import classbytecode
import classloader




class AbstractClassRebuilder(object):
	def __init__(self, file, **opts):
		self.file = file
		self.opts = {
			# simply lists functions and fields
			'list_class' : opts.get('list_class', False),
			# attempts to output an abstract hull of the class, turning all methods to abstract (commenting out ones that can't be abstract)
			'render_abstract' : opts.get('render_abstract', False),
			# uses classbytecode module to disassemble the bytecode
			'decompile_bytecode' : opts.get('decompile_bytecode', False),
			# tells the classbytecode module to link the constants of class file when disassembling instead of displaying constant numbers
			'link_bytecode' : opts.get('link_bytecode', False),

			# tells the classbytecode module to filter assembly instructions, looking for critical instructions such as instantiation, calls, branches, throws, and returns
			'filter_critical' : opts.get('filter_critical', False),
			# filters field referencing assembly
			'filter_field_references' : opts.get('filter_field_references', False),
			# filters method referencing assembly
			'filter_method_references' : opts.get('filter_method_references', False),

			# shows jump destinations and sources using obvious symbols
			'mark_jumps' : opts.get('mark_jumps', False),

			'filter_method_name' : opts.get('filter_method_name', None),
			'filter_method_descriptor' : opts.get('filter_method_descriptor', None),
		}

	# converts the given class file to a rough java code string
	def stringClass(self):
		text = ''

		if classNameToPackageCode(self.file.this_class) is not None:
			text += 'package ' + classNameToPackageCode(self.file.this_class) + ';\n'

		if self.opts['render_abstract']:
			if 'ACC_ABSTRACT' not in self.file.access_flags:
				text += 'abstract '

		text += classAccessFlagsToCode(self.file.access_flags) + ' '+ classTypeToCode(self.file.access_flags) +\
			' ' + classNameToSimpleNameCode(self.file.this_class)
		if classNameToCode(self.file.super_class) != 'java.lang.Object':
			text += ' extends ' + classNameToCode(self.file.super_class)
		if len(self.file.interfaces) > 0:
			if classTypeToCode(self.file.access_flags) == 'class':
				text += ' implements '
			else:
				text += ' extends '
			text += ', '.join(classNameToCode(interface) for interface in self.file.interfaces)
		text += ' {\n'


		if len(self.file.fields) > 0:
			text += '\t// fields\n'

		for field in self.file.fields:
			text += '\t' + self.stringField(field) + '\n'
			
		if len(self.file.fields) > 0:
			text += '\n'


		if len(self.file.methods) > 0:
			text += '\t// methods\n'

		if self.opts['filter_method_name'] is None:
			methodlist = self.file.methods
		else:
			methodlist = self.file.getMethodsByName(self.opts['filter_method_name'], self.opts['filter_method_descriptor'])
		for method in methodlist:
			text += indentCode(self.stringMethod(method)) + '\n'

		text += '}\n'

		return text

	# converts the given class method to a rough java code method string
	def stringMethod(self, method):
		text = ''

		argtypes, rettype = methodDescriptorToCode(method.descriptorIndex.string)
		methodname = method.nameIndex.string

		# too many optional cases here, i wish i could clean this up
		if self.opts['render_abstract']:
			if 'ACC_STATIC' in method.accessFlags or methodname == '<clinit>' or methodname == '<init>':
				text += '// '
			elif not method.isAbstract():
				text += 'abstract '


		if methodname == '<clinit>':
			text += methodAccessFlagsToCode(method.accessFlags)
		elif methodname == '<init>':
			# methodname = classNameToSimpleNameCode(self.file.this_class)
			text += methodAccessFlagsToCode(method.accessFlags) + ' ' + classNameToSimpleNameCode(self.file.this_class) +\
					' (' + ', '.join([ argtypes[i]+' arg'+str(i) for i in range(len(argtypes)) ]) + ')'
		else:
			text += methodAccessFlagsToCode(method.accessFlags) + ' ' + rettype + ' ' + methodname +\
					' (' + ', '.join([ argtypes[i]+' arg'+str(i) for i in range(len(argtypes)) ]) + ')'

		# if not method.isAbstract():
		if method.exceptionsThrown is not None:
			text += ' throws ' + ', '.join( classNameToCode(exceptionClass) for exceptionClass in method.exceptionsThrown)

		if self.opts['render_abstract'] or self.opts['list_class'] or method.isAbstract():
			text += ';'
		else:
			text += ' {\n'
			if self.opts['decompile_bytecode']:
				bc = classbytecode.ClassBytecode(
					resolveConstants=not self.opts['link_bytecode'], classfile=self.file, exceptionTable=method.codeStructure['exception_table'],
					markJumpDestinations=self.opts['mark_jumps'], markJumpSources=self.opts['mark_jumps'],
				)
				bc.decompile(method.codeStructure['code'])
				if self.opts['link_bytecode']:
					bc.linkAssembly(self.file)

				assemblyFilter = []
				if self.opts['filter_critical']:
					assemblyFilter += classbytecode.assemblyCriticalInstructionsListing
				if self.opts['filter_field_references']:
					assemblyFilter += classbytecode.assemblyFieldReferencingListing
				if self.opts['filter_method_references']:
					assemblyFilter += classbytecode.assemblyMethodReferencingListing
				
				if len(assemblyFilter) == 0:
					assemblyFilter = None

				text += indentCode(bc.stringAssembly(assemblyFilterList=assemblyFilter)) + '\n'
			else:
				text += '\t// code ...\n'
			text += '}'

		return text

	# converts the given class field to a rough java code field string
	def stringField(self, field):
		name = field.nameIndex.string
		typestr = typeToCode(field.descriptorIndex.string)
		return fieldAccessFlagsToCode(field.accessFlags) + ' ' + typestr + ' ' + name + ';'




def main(*args):
	if len(args) == 0:
		print("argument required")
	else:
		loader = classloader.ClassFileLoader()
		opts = {}
		i = 0
		while i < len(args):
			arg = args[i]
			if arg == '--render_abstract' or arg == '-abs':
				opts['render_abstract'] = True
			elif arg == '--list_class' or arg == '-l':
				opts['list_class'] = True

			elif arg == '--decompile_bytecode' or arg =='-db':
				opts['decompile_bytecode'] = True
			elif arg == '--link_bytecode' or arg == '-lb':
				opts['link_bytecode'] = True
			elif arg == '--mark_jumps' or arg == '-mj':
				opts['mark_jumps'] = True

			elif arg == '--filter_field_references' or arg == '-ff':
				opts['filter_field_references'] = True
			elif arg == '--filter_method_references' or arg == '-fm':
				opts['filter_method_references'] = True
			elif arg == '--filter_critical' or arg == '-fc':
				opts['filter_critical'] = True

			elif arg == '--filter_method_name' or arg == '-mn':
				opts['filter_method_name'] = args[i+1]
				i += 1
			elif arg == '--filter_method_descriptor' or arg == '-md':
				opts['filter_method_descriptor'] = args[i+1]
				i += 1
			elif arg == '--class_loader' or arg == '-cl':
				loader.setFilepath(args[i+1])
				i += 1
			else:
				cf = loader.loadClass(arg)
				rebuilder = AbstractClassRebuilder(cf, **opts)
				print (rebuilder.stringClass())
			i += 1




if __name__ == '__main__':
	main(*sys.argv[1:])
