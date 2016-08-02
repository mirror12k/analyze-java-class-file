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

# accepts two [inlined] classfiles and a method and safely appends the method to the recipient class
def transplantMethod(method, donorClass, recipientClass):

	# decompile the method bytecode and link it to 
	bc = classbytecode.ClassBytecode()
	bc.decompile(method.codeStructure['code'])
	bc.linkAssembly(donorClass)

	# uninline the assembly to ensure that the constants are present in the new
	bc.uninlineAssembly(recipientClass)
	# relink and recompile the bytecode to the method
	bc.unlinkAssembly(recipientClass)
	bc.compile()
	method.codeStructure['code'] = bc.bytecode

	# append it to the recipient
	recipientClass.methods.append(method)



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
			if 'ACC_ABSTRACT' not in method.accessFlags:
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

	else:
		raise Exception('unknown command: '+command)


	printinfo('done!')

	# # if recipientClass.this_class != donorClass.this_class:
	# # 	print ("incorrect this_class:", stringConstantSimple(recipientClass.this_class), ' vs ',
	# # 			stringConstantSimple(donorClass.this_class))

	# # if recipientClass.super_class != donorClass.super_class:
	# # 	print ("incorrect super_class:", stringConstantSimple(recipientClass.super_class), ' vs ',
	# # 			stringConstantSimple(donorClass.super_class))

	# # for const in donorClass.constants:
	# # 	if const not in recipientClass.constants:
	# # 		print("transplanting constant:", const)
	# # 		recipientClass.constants.append(const)

	# for method in donorClass.methods:
	# 	if 'ACC_ABSTRACT' not in method.accessFlags and method.nameIndex.string != '<init>':
	# 		print ("transplanting method", stringConstantSimple(method.nameIndex))
	# 		transplantMethod(method, donorClass, recipientClass)
			


	# # c = classfile.createConstant('CONSTANT_Utf8', 'this is another injected constant!')

	# # recipientClass.constants.append(c)

	# recipientClass.uninlineClassFile()
	# recipientClass.unlinkClassFile()
	# recipientClass.toFile()


if __name__ == '__main__':
	main(*sys.argv[1:])
