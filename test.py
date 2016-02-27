#!/usr/bin/env python3



import sys
import classfile
import pprint



def main():
	if len(sys.argv) < 2:
		print("argument required")
	else:
		file = classfile.openFile(sys.argv[1])
		pprint.pprint(file.fileStructure)
		print ("class constants:")
		for const in file.fileStructure['constants']:
			print (const)
		print ("class fields:")
		for field in file.fileStructure['fields']:
			print (field)
		print ("class methods:")
		for method in file.fileStructure['methods']:
			print (method)
		print ("class attributes:")
		for attr in file.fileStructure['attributes']:
			print (attr)

		for const in file.fileStructure['constants']:
			if const.tagName == 'CONSTANT_Utf8' and const.string == 'helloworld!':
				print ("found my const: ", const)
				const.string = 'gameover!'
				print("changed it to ", const)

		file.packClassFile()


if __name__ == '__main__':
	main()
