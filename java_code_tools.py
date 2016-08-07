




# converts a constant to a simple to understand string describing it
# different from the output of str(const)
def stringConstantSimple(const):
	if const.tagName == 'CONSTANT_Utf8':
		return 'utf8 ' + repr(const.string) + ''
	elif const.tagName == 'CONSTANT_Class':
		return 'class ' + classConstantToName(const)
	elif const.tagName == 'CONSTANT_String':
		return 'string ' + repr(const.stringIndex.string) + ''
	elif const.tagName == 'CONSTANT_InterfaceMethodref':
		argtypes, rettype = methodDescriptorToCode(const.nameAndTypeIndex.descriptorIndex.string)
		return 'interface method ' + rettype + ' ' + classConstantToName(const.classIndex) +\
				'.' + const.nameAndTypeIndex.nameIndex.string + ' (' + ', '.join(argtypes) + ')'
	elif const.tagName == 'CONSTANT_Methodref':
		argtypes, rettype = methodDescriptorToCode(const.nameAndTypeIndex.descriptorIndex.string)
		return 'method ' + rettype + ' ' + classConstantToName(const.classIndex) + '.' + const.nameAndTypeIndex.nameIndex.string + ' (' + ', '.join(argtypes) + ')'
	elif const.tagName == 'CONSTANT_Fieldref':
		return 'field ' + typeToCode(const.nameAndTypeIndex.descriptorIndex.string) + ' ' +\
				classConstantToName(const.classIndex) + '.' + const.nameAndTypeIndex.nameIndex.string
	elif const.tagName == 'CONSTANT_Integer':
		return 'Integer ' + str(const.value)
	elif const.tagName == 'CONSTANT_Float':
		return 'Float ' + str(const.value) + 'F'
	elif const.tagName == 'CONSTANT_Long':
		return 'Long ' + str(const.value) + 'L'
	elif const.tagName == 'CONSTANT_Double':
		return 'Double ' + str(const.value) + 'D'
		# elif self.tagName == 'CONSTANT_Integer' or self.tagName == 'CONSTANT_Float'\
		# 	or self.tagName == 'CONSTANT_Long' or self.tagName == 'CONSTANT_Double':
	else:
		raise Exception("unknown constant type: " + const.tagName)



# converts a stored classname to a standard java class name
def classNameToCode(classname):
	return classname.replace('/', '.')

def classNameToSimpleNameCode(classname):
	code = classNameToCode(classname)
	if code.rfind('.') == -1:
		return code
	else:
		return code[code.rfind('.')+1:]

def classNameToPackageCode(classname):
	code = classNameToCode(classname)
	if code.rfind('.') == -1:
		return None
	else:
		return code[:code.rfind('.')]



# safely converts a class constant to the java class name
def classConstantToName(const):
	if const.tagName != 'CONSTANT_Class':
		raise Exception('classConstantToName called with non-class constant: ' + str(const))

	name = const.nameIndex

	if name.tagName != 'CONSTANT_Utf8':
		raise Exception('classConstantToName called with non-string classname constant: ' + str(name))

	return classNameToCode(name.string)

# safely converts a class constant to the simple java class name (excludes the package)
def classConstantToSimpleName(const):
	if const.tagName != 'CONSTANT_Class':
		raise Exception('classConstantToSimpleName called with non-class constant: ' + str(const))

	name = const.nameIndex

	if name.tagName != 'CONSTANT_Utf8':
		raise Exception('classConstantToSimpleName called with non-string classname constant: ' + str(name))

	code = classNameToCode(name.string)
	if code.rfind('.') == -1:
		return code
	else:
		return code[code.rfind('.')+1:]

# safely converts a class constant to the simple java class package (excludes the class name)
def classConstantToPackageName(const):
	if const.tagName != 'CONSTANT_Class':
		raise Exception('classConstantToPackageName called with non-class constant: ' + str(const))

	name = const.nameIndex

	if name.tagName != 'CONSTANT_Utf8':
		raise Exception('classConstantToPackageName called with non-string classname constant: ' + str(name))

	code = classNameToCode(name.string)
	if code.rfind('.') == -1:
		return None
	else:
		return code[:code.rfind('.')]


def classTypeToCode(flags):
	if 'ACC_ENUM' in flags:
		return 'enum'
	elif 'ACC_INTERFACE' in flags:
		return 'interface'
	else:
		return 'class'



def methodToMethodDescription(method):
	argtypes, rettype = methodDescriptorToCode(method.descriptor)
	throwClause = ''
	if method.exceptionsThrown is not None:
		throwClause = ' throws ' + ', '.join( classNameToCode(exceptionClass) for exceptionClass in method.exceptionsThrown )
	return  methodAccessFlagsToCode(method.accessFlags) + ' ' + rettype + ' ' + method.name + ' (' + ', '.join(argtypes) + ')' + throwClause

def fieldToFieldDescription(field):
	return fieldAccessFlagsToCode(field.accessFlags) + ' ' + typeToCode(field.descriptor) + ' ' + field.name + ';'



# converts the list of class access flags to a java code string describing the access
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
			pass # this is handled elsewhere
			# newflags.append('interface')
		elif flag == 'ACC_ABSTRACT': # Declared abstract; must not be instantiated.
			newflags.append('abstract')
		elif flag == 'ACC_SYNTHETIC': # Declared synthetic; not present in the source code.
			newflags.append('/*SYNTHETIC*/')
		elif flag == 'ACC_ANNOTATION': # Declared as an annotation type.
			newflags.append('/*ANNOTATION*/')
		elif flag == 'ACC_ENUM': # Declared as an enum type.
			pass # this is handled elsewhere
			# newflags.append('enum')
		else:
			raise Exception('invalid flag in class access flags: '+flag)
	return ' '.join(newflags)

# converts the list of field access flags to a java code string describing the access
def fieldAccessFlagsToCode(flags):
	newflags = []
	for flag in flags:
		if flag == 'ACC_PUBLIC': # Declared public; may be accessed from outside its package.
			newflags.append('public')
		elif flag == 'ACC_PRIVATE': # Declared private; usable only within the defining class.
			newflags.append('private')
		elif flag == 'ACC_PROTECTED': # Declared protected; may be accessed within subclasses.
			newflags.append('protected')
		elif flag == 'ACC_STATIC': # Declared static.
			newflags.append('static')
		elif flag == 'ACC_FINAL': # Declared final; never directly assigned to after object construction
			newflags.append('final')
		elif flag == 'ACC_VOLATILE': # Declared volatile; cannot be cached.
			newflags.append('volatile')
		elif flag == 'ACC_TRANSIENT': # Declared transient; not written or read by a persistent object manager.
			newflags.append('transient')
		elif flag == 'ACC_SYNTHETIC': # Declared synthetic; not present in the source code.
			newflags.append('/*SYNTHETIC*/')
		elif flag == 'ACC_ENUM': # Declared as an element of an enum.
			newflags.append('enum')
		else:
			raise Exception('invalid flag in method access flags: '+flag)
	return ' '.join(newflags)



# converts the list of method access flags to a java code string describing the access
def methodAccessFlagsToCode(flags):
	newflags = []
	for flag in flags:
		if flag == 'ACC_PUBLIC': # Declared public; may be accessed from outside its package.
			newflags.append('public')
		elif flag == 'ACC_PRIVATE': # Declared private; accessible only within the defining class.
			newflags.append('private')
		elif flag == 'ACC_PROTECTED': # Declared protected; may be accessed within subclasses.
			newflags.append('protected')
		elif flag == 'ACC_STATIC': # Declared static.
			newflags.append('static')
		elif flag == 'ACC_FINAL': # Declared final; must not be overridden.
			newflags.append('final')
		elif flag == 'ACC_SYNCHRONIZED': # Declared synchronized; invocation is wrapped by a monitor use.
			newflags.append('synchronized')
		elif flag == 'ACC_BRIDGE': # A bridge method, generated by the compiler.
			newflags.append('/*BRIDGE*/')
		elif flag == 'ACC_VARARGS': # Declared with variable number of arguments.
			newflags.append('/*VARARGS*/')
		elif flag == 'ACC_NATIVE': # Declared native; implemented in a language other than Java.
			newflags.append('native')
		elif flag == 'ACC_ABSTRACT': # Declared abstract; no implementation is provided.
			newflags.append('abstract')
		elif flag == 'ACC_STRICT': # Declared strictfp; floating-point mode is FP-strict.
			newflags.append('strictfp')
		elif flag == 'ACC_SYNTHETIC': # Declared synthetic; not present in the source code.
			newflags.append('/*SYNTHETIC*/')
		else:
			raise Exception('invalid flag in method access flags: '+flag)
	return ' '.join(newflags)


letterTypeToCode = {
	'V' : 'void',

	'I' : 'int',
	'J' : 'long',
	'S' : 'short',
	'B' : 'byte',
	'C' : 'char',
	'F' : 'float',
	'D' : 'double',
	'Z' : 'boolean',

	'a' : 'reference',
}

	
# converts the packed type string to a java code type
def typeToCode(typestr):
	arraydepth = 0
	while typestr[0] == '[':
		typestr = typestr[1:]
		arraydepth = arraydepth + 1

	if typestr[0] == 'L':
		return classNameToCode(typestr[1:-1]) + ('[]' * arraydepth)
	else:
		return letterTypeToCode[typestr] + ('[]' * arraydepth)

# converts the packed method descriptor string to a tuple of a list of argument types (java code format) and a return type (java code format)
def methodDescriptorToCode(desc):
	if desc[0] != '(':
		raise Exception('invalid method description: '+desc)

	offset = 1
	argtypes = []
	while desc[offset] != ')':
		startoffset = offset
		while desc[offset] == '[':
			offset = offset + 1

		if desc[offset] == 'L':
			endoffset = desc.find(';', offset) + 1
			offset = endoffset
		else:
			endoffset = offset + 1
			offset = offset + 1

		typestr = desc[startoffset:endoffset]
		argtypes.append(typeToCode(typestr))

	retstr = desc[offset+1:]
	rettype = typeToCode(retstr)

	return (argtypes, rettype)

# indents every line in  the give code text with count number of tabs
def indentCode(code, count=1):
	return '\n'.join([ '\t' * count + line for line in code.split('\n') ])


