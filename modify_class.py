#!/usr/bin/env python3



import sys

import classfile
import classloader
import classbytecode
from java_code_tools import *


def printinfo(*args):
	print('[*]', *args)

def printaction(*args):
	print('[+]', *args)

def printwarning(*args):
	print('[-]', *args)

def printerror(*args):
	print('[!]', *args)

def printprompt(*args):
	print('[?]', *args)



def dropConstants(file):
	file.constants = []

def hookMethodTrace(file, method):
	methodname = method.name
	method.name = methodname + '__traced'

	argtypes, rettype = methodDescriptorToCode(method.descriptor)
	code = ['getstatic', classfile.createConstant('CONSTANT_Fieldref', 'java/lang/System', 'out', 'Ljava/io/PrintStream;'),\
				'ldc', classfile.createConstant('CONSTANT_String', 'trace -> ' + classNameToCode(file.this_class) + '.' + methodname +' (' + ', '.join(argtypes) + ')'),\
				'invokevirtual', classfile.createConstant('CONSTANT_Methodref', 'java/io/PrintStream', 'println', '(Ljava/lang/String;)V')] +\
			['aload_0'] + [ typeToBytecodeType(argtypes[i]) + 'load_' + str(i+1) for i in range(len(argtypes)) ] +\
			['invokevirtual', classfile.createConstant('CONSTANT_Methodref', file.this_class, method.name, method.descriptor)] +\
			['getstatic', classfile.createConstant('CONSTANT_Fieldref', 'java/lang/System', 'out', 'Ljava/io/PrintStream;'),\
				'ldc', classfile.createConstant('CONSTANT_String', 'trace <- ' + classNameToCode(file.this_class) + '.' + methodname +' (' + ', '.join(argtypes) + ')'),\
				'invokevirtual', classfile.createConstant('CONSTANT_Methodref', 'java/io/PrintStream', 'println', '(Ljava/lang/String;)V')] +\
			[typeToBytecodeType(rettype) + 'return']
	
	codeStructure = {}
	codeStructure['code'] = code
	if 1 + len(argtypes) < 3:
		codeStructure['max_stack'] = 3
	else:
		codeStructure['max_stack'] = 1 + len(argtypes)
	codeStructure['max_locals'] = 1 + len(argtypes)
	codeStructure['exception_table'] = []
	codeStructure['attributes'] = []

	attributes = []
	if method.exceptionsThrown is not None:
		attributes.append(classfile.createAttribute('Exceptions', list(method.exceptionsThrown)))
	attributes.append(classfile.createAttribute('Code'))

	newmethod = classfile.ClassFileMethod(list(method.accessFlags), -1, -1, attributes)
	newmethod.codeStructure = codeStructure

	newmethod.name = methodname
	newmethod.descriptor = method.descriptor

	file.methods.append(newmethod)

def hookStaticMethodTrace(file, method):
	methodname = method.name
	method.name = methodname + '__traced'

	argtypes, rettype = methodDescriptorToCode(method.descriptor)
	code = ['getstatic', classfile.createConstant('CONSTANT_Fieldref', 'java/lang/System', 'out', 'Ljava/io/PrintStream;'),\
				'ldc', classfile.createConstant('CONSTANT_String', 'trace -> ' + methodname +' (' + ', '.join(argtypes) + ')'),\
				'invokevirtual', classfile.createConstant('CONSTANT_Methodref', 'java/io/PrintStream', 'println', '(Ljava/lang/String;)V')] +\
			[ typeToBytecodeType(argtypes[i]) + 'load_' + str(i) for i in range(len(argtypes)) ] +\
			['invokestatic', classfile.createConstant('CONSTANT_Methodref', file.this_class, method.name, method.descriptor)] +\
			['getstatic', classfile.createConstant('CONSTANT_Fieldref', 'java/lang/System', 'out', 'Ljava/io/PrintStream;'),\
				'ldc', classfile.createConstant('CONSTANT_String', 'trace <- ' + methodname +' (' + ', '.join(argtypes) + ')'),\
				'invokevirtual', classfile.createConstant('CONSTANT_Methodref', 'java/io/PrintStream', 'println', '(Ljava/lang/String;)V')] +\
			[typeToBytecodeType(rettype) + 'return']
	
	codeStructure = {}
	codeStructure['code'] = code
	if 1 + len(argtypes) < 3:
		codeStructure['max_stack'] = 3
	else:
		codeStructure['max_stack'] = 1 + len(argtypes)
	codeStructure['max_locals'] = 1 + len(argtypes)
	codeStructure['exception_table'] = []
	codeStructure['attributes'] = []

	attributes = []
	if method.exceptionsThrown is not None:
		attributes.append(classfile.createAttribute('Exceptions', list(method.exceptionsThrown)))
	attributes.append(classfile.createAttribute('Code'))

	newmethod = classfile.ClassFileMethod(list(method.accessFlags), -1, -1, attributes)
	newmethod.codeStructure = codeStructure

	newmethod.name = methodname
	newmethod.descriptor = method.descriptor

	file.methods.append(newmethod)






def main(*args):
	loader = classloader.ClassFileLoader()

	command = args[0]
	args = args[1:]
	while command == '-cl':
		if command == '-cl':
			loader.setFilepath(args[0])
			command = args[1]
			args = args[2:]

	if command is None:
		printerror("command required")
	elif command == 'drop_constants':
		if len(args) < 1:
			raise Exception('usage: drop_constants <class filepath>')

		printinfo('dropping constants from class file '+args[0])
		printaction('unpacking file')
		file = loader.loadClass(args[0])
		file.linkBytecode()

		printaction('dropping constants')
		dropConstants(file)

		printaction('packing file')
		file.unlinkBytecode()
		loader.storeClass(file)

	elif command == 'rename_method':
		if len(args) < 3:
			raise Exception('usage: rename_method <class filepath> <method name> <new method name> [method descriptor]')
		elif len(args) == 3:
			filepath, methodname, newmethodname = args
			methoddescriptor = None
		else:
			filepath, methodname, newmethodname, methoddescriptor = args


		printinfo('renaming method(s) '+ methodname + ' to ' + newmethodname + ' in ' + filepath)
		printaction('unpacking file')
		file = loader.loadClass(filepath)
		file.linkBytecode()

		printinfo('searching for methods')
		renamedmethods = file.getMethodsByName(methodname, methoddescriptor)
		if len(renamedmethods) == 0:
			raise Exception('no matching methods found!')

		printaction('renaming methods')
		for method in renamedmethods:
			if not method.isAbstract():
				printaction ("renaming method: " + method.name + " " + method.descriptor)
				method.name = newmethodname

		printaction('packing file')
		file.unlinkBytecode()
		loader.storeClass(file)

	elif command == 'transplant_method':
		if len(args) < 3:
			raise Exception('usage: transplant_method <recipient filepath> <donor filepath> <method name> [method descriptor]')
		elif len(args) == 3:
			recipientFilepath, donorFilepath, methodname = args
			methoddescriptor = None
		else:
			recipientFilepath, donorFilepath, methodname, methoddescriptor = args

		printinfo('transplanting method(s) '+ methodname + ' from ' + donorFilepath + ' to ' + recipientFilepath)

		printaction('unpacking recipient class')
		recipientClass = loader.loadClass(recipientFilepath)
		recipientClass.linkBytecode()

		printaction('unpacking donor class')
		donorClass = loader.loadClass(donorFilepath)
		donorClass.linkBytecode()

		printinfo('checking for saftey')
		checkedMethods = recipientClass.getMethodsByName(methodname, methoddescriptor)
		if len(checkedMethods) != 0:
			raise Exception('recipient class already has method(s) matching the arguments!')

		printinfo('searching for methods')
		transplantedMethods = donorClass.getMethodsByName(methodname, methoddescriptor)
		if len(transplantedMethods) == 0:
			raise Exception('no matching methods found!')

		printaction('transplanting methods')
		for method in transplantedMethods:
			if 'ACC_ABSTRACT' not in method.accessFlags:
				printaction ("transplanting method: " + method.name + " " + method.descriptor)
				recipientClass.methods.append(method)

		printaction('packing recipient class')
		recipientClass.unlinkBytecode()
		loader.storeClass(recipientClass)

	elif command == 'hook_method':
		if len(args) < 3:
			raise Exception('usage: hook_method <recipient filepath> <donor filepath> <method name> [method descriptor]')
		elif len(args) == 3:
			recipientFilepath, donorFilepath, methodname = args
			methoddescriptor = None
		else:
			recipientFilepath, donorFilepath, methodname, methoddescriptor = args

		printinfo('hooking method(s) '+ methodname + ' from ' + donorFilepath + ' to ' + recipientFilepath)

		printaction('unpacking recipient class')
		recipientClass = loader.loadClass(recipientFilepath)
		recipientClass.linkBytecode()

		printaction('unpacking donor class')
		donorClass = loader.loadClass(donorFilepath)
		donorClass.linkBytecode()

		printinfo('searching for method(s)')
		hookedMethods = donorClass.getMethodsByName(methodname, methoddescriptor)
		if len(hookedMethods) == 0:
			raise Exception('donor class has no method(s) matching the arguments!')

		printinfo('hooking method(s)')
		for method in hookedMethods:
			targetMethods = recipientClass.getMethodsByName(method.name, method.descriptor)
			if len(targetMethods) == 0:
				printwarning('method target [' + method.name + ' ' + method.descriptor + '] missing, skipping')
			else:
				for target in targetMethods:
					printinfo('renaming hooked method [' + target.name + ' ' + target.descriptor + ']')
					target.name += '__hooked'

				printaction('transplanting hook method [' + method.name + ' ' + method.descriptor + '] to recipient class')
				recipientClass.methods.append(method)



		printaction('packing recipient class')
		recipientClass.unlinkBytecode()
		loader.storeClass(recipientClass)

	elif command == 'trace_method':
		if len(args) < 2:
			raise Exception('usage: trace_method <classpath> <method name> [method descriptor]')
		elif len(args) == 2:
			classpath, methodname = args
			methoddescriptor = None
		else:
			classpath, methodname, methoddescriptor = args

		printinfo('tracing method(s) '+ methodname + ' from ' + classpath)

		printaction('unpacking recipient class')
		recipientClass = loader.loadClass(classpath)
		recipientClass.linkBytecode()

		printinfo('searching for method(s)')
		if methodname != '*':
			hookedMethods = recipientClass.getMethodsByName(methodname, methoddescriptor)
		else:
			hookedMethods = recipientClass.getMethodsByName(None, methoddescriptor)
		if len(hookedMethods) == 0:
			raise Exception('class has no method(s) matching the arguments!')
		
		printinfo('hooking method(s)')
		for method in hookedMethods:
			if (not method.isAbstract()) and (not method.isSpecial()):
				printaction('tracing method [' + method.name + ' ' + method.descriptor + '] in recipient class')
				if method.isStatic():
					hookStaticMethodTrace(recipientClass, method)
				else:
					hookMethodTrace(recipientClass, method)
			else:
				printwarning('skipping method [' + method.name + ' ' + method.descriptor + ']')

		

		printaction('packing recipient class')
		recipientClass.unlinkBytecode()
		loader.storeClass(recipientClass)

	else:
		raise Exception('unknown command: '+command)


	printinfo('done!')


if __name__ == '__main__':
	main(*sys.argv[1:])
