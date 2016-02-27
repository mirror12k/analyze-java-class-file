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
		for const in file.fileStructure['constants']:
			print (const)
		for field in file.fileStructure['fields']:
			print (field)
		for method in file.fileStructure['methods']:
			print (method)
		for attr in file.fileStructure['attributes']:
			print (attr)


if __name__ == '__main__':
	main()
