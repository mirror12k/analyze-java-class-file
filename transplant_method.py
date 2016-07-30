#!/usr/bin/env python3



import sys

import classfile
import class_abstract_rebuilder







def main(args):
	recipientClass = classfile.openFile(args[0])
	donorClass = classfile.openFile(args[1])

	if recipientClass.fileStructure['this_class'] != donorClass.fileStructure['this_class']:
		print ("incorrect this_class:", class_abstract_rebuilder.stringConstantSimple(recipientClass.fileStructure['this_class']), ' vs ',
				class_abstract_rebuilder.stringConstantSimple(donorClass.fileStructure['this_class']))

	if recipientClass.fileStructure['super_class'] != donorClass.fileStructure['super_class']:
		print ("incorrect super_class:", class_abstract_rebuilder.stringConstantSimple(recipientClass.fileStructure['super_class']), ' vs ',
				class_abstract_rebuilder.stringConstantSimple(donorClass.fileStructure['super_class']))

	for method in donorClass.fileStructure['methods']:
		if 'ACC_ABSTRACT' not in method.accessFlags and method.nameIndex.string != '<init>':
			print ("transplanting method", class_abstract_rebuilder.stringConstantSimple(method.nameIndex))
			
			# recipientClass.fileStructure['methods'].append(method)


	c = classfile.ClassFileConstant(1)
	c.string = 'java/lang/System'

	recipientClass.fileStructure['constants'].append(c)

	# for const in donorClass.fileStructure['constants']:
	# 	if const not in recipientClass.fileStructure['constants']:
	# 		recipientClass.fileStructure['constants'].append(const)

	recipientClass.packClassFile()


if __name__ == '__main__':
	main(sys.argv[1:])
