#!/usr/bin/env python3



import sys
import classfile



def main():
	if len(sys.argv) < 2:
		print("argument required")
	else:
		file = classfile.openFile(sys.argv[1])
		print(file.header)


if __name__ == '__main__':
	main()
