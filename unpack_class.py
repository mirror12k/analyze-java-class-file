#!/usr/bin/env python3



import sys
import classfile
from java_code_tools import *
import pprint



def main(*args):
	if len(args) == 0:
		print("file argument required")

	analyze_level = 3
	i = 0
	while i < len(args):
		arg = args[i]
		if arg == '--level':
			# set unpacking level
			# level 1 only unpacks the file
			# level 2 also links constants together, can die if constants are linked incorrectly
			# level 3 also inlines values to produce cleaner output
			i += 1
			level_arg = args[i]
			if level_arg == 'unpack':
				analyze_level = 1
			elif level_arg == 'link':
				analyze_level = 2
			elif level_arg == 'inline':
				analyze_level = 3
			else:
				analyze_level = int(level_arg)
		else:
			# process the file
			file = classfile.openFile(arg)

			if analyze_level >= 2:
				file.linkClassFile()
			if analyze_level >= 3:
				file.inlineClassFile()
				file.linkBytecode()

			# output data
			# pprint.pprint(file.fileStructure)

			print ("class identifier:")
			print("\t file.this_class = " + str(file.this_class))
			print("\t file.super_class = " + str(file.super_class))
			print("\t file.access_flags = " + str(file.access_flags))

			print ("class interfaces:")
			for interface in file.interfaces:
				print ("\t" + str(interface))
			print ("class constants:")
			for i in range(len(file.constants)):
				print ("\t" + str(i+1) + ' : ' + str(file.constants[i]))
			print ("class fields:")
			for field in file.fields:
				print ("\t" + str(field))
			print ("class methods:")
			for method in file.methods:
				print (indentCode(str(method)))
				if method.codeStructure is not None and 'stackmap' in method.codeStructure:
					pprint.pprint(method.codeStructure['stackmap'])
			print ("class attributes:")
			for attr in file.attributes:
				print ("\t", attr)

			# repackage the file
			if analyze_level >= 3:
				file.unlinkBytecode()
				file.uninlineClassFile()
			if analyze_level >= 2:
				file.unlinkClassFile()

			file.toFile()

		i += 1


		# c = classfile.createConstant('CONSTANT_Class', 'java/lang/System')
		# if c in file.constants:
		# 	print ("present!")

		# for const in file.fileStructure['constants']:
		# 	if const.tagName == 'CONSTANT_Utf8' and const.string == 'helloworld!':
		# 		print ("found my const: ", const)
		# 		const.string = 'game over! try again next time!'
		# 		print("changed it to ", const)




if __name__ == '__main__':
	main(*sys.argv[1:])
