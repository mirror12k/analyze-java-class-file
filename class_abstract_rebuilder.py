#!/usr/bin/env python3


import sys


from java_code_tools import *
import classfile
import classbytecode




class AbstractClassRebuilder(object):
	def __init__(self, filepath, opts={}):
		self.file = classfile.openFile(filepath)
		self.file.linkClassFile()
		self.file.inlineClassFile()
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
		}

	# converts the given class file to a rough java code string
	def stringClass(self):
		text = ''

		if classNameToPackageCode(self.file.this_class) is not None:
			text += 'package ' + classNameToPackageCode(self.file.this_class) + ';\n'

		if self.opts['render_abstract']:
			if 'ACC_ABSTRACT' not in self.file.access_flags:
				text += 'abstract '

		text += classAccessFlagsToCode(self.file.access_flags) + ' class ' + classNameToSimpleNameCode(self.file.this_class)
		if classNameToCode(self.file.super_class) != 'java.lang.Object':
			text += ' extends ' + classNameToCode(self.file.super_class)
		text += ' {\n'


		if len(self.file.fields) > 0:
			text += '\t// fields\n'

		for field in self.file.fields:
			text += '\t' + self.stringField(field) + '\n'
			
		if len(self.file.fields) > 0:
			text += '\n'


		if len(self.file.methods) > 0:
			text += '\t// methods\n'

		for method in self.file.methods:
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
			elif 'ACC_ABSTRACT' not in method.accessFlags:
				text += 'abstract '


		if methodname == '<clinit>':
			text += methodAccessFlagsToCode(method.accessFlags)
		else:
			if methodname == '<init>':
				methodname = classNameToSimpleNameCode(self.file.this_class)

			text += methodAccessFlagsToCode(method.accessFlags) + ' ' + rettype + ' ' + methodname +\
					' (' + ', '.join([ argtypes[i]+' arg'+str(i) for i in range(len(argtypes)) ]) + ')'

		if 'exceptions_thrown' in method.codeStructure:
			text += ' throws ' + ', '.join( classNameToCode(exceptionClass) for exceptionClass in method.codeStructure['exceptions_thrown'])

		if self.opts['render_abstract'] or self.opts['list_class']:
			text += ';'
		else:
			text += ' {\n'
			if self.opts['decompile_bytecode']:
				bc = classbytecode.ClassBytecode(
					resolveConstants=not self.opts['link_bytecode'], classfile=self.file, exceptionTable=method.codeStructure['exception_table']
				)
				bc.decompile(method.codeStructure['code'])
				if self.opts['link_bytecode']:
					bc.linkAssembly(self.file)

				if self.opts['filter_critical']:
					assemblyFilter = classbytecode.assemblyCriticalInstructionsListing
				else:
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
		opts = {}
		for arg in args:
			if arg == '--render_abstract' or arg == '-abs':
				opts['render_abstract'] = True
			elif arg == '--decompile_bytecode' or arg =='-db':
				opts['decompile_bytecode'] = True
			elif arg == '--link_bytecode' or arg == '-lb':
				opts['link_bytecode'] = True
			elif arg == '--list_class' or arg == '-l':
				opts['list_class'] = True
			elif arg == '--filter_critical' or arg == '-fc':
				opts['filter_critical'] = True
			else:
				rebuilder = AbstractClassRebuilder(arg, opts)
				print (rebuilder.stringClass())




if __name__ == '__main__':
	main(*sys.argv[1:])
