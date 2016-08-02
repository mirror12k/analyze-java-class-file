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

	elif command == 'transplant_method':
		if len(args) < 3:
			raise Exception('usage: transplant_method <recipient filepath> <donor filepath> <method name>')

		recipientFilepath, donorFilepath, methodname = args

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
		checkedMethods = recipientClass.getMethodsByName(methodname)
		if len(checkedMethods) != 0:
			raise Exception('recipient class already has method(s) matching the arguments!')

		printinfo('searching for methods')
		transplantedMethods = donorClass.getMethodsByName(methodname)
		if len(transplantedMethods) == 0:
			raise Exception('no matching methods found!')

		printaction('transplanting methods')
		for method in transplantedMethods:
			if 'ACC_ABSTRACT' not in method.accessFlags and method.name == methodname:
				printaction ("transplanting method: " + method.name + " " + method.descriptor)
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
