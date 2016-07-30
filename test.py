#!/usr/bin/env python3



import sys
import classfile
import pprint



def main():
	if len(sys.argv) < 2:
		print("argument required")
	else:
		file = classfile.openFile(sys.argv[1])


		# pprint.pprint(file.fileStructure)
		print ("class constants:")
		for const in file.constants:
			print ("\t", const)
		print ("class fields:")
		for field in file.fields:
			print ("\t", field)
		print ("class methods:")
		for method in file.methods:
			print ("\t", method)
			if 'stackmap' in method.codeStructure:
				pprint.pprint(method.codeStructure['stackmap'])
		print ("class attributes:")
		for attr in file.attributes:
			print ("\t", attr)

		c = classfile.createConstant('CONSTANT_Class', 'java/lang/System')
		if c in file.constants:
			print ("present!")



		# for const in file.fileStructure['constants']:
		# 	if const.tagName == 'CONSTANT_Utf8' and const.string == 'helloworld!':
		# 		print ("found my const: ", const)
		# 		const.string = 'game over! try again next time!'
		# 		print("changed it to ", const)

		file.packClassFile()


if __name__ == '__main__':
	main()
