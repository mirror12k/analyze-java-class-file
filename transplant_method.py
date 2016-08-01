#!/usr/bin/env python3



import sys

import classfile
import classbytecode
from java_code_tools import *




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



def main(args):
	file = classfile.openFile(args[0])
	file.linkClassFile()
	file.inlineClassFile()
	file.linkBytecode()

	print("dropping constants")
	dropConstants(file)

	file.unlinkBytecode()
	file.uninlineClassFile()
	file.unlinkClassFile()
	file.toFile()


	# donorClass = classfile.openFile(args[0])
	# donorClass.linkClassFile()
	# donorClass.inlineClassFile()
	# recipientClass = classfile.openFile(args[1])
	# recipientClass.linkClassFile()
	# recipientClass.inlineClassFile()

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
	main(sys.argv[1:])
