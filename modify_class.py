#!/usr/bin/env python3



import sys

import classfile
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
				'ldc', classfile.createConstant('CONSTANT_String', 'trace enter ' + methodname +' (' + ', '.join(argtypes) + ')'),\
				'invokevirtual', classfile.createConstant('CONSTANT_Methodref', 'java/io/PrintStream', 'println', '(Ljava/lang/String;)V')] +\
			['aload_0'] + [ typeToBytecodeType(argtypes[i]) + 'load_' + str(i+1) for i in range(len(argtypes)) ] +\
			['invokevirtual', classfile.createConstant('CONSTANT_Methodref', file.this_class, method.name, method.descriptor)] +\
			['getstatic', classfile.createConstant('CONSTANT_Fieldref', 'java/lang/System', 'out', 'Ljava/io/PrintStream;'),\
				'ldc', classfile.createConstant('CONSTANT_String', 'trace exit ' + methodname +' (' + ', '.join(argtypes) + ')'),\
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
		attr = classfile.ClassFileAttribute(-1, list(method.exceptionsThrown))
		attr.name = 'Exceptions'
		attr.inlined = True
		attributes.append(attr)
	codeAttr = classfile.ClassFileAttribute(-1, None)
	codeAttr.name = 'Code'
	attributes.append(codeAttr)

	newmethod = classfile.ClassFileMethod(list(method.accessFlags), -1, -1, attributes)
	newmethod.codeStructure = codeStructure

	newmethod.name = methodname
	newmethod.descriptor = method.descriptor

	file.methods.append(newmethod)






def main(command=None, *args):
	if command is None:
		printerror("command required")
	elif command == 'drop_constants':
		if len(args) < 1:
			raise Exception('usage: drop_constants <class filepath>')

		printinfo('dropping constants from class file '+args[0])
		printaction('unpacking file')
		file = classfile.openFile(args[0])
		file.linkClassFile()
		file.inlineClassFile()
		file.linkBytecode()

		printaction('dropping constants')
		dropConstants(file)

		printaction('packing file')
		file.unlinkBytecode()
		file.uninlineClassFile()
		file.unlinkClassFile()
		file.toFile()

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
		file = classfile.openFile(filepath)
		file.linkClassFile()
		file.inlineClassFile()
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
		file.uninlineClassFile()
		file.unlinkClassFile()
		file.toFile()

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
		recipientClass = classfile.openFile(recipientFilepath)
		recipientClass.linkClassFile()
		recipientClass.inlineClassFile()
		recipientClass.linkBytecode()

		printaction('unpacking donor class')
		donorClass = classfile.openFile(donorFilepath)
		donorClass.linkClassFile()
		donorClass.inlineClassFile()
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
		recipientClass.uninlineClassFile()
		recipientClass.unlinkClassFile()
		recipientClass.toFile()

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
		recipientClass = classfile.openFile(recipientFilepath)
		recipientClass.linkClassFile()
		recipientClass.inlineClassFile()
		recipientClass.linkBytecode()

		printaction('unpacking donor class')
		donorClass = classfile.openFile(donorFilepath)
		donorClass.linkClassFile()
		donorClass.inlineClassFile()
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
		recipientClass.uninlineClassFile()
		recipientClass.unlinkClassFile()
		recipientClass.toFile()

	elif command == 'trace_method':
		if len(args) < 2:
			raise Exception('usage: trace_method <class filepath> <method name> [method descriptor]')
		elif len(args) == 2:
			classFilepath, methodname = args
			methoddescriptor = None
		else:
			classFilepath, methodname, methoddescriptor = args

		printinfo('tracing method(s) '+ methodname + ' from ' + classFilepath)

		printaction('unpacking recipient class')
		recipientClass = classfile.openFile(classFilepath)
		recipientClass.linkClassFile()
		recipientClass.inlineClassFile()
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
			if (not method.isAbstract()) and (not method.isStatic()) and (not method.isSpecial()):
				printaction('tracing method [' + method.name + ' ' + method.descriptor + '] in recipient class')
				hookMethodTrace(recipientClass, method)
		

		printaction('packing recipient class')
		recipientClass.unlinkBytecode()
		recipientClass.uninlineClassFile()
		recipientClass.unlinkClassFile()
		recipientClass.toFile()

	else:
		raise Exception('unknown command: '+command)


	printinfo('done!')


if __name__ == '__main__':
	main(*sys.argv[1:])
