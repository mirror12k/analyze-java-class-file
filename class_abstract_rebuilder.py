#!/usr/bin/env python


import sys

import classfile



def classConstantToName(const):
	if const.tagName != 'CONSTANT_Class':
		raise Exception('classConstantToName called with non-class constant: ' + str(const))

	name = const.nameIndex

	if name.tagName != 'CONSTANT_Utf8':
		raise Exception('classConstantToName called with non-string classname constant: ' + str(name))

	return name.string.replace('/', '.')


def classAccessFlagsToCode(flags):
	newflags = []
	for flag in flags:
		if flag == 'ACC_PUBLIC': # Declared public; may be accessed from outside its package.
			newflags.append('public')
		elif flag == 'ACC_FINAL': # Declared final; no subclasses allowed.
			newflags.append('final')
		elif flag == 'ACC_SUPER': # Treat superclass methods specially when invoked by the invokespecial instruction.
			pass
			# newflags.append()
		elif flag == 'ACC_INTERFACE': # Is an interface, not a class.
			newflags.append('interface')
		elif flag == 'ACC_ABSTRACT': # Declared abstract; must not be instantiated.
			newflags.append('abstract')
		elif flag == 'ACC_SYNTHETIC': # Declared synthetic; not present in the source code.
			newflags.append('SYNTHETIC')
		elif flag == 'ACC_ANNOTATION': # Declared as an annotation type.
			newflags.append('ANNOTATION')
		elif flag == 'ACC_ENUM': # Declared as an enum type.
			newflags.append('enum')
		else:
			raise Exception('invalid flag for file.access_flags:'+flag)
	return ' '.join(newflags)


def main(args):
	if len(args) == 0:
		print("argument required")
	else:
		file = classfile.openFile(args[0])

		classDeclaration = classAccessFlagsToCode(file.fileStructure['access_flags']) + ' class ' + classConstantToName(file.fileStructure['this_class']) +\
				' extends ' + classConstantToName(file.fileStructure['super_class'])

		print classDeclaration + ' {'
		print '}'




if __name__ == '__main__':
	main(sys.argv[1:])
