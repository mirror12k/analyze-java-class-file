
import struct


import classbytecode



constantTagTypeToTagName = {
	1 : 'CONSTANT_Utf8',
	3 : 'CONSTANT_Integer',
	4 : 'CONSTANT_Float',
	5 : 'CONSTANT_Long',
	6 : 'CONSTANT_Double',
	7 : 'CONSTANT_Class',
	8 : 'CONSTANT_String',
	9 : 'CONSTANT_Fieldref',
	10 : 'CONSTANT_Methodref',
	11 : 'CONSTANT_InterfaceMethodref',
	12 : 'CONSTANT_NameAndType',
	15 : 'CONSTANT_MethodHandle',
	16 : 'CONSTANT_MethodType',
	18 : 'CONSTANT_InvokeDynamic',
}


constantTagNameToTagType = {
	'CONSTANT_Utf8' : 1,
	'CONSTANT_Integer' : 3,
	'CONSTANT_Float' : 4,
	'CONSTANT_Long' : 5,
	'CONSTANT_Double' : 6,
	'CONSTANT_Class' : 7,
	'CONSTANT_String' : 8,
	'CONSTANT_Fieldref' : 9,
	'CONSTANT_Methodref' : 10,
	'CONSTANT_InterfaceMethodref' : 11,
	'CONSTANT_NameAndType' : 12,
	'CONSTANT_MethodHandle' : 15,
	'CONSTANT_MethodType' : 16,
	'CONSTANT_InvokeDynamic' : 18,
}



# quick method for easily creating an inlined constant
# arguments differ based on what constant type it is
def createConstant(consttype, *args):
	const = ClassFileConstant(constantTagNameToTagType[consttype], True)

	if consttype == 'CONSTANT_Class':
		const.classname = args[0]
	elif consttype == 'CONSTANT_String':
		const.string = args[0]
	elif consttype == 'CONSTANT_Methodref' or consttype == 'CONSTANT_Fieldref' or consttype == 'CONSTANT_InterfaceMethodref':
		const.classname = args[0]
		const.methodname = args[1]
		const.methodtype = args[2]
	elif consttype == 'CONSTANT_NameAndType':
		const.name = args[0]
		const.descriptor = args[1]
	elif consttype == 'CONSTANT_Utf8':
		const.string = args[0]
	elif consttype == 'CONSTANT_Integer' or consttype == 'CONSTANT_Float' or consttype == 'CONSTANT_Long' or consttype == 'CONSTANT_Double':
		const.value = args[0]
	else:
		raise Exception ("unknown tag type: ", consttype)

	return const




# represents a class file constant
class ClassFileConstant(object):
	def __init__(self, tagType, inlined=False):
		self.tagType = tagType
		self.tagName = constantTagTypeToTagName[tagType]

		self.nameIndex = None
		self.descriptorIndex = None
		self.classIndex = None
		self.nameAndTypeIndex = None
		self.stringIndex = None
		self.value = None
		self.string = None
		self.referenceKind = None
		self.referenceIndex = None
		self.bootstrapIndex = None

		self.inlined = inlined
	def link(self, classfile):
		if self.tagName == 'CONSTANT_Class':
			self.nameIndex = classfile.constantFromIndex(self.nameIndex, 'CONSTANT_Utf8')
		elif self.tagName == 'CONSTANT_String':
			self.stringIndex = classfile.constantFromIndex(self.stringIndex, 'CONSTANT_Utf8')
		elif self.tagName == 'CONSTANT_Methodref' or self.tagName == 'CONSTANT_Fieldref' or self.tagName == 'CONSTANT_InterfaceMethodref':
			self.classIndex = classfile.constantFromIndex(self.classIndex, 'CONSTANT_Class')
			self.nameAndTypeIndex = classfile.constantFromIndex(self.nameAndTypeIndex, 'CONSTANT_NameAndType')
		elif self.tagName == 'CONSTANT_NameAndType':
			self.nameIndex = classfile.constantFromIndex(self.nameIndex, 'CONSTANT_Utf8')
			self.descriptorIndex = classfile.constantFromIndex(self.descriptorIndex, 'CONSTANT_Utf8')
		elif self.tagName == 'CONSTANT_Utf8' or self.tagName == 'CONSTANT_Integer' or self.tagName == 'CONSTANT_Float'\
			or self.tagName == 'CONSTANT_Long' or self.tagName == 'CONSTANT_Double':
			pass
		else:
			raise Exception ("unknown tag type: ", self.tagName)
	def unlink(self, classfile):
		if self.tagName == 'CONSTANT_Class':
			self.nameIndex = classfile.constantToIndex(self.nameIndex, 'CONSTANT_Utf8')
		elif self.tagName == 'CONSTANT_String':
			self.stringIndex = classfile.constantToIndex(self.stringIndex, 'CONSTANT_Utf8')
		elif self.tagName == 'CONSTANT_Methodref' or self.tagName == 'CONSTANT_Fieldref' or self.tagName == 'CONSTANT_InterfaceMethodref':
			self.classIndex = classfile.constantToIndex(self.classIndex, 'CONSTANT_Class')
			self.nameAndTypeIndex = classfile.constantToIndex(self.nameAndTypeIndex, 'CONSTANT_NameAndType')
		elif self.tagName == 'CONSTANT_NameAndType':
			self.nameIndex = classfile.constantToIndex(self.nameIndex, 'CONSTANT_Utf8')
			self.descriptorIndex = classfile.constantToIndex(self.descriptorIndex, 'CONSTANT_Utf8')
		elif self.tagName == 'CONSTANT_Utf8' or self.tagName == 'CONSTANT_Integer' or self.tagName == 'CONSTANT_Float'\
			or self.tagName == 'CONSTANT_Long' or self.tagName == 'CONSTANT_Double':
			pass
		else:
			raise Exception ("unknown tag type: ", self.tagName)

	def inline(self):
		if self.tagName == 'CONSTANT_Class':
			self.classname = self.nameIndex.string
		elif self.tagName == 'CONSTANT_String':
			self.string = self.stringIndex.string
		elif self.tagName == 'CONSTANT_Methodref' or self.tagName == 'CONSTANT_Fieldref' or self.tagName == 'CONSTANT_InterfaceMethodref':
			self.classname = self.classIndex.nameIndex.string
			self.methodname = self.nameAndTypeIndex.nameIndex.string
			self.methodtype = self.nameAndTypeIndex.descriptorIndex.string
		elif self.tagName == 'CONSTANT_NameAndType':
			self.name = self.nameIndex.string
			self.descriptor = self.descriptorIndex.string
		elif self.tagName == 'CONSTANT_Utf8' or self.tagName == 'CONSTANT_Integer' or self.tagName == 'CONSTANT_Float'\
			or self.tagName == 'CONSTANT_Long' or self.tagName == 'CONSTANT_Double':
			pass
		else:
			raise Exception ("unknown tag type: ", self.tagName)

	def uninline(self, classfile):
		if self.tagName == 'CONSTANT_Class':
			self.nameIndex = classfile.getSetInlinedConstant(createConstant('CONSTANT_Utf8', self.classname))
		elif self.tagName == 'CONSTANT_String':
			self.stringIndex = classfile.getSetInlinedConstant(createConstant('CONSTANT_Utf8', self.string))
		elif self.tagName == 'CONSTANT_Methodref' or self.tagName == 'CONSTANT_Fieldref' or self.tagName == 'CONSTANT_InterfaceMethodref':
			self.classIndex = classfile.getSetInlinedConstant(createConstant('CONSTANT_Class', self.classname))
			self.nameAndTypeIndex = classfile.getSetInlinedConstant(createConstant('CONSTANT_NameAndType', self.methodname, self.methodtype))
		elif self.tagName == 'CONSTANT_NameAndType':
			self.nameIndex = classfile.getSetInlinedConstant(createConstant('CONSTANT_Utf8', self.name))
			self.descriptorIndex = classfile.getSetInlinedConstant(createConstant('CONSTANT_Utf8', self.descriptor))
		elif self.tagName == 'CONSTANT_Utf8' or self.tagName == 'CONSTANT_Integer' or self.tagName == 'CONSTANT_Float'\
			or self.tagName == 'CONSTANT_Long' or self.tagName == 'CONSTANT_Double':
			pass
		else:
			raise Exception ("unknown tag type: ", self.tagName)
		
	def setInlined(self, inlined=True):
		self.inlined = inlined

	def __str__(self):
		if self.inlined:
			s = 'C<'+self.tagName+'>('
			if self.tagName == 'CONSTANT_Class':
				s += '"' + self.classname + '"'
			elif self.tagName == 'CONSTANT_String':
				s += '"' + self.string + '"'
			elif self.tagName == 'CONSTANT_Methodref' or self.tagName == 'CONSTANT_Fieldref' or self.tagName == 'CONSTANT_InterfaceMethodref':
				s += '"' + self.classname + '", "' + self.methodname + '", "' + self.methodtype + '"'
			elif self.tagName == 'CONSTANT_NameAndType':
				s += '"' + self.name + '", "' + self.descriptor + '"'
			elif self.tagName == 'CONSTANT_Utf8':
				s += '"' + self.string + '"'
			elif self.tagName == 'CONSTANT_Integer' or self.tagName == 'CONSTANT_Float'\
					or self.tagName == 'CONSTANT_Long' or self.tagName == 'CONSTANT_Double':
				s += str(self.value)
			else:
				raise Exception ("unknown tag type: ", self.tagName)
			s += ')'
			return s

		else:
			s = 'C<'+self.tagName+'>('
			if self.nameIndex is not None:
				s += 'nameIndex=' + str(self.nameIndex) + ','
			if self.descriptorIndex is not None:
				s += 'descriptorIndex=' + str(self.descriptorIndex) + ','
			if self.classIndex is not None:
				s += 'classIndex=' + str(self.classIndex) + ','
			if self.nameAndTypeIndex is not None:
				s += 'nameAndTypeIndex=' + str(self.nameAndTypeIndex) + ','
			if self.stringIndex is not None:
				s += 'stringIndex=' + str(self.stringIndex) + ','
			if self.value is not None:
				s += 'value=' + str(self.value) + ','
			if self.string is not None:
				s += 'string="' + str(self.string) + '",'
			if self.referenceKind is not None:
				s += 'referenceKind=' + str(self.referenceKind) + ','
			if self.referenceIndex is not None:
				s += 'referenceIndex=' + str(self.referenceIndex) + ','
			s += ')'
			return s
	def __eq__(self, other):
		if not isinstance(other, ClassFileConstant):
			return False
		else:
			if self.tagType != other.tagType:
				return False
			elif self.inlined != other.inlined:
				return False
			else:
				if self.inlined:
					if self.tagName == 'CONSTANT_Class':
						return self.classname == other.classname
					elif self.tagName == 'CONSTANT_String':
						return self.string == other.string
					elif self.tagName == 'CONSTANT_Methodref' or self.tagName == 'CONSTANT_Fieldref' or self.tagName == 'CONSTANT_InterfaceMethodref':
						return self.classname == other.classname and self.methodname == other.methodname and self.methodtype == other.methodtype
					elif self.tagName == 'CONSTANT_NameAndType':
						return self.name == other.name and self.descriptor == other.descriptor
					elif self.tagName == 'CONSTANT_Utf8':
						return self.string == other.string
					elif self.tagName == 'CONSTANT_Integer' or self.tagName == 'CONSTANT_Float' or\
							self.tagName == 'CONSTANT_Long' or self.tagName == 'CONSTANT_Double':
						return self.value == other.value
					else:
						raise Exception ("unknown tag type: ", self.tagName)
				else:
					if self.tagName == 'CONSTANT_Utf8':
						return self.string == other.string
					elif self.tagName == 'CONSTANT_Class':
						return self.nameIndex == other.nameIndex
					elif self.tagName == 'CONSTANT_String':
						return self.stringIndex == other.stringIndex
					elif self.tagName == 'CONSTANT_Methodref' or self.tagName == 'CONSTANT_Fieldref' or self.tagName == 'CONSTANT_InterfaceMethodref':
						return self.classIndex == other.classIndex and self.nameAndTypeIndex == other.nameAndTypeIndex
					elif self.tagName == 'CONSTANT_NameAndType':
						return self.nameIndex == other.nameIndex and self.descriptorIndex == other.descriptorIndex
					elif self.tagName == 'CONSTANT_Integer' or self.tagName == 'CONSTANT_Float'\
							or self.tagName == 'CONSTANT_Long' or self.tagName == 'CONSTANT_Double':
						return self.value == other.value
					else:
						raise Exception("unknown constant type: " + self.tagName)





class ClassFileObject(object):
	def getAttributeByName(self, name):
		for attribute in self.attributes:
			if attribute.inlined and attribute.name == name:
				return attribute
			elif attribute.nameIndex.string == name:
				return attribute


class ClassFileField(ClassFileObject):
	def __init__(self, accessFlags, nameIndex, descriptorIndex, attributes):
		self.accessFlags = accessFlags
		self.nameIndex = nameIndex
		self.descriptorIndex = descriptorIndex
		self.attributes = attributes

	def link(self, classfile):
		flags = []
		code = self.accessFlags
		if code & 0x0001: # Declared public; may be accessed from outside its package.
			flags.append('ACC_PUBLIC')
		if code & 0x0002: # Declared private; usable only within the defining class.
			flags.append('ACC_PRIVATE')
		if code & 0x0004: # Declared protected; may be accessed within subclasses.
			flags.append('ACC_PROTECTED')
		if code & 0x0008: # Declared static.
			flags.append('ACC_STATIC')
		if code & 0x0010: # Declared final; never directly assigned to after object construction
			flags.append('ACC_FINAL')
		if code & 0x0040: # Declared volatile; cannot be cached.
			flags.append('ACC_VOLATILE')
		if code & 0x0080: # Declared transient; not written or read by a persistent object manager.
			flags.append('ACC_TRANSIENT')
		if code & 0x1000: # Declared synthetic; not present in the source code.
			flags.append('ACC_SYNTHETIC')
		if code & 0x4000: # Declared as an element of an enum.
			flags.append('ACC_ENUM')
		self.accessFlags = flags

		self.nameIndex = classfile.constantFromIndex(self.nameIndex, 'CONSTANT_Utf8')
		self.descriptorIndex = classfile.constantFromIndex(self.descriptorIndex, 'CONSTANT_Utf8')

		for attribute in self.attributes:
			attribute.link(classfile)

	def unlink(self, classfile):
		code = 0
		for flag in self.accessFlags:
			if flag == 'ACC_PUBLIC': # Declared public; may be accessed from outside its package.
				code |= 0x0001
			elif flag == 'ACC_PRIVATE': # Declared private; usable only within the defining class.
				code |= 0x0002
			elif flag == 'ACC_PROTECTED': # Declared protected; may be accessed within subclasses.
				code |= 0x0004
			elif flag == 'ACC_STATIC': # Declared static.
				code |= 0x0008
			elif flag == 'ACC_FINAL': # Declared final; never directly assigned to after object construction
				code |= 0x0010
			elif flag == 'ACC_VOLATILE': # Declared volatile; cannot be cached.
				code |= 0x0040
			elif flag == 'ACC_TRANSIENT': # Declared transient; not written or read by a persistent object manager.
				code |= 0x0080
			elif flag == 'ACC_SYNTHETIC': # Declared synthetic; not present in the source code.
				code |= 0x1000
			elif flag == 'ACC_ENUM': # Declared as an element of an enum.
				code |= 0x4000
			else:
				raise Exception('invalid flag for field.accessFlags:'+flag)
		self.accessFlags = code
		self.nameIndex = classfile.constantToIndex(self.nameIndex, 'CONSTANT_Utf8')
		self.descriptorIndex = classfile.constantToIndex(self.descriptorIndex, 'CONSTANT_Utf8')

		for attribute in self.attributes:
			attribute.unlink(classfile)

	def inline(self):
		self.name = self.nameIndex.string
		self.descriptor = self.descriptorIndex.string

		for attribute in self.attributes:
			attribute.inline()

	def uninline(self, classfile):
		self.nameIndex = classfile.getSetInlinedConstant(createConstant('CONSTANT_Utf8', self.name))
		self.descriptorIndex = classfile.getSetInlinedConstant(createConstant('CONSTANT_Utf8', self.descriptor))

		for attribute in self.attributes:
			attribute.uninline(classfile)

	def __str__(self):
		return 'ClassFileField(accessFlags='+str(self.accessFlags)+\
			',nameIndex='+str(self.nameIndex)+\
			',descriptorIndex='+str(self.descriptorIndex)+\
			',attributes='+str([ str(o) for o in self.attributes ])+')'





class ClassFileMethod(ClassFileObject):
	def __init__(self, accessFlags, nameIndex, descriptorIndex, attributes):
		self.accessFlags = accessFlags
		self.nameIndex = nameIndex
		self.descriptorIndex = descriptorIndex
		self.attributes = attributes

		self.exceptionsThrown = None

		self.codeStructure = None


	def isAbstract(self):
		return 'ACC_ABSTRACT' in self.accessFlags
	def isStatic(self):
		return 'ACC_STATIC' in self.accessFlags
	def isSpecial(self):
		return self.name == '<init>' or self.name == '<clinit>'


	def link(self, classfile):
		flags = []
		code = self.accessFlags
		if code & 0x0001: # Declared public; may be accessed from outside its package.
			flags.append('ACC_PUBLIC')
		if code & 0x0002: # Declared private; accessible only within the defining class.
			flags.append('ACC_PRIVATE')
		if code & 0x0004: # Declared protected; may be accessed within subclasses.
			flags.append('ACC_PROTECTED')
		if code & 0x0008: # Declared static.
			flags.append('ACC_STATIC')
		if code & 0x0010: # Declared final; must not be overridden.
			flags.append('ACC_FINAL')
		if code & 0x0020: # Declared synchronized; invocation is wrapped by a monitor use.
			flags.append('ACC_SYNCHRONIZED')
		if code & 0x0040: # A bridge method, generated by the compiler.
			flags.append('ACC_BRIDGE')
		if code & 0x0080: # Declared with variable number of arguments.
			flags.append('ACC_VARARGS')
		if code & 0x0100: # Declared native; implemented in a language other than Java.
			flags.append('ACC_NATIVE')
		if code & 0x0400: # Declared abstract; no implementation is provided.
			flags.append('ACC_ABSTRACT')
		if code & 0x0800: # Declared strictfp; floating-point mode is FP-strict.
			flags.append('ACC_STRICT')
		if code & 0x1000: # Declared synthetic; not present in the source code.
			flags.append('ACC_SYNTHETIC')
		self.accessFlags = flags

		self.nameIndex = classfile.constantFromIndex(self.nameIndex, 'CONSTANT_Utf8')
		self.descriptorIndex = classfile.constantFromIndex(self.descriptorIndex, 'CONSTANT_Utf8')

		for attribute in self.attributes:
			attribute.link(classfile)

		if 'ACC_ABSTRACT' not in self.accessFlags:
			self.unpackCodeAttribute(classfile)

		exceptionsAttribute = self.getAttributeByName('Exceptions')
		if exceptionsAttribute is not None:
			numberExceptions, = struct.unpack('>H', exceptionsAttribute.data[:2])
			exceptionsAttribute.data = [ index for index in struct.unpack('>' + 'H' * numberExceptions, exceptionsAttribute.data[2:]) ]
			exceptionsAttribute.data = [ classfile.constantFromIndex(index, 'CONSTANT_Class') for index in exceptionsAttribute.data ]
			# if not self.isAbstract():
			# 	self.codeStructure['exceptions_thrown'] = list(exceptionsAttribute.data)
			self.exceptionsThrown = list(exceptionsAttribute.data)

	def unlink(self, classfile):
		if 'ACC_ABSTRACT' not in self.accessFlags:
			self.packCodeAttribute(classfile)

		exceptionsAttribute = self.getAttributeByName('Exceptions')
		if exceptionsAttribute is not None:
			exceptionsAttribute.data = [ classfile.constantToIndex(index, 'CONSTANT_Class') for index in exceptionsAttribute.data ]
			exceptionsAttribute.data = struct.pack('>H' + 'H' * len(exceptionsAttribute.data), len(exceptionsAttribute.data),
					*exceptionsAttribute.data)

		code = 0
		for flag in self.accessFlags:
			if flag == 'ACC_PUBLIC': # Declared public; may be accessed from outside its package.
				code |= 0x0001
			elif flag == 'ACC_PRIVATE': # Declared private; accessible only within the defining class.
				code |= 0x0002
			elif flag == 'ACC_PROTECTED': # Declared protected; may be accessed within subclasses.
				code |= 0x0004
			elif flag == 'ACC_STATIC': # Declared static.
				code |= 0x0008
			elif flag == 'ACC_FINAL': # Declared final; must not be overridden.
				code |= 0x0010
			elif flag == 'ACC_SYNCHRONIZED': # Declared synchronized; invocation is wrapped by a monitor use.
				code |= 0x0020
			elif flag == 'ACC_BRIDGE': # A bridge method, generated by the compiler.
				code |= 0x0040
			elif flag == 'ACC_VARARGS': # Declared with variable number of arguments.
				code |= 0x0080
			elif flag == 'ACC_NATIVE': # Declared native; implemented in a language other than Java.
				code |= 0x0100
			elif flag == 'ACC_ABSTRACT': # Declared abstract; no implementation is provided.
				code |= 0x0400
			elif flag == 'ACC_STRICT': # Declared strictfp; floating-point mode is FP-strict.
				code |= 0x0800
			elif flag == 'ACC_SYNTHETIC': # Declared synthetic; not present in the source code.
				code |= 0x1000
			else:
				raise Exception('invalid flag for method.accessFlags:'+flag)
		self.accessFlags = code

		self.nameIndex = classfile.constantToIndex(self.nameIndex, 'CONSTANT_Utf8')
		self.descriptorIndex = classfile.constantToIndex(self.descriptorIndex, 'CONSTANT_Utf8')

		for attribute in self.attributes:
			attribute.unlink(classfile)


	def inline(self):
		self.name = self.nameIndex.string
		self.descriptor = self.descriptorIndex.string

		for attribute in self.attributes:
			attribute.inline()

		if 'ACC_ABSTRACT' not in self.accessFlags:
			for exception in self.codeStructure['exception_table']:
				if exception['catch_type'] is not None:
					exception['catch_type'] = exception['catch_type'].nameIndex.string

			for attribute in self.codeStructure['attributes']:
				attribute.inline()

			if 'stackmap' in self.codeStructure:
				self.inlineStackMap()

		exceptionsAttribute = self.getAttributeByName('Exceptions')
		if exceptionsAttribute is not None:
			exceptionsAttribute.data = [ classconst.nameIndex.string for classconst in exceptionsAttribute.data ]
			# self.codeStructure['exceptions_thrown'] = list(exceptionsAttribute.data)
			self.exceptionsThrown = list(exceptionsAttribute.data)

	def uninline(self, classfile):
		self.nameIndex = classfile.getSetInlinedConstant(createConstant('CONSTANT_Utf8', self.name))
		self.descriptorIndex = classfile.getSetInlinedConstant(createConstant('CONSTANT_Utf8', self.descriptor))

		for attribute in self.attributes:
			attribute.uninline(classfile)

		if 'ACC_ABSTRACT' not in self.accessFlags:
			for exception in self.codeStructure['exception_table']:
				if exception['catch_type'] is not None:
					exception['catch_type'] = classfile.getSetInlinedConstant(createConstant('CONSTANT_Class', exception['catch_type']))

			for attribute in self.codeStructure['attributes']:
				attribute.uninline(classfile)

			if 'stackmap' in self.codeStructure:
				self.uninlineStackMap(classfile)

		exceptionsAttribute = self.getAttributeByName('Exceptions')
		if exceptionsAttribute is not None:
			exceptionsAttribute.data = [ classfile.getSetInlinedConstant(createConstant('CONSTANT_Class', classname)) for classname in exceptionsAttribute.data ]
			# self.codeStructure['exceptions_thrown'] = list(exceptionsAttribute.data)
			self.exceptionsThrown = list(exceptionsAttribute.data)


	def unpackCodeAttribute(self, classfile):
		attribute = self.getAttributeByName('Code')
		if attribute is None:
			raise Exception('missing Code attribute in method')
		
		data = attribute.data
		codeStructure = {}
		codeStructure['max_stack'], codeStructure['max_locals'], codeStructure['code_length'], = struct.unpack('>HHL', data[:8])
		codeStructure['code'] = data[8 : 8 + codeStructure['code_length']]
		data = data[8 + codeStructure['code_length']:]

		codeStructure['exception_table_length'], = struct.unpack('>H', data[:2])
		codeStructure['exception_table'] = data[2 : 2 + 8 * codeStructure['exception_table_length']]
		codeStructure['exception_table'] = [ codeStructure['exception_table'][i * 8:i * 8 + 8] for i in range(codeStructure['exception_table_length']) ]
		for i in range(codeStructure['exception_table_length']):
			entry = {}
			entry['start_pc'], entry['end_pc'], entry['handler_pc'], entry['catch_type'], = struct.unpack('>HHHH', codeStructure['exception_table'][i])
			if entry['catch_type'] == 0: # 0 is a special case meaning catch all exceptions ('finally' keyword)
				entry['catch_type'] = None
			else:
				entry['catch_type'] = classfile.constantFromIndex(entry['catch_type'])
			codeStructure['exception_table'][i] = entry
		data = data[2 + 8 * codeStructure['exception_table_length']:]

		codeStructure['attributes_count'], = struct.unpack('>H', data[:2])
		data = data[2:]
		codeStructure['attributes'] = []
		for i in range(codeStructure['attributes_count']):
			code_attribute, data, = self.unpackAttribute(data)
			code_attribute.link(classfile)
			codeStructure['attributes'].append(code_attribute)

		if len(data) > 0:
			raise Exception("invalid data on the end of Code attribute: "+str(data))


		stackmap = None
		for code_attribute in codeStructure['attributes']:
			if code_attribute.nameIndex.string == 'StackMapTable':
				stackmap = code_attribute

		if stackmap is not None:
			data = stackmap.data
			frame_count, = struct.unpack('>H', data[:2])
			data = data[2:]
			codeStructure['stackmap_frame_count'] = frame_count

			stackframes = []
			for i in range(frame_count):
				frame, data = self.unpackStackFrame(data)
				stackframes.append(frame)

			codeStructure['stackmap'] = stackframes


		self.codeStructure = codeStructure

		if 'stackmap' in self.codeStructure:
			self.linkStackMap(classfile)


	def packCodeAttribute(self, classfile):
		codeStructure = self.codeStructure
		data = b''

		# allows changing code without bothering with code_length
		data += struct.pack('>HHL', codeStructure['max_stack'], codeStructure['max_locals'], len(codeStructure['code']))
		# data += struct.pack('>HHL', codeStructure['max_stack'], codeStructure['max_locals'], codeStructure['code_length'])
		data += codeStructure['code']

		# allows changing exceptions without bothering with exception_table_length
		data += struct.pack('>H', len(codeStructure['exception_table']))
		# data += struct.pack('>H', codeStructure['exception_table_length'])
		for entry in codeStructure['exception_table']:
			if entry['catch_type'] is None:
				entry['catch_type'] = 0
			else:
				entry['catch_type'] = classfile.constantToIndex(entry['catch_type'])
			data += struct.pack('>HHHH', entry['start_pc'], entry['end_pc'], entry['handler_pc'], entry['catch_type'])

		# allows changing attributes without bothering with attributes_count
		data += struct.pack('>H', len(codeStructure['attributes']))
		# data += struct.pack('>H', codeStructure['attributes_count'])
		for code_attribute in codeStructure['attributes']:
			if code_attribute.nameIndex.string == 'StackMapTable':
				self.unlinkStackMap(classfile)

				smt_data = struct.pack('>H', len(self.codeStructure['stackmap'])) + b''.join( self.packStackFrame(frame) for frame in self.codeStructure['stackmap'] )
				code_attribute.data = smt_data

			code_attribute.unlink(classfile)
			data += self.packAttribute(code_attribute)

		attribute = self.getAttributeByName('Code')
		attribute.data = data


	def linkStackMap(self, classfile):
		for frame in self.codeStructure['stackmap']:
			if frame['frame_type'] == 'same_locals_1_stack_item_frame' or frame['frame_type'] == 'same_locals_1_stack_item_frame_extended':
				if frame['stack'][0] == 'ITEM_Object':
					frame['stack'][1] = classfile.constantFromIndex(frame['stack'][1], 'CONSTANT_Class')
			elif frame['frame_type'] == 'append_frame':
				for typeinfo in frame['stack']:
					if typeinfo[0] == 'ITEM_Object':
						typeinfo[1] = classfile.constantFromIndex(typeinfo[1], 'CONSTANT_Class')
			elif frame['frame_type'] == 'full_frame':
				for typeinfo in frame['locals_stack']:
					if typeinfo[0] == 'ITEM_Object':
						typeinfo[1] = classfile.constantFromIndex(typeinfo[1], 'CONSTANT_Class')
				for typeinfo in frame['stack']:
					if typeinfo[0] == 'ITEM_Object':
						typeinfo[1] = classfile.constantFromIndex(typeinfo[1], 'CONSTANT_Class')
					

	def unlinkStackMap(self, classfile):
		# self.nameIndex = classfile.constantToIndex(self.nameIndex, 'CONSTANT_Utf8')
		for frame in self.codeStructure['stackmap']:
			if frame['frame_type'] == 'same_locals_1_stack_item_frame' or frame['frame_type'] == 'same_locals_1_stack_item_frame_extended':
				if frame['stack'][0] == 'ITEM_Object':
					frame['stack'][1] = classfile.constantToIndex(frame['stack'][1], 'CONSTANT_Class')
			elif frame['frame_type'] == 'append_frame':
				for typeinfo in frame['stack']:
					if typeinfo[0] == 'ITEM_Object':
						typeinfo[1] = classfile.constantToIndex(typeinfo[1], 'CONSTANT_Class')
			elif frame['frame_type'] == 'full_frame':
				for typeinfo in frame['locals_stack']:
					if typeinfo[0] == 'ITEM_Object':
						typeinfo[1] = classfile.constantToIndex(typeinfo[1], 'CONSTANT_Class')
				for typeinfo in frame['stack']:
					if typeinfo[0] == 'ITEM_Object':
						typeinfo[1] = classfile.constantToIndex(typeinfo[1], 'CONSTANT_Class')

	def inlineStackMap(self):
		for frame in self.codeStructure['stackmap']:
			if frame['frame_type'] == 'same_locals_1_stack_item_frame' or frame['frame_type'] == 'same_locals_1_stack_item_frame_extended':
				if frame['stack'][0] == 'ITEM_Object':
					frame['stack'][1] = frame['stack'][1].nameIndex.string
			elif frame['frame_type'] == 'append_frame':
				for typeinfo in frame['stack']:
					if typeinfo[0] == 'ITEM_Object':
						typeinfo[1] = typeinfo[1].nameIndex.string
			elif frame['frame_type'] == 'full_frame':
				for typeinfo in frame['locals_stack']:
					if typeinfo[0] == 'ITEM_Object':
						typeinfo[1] = typeinfo[1].nameIndex.string
				for typeinfo in frame['stack']:
					if typeinfo[0] == 'ITEM_Object':
						typeinfo[1] = typeinfo[1].nameIndex.string
	def uninlineStackMap(self, classfile):
		for frame in self.codeStructure['stackmap']:
			if frame['frame_type'] == 'same_locals_1_stack_item_frame' or frame['frame_type'] == 'same_locals_1_stack_item_frame_extended':
				if frame['stack'][0] == 'ITEM_Object':
					frame['stack'][1] = classfile.getSetInlinedConstant(createConstant('CONSTANT_Class', frame['stack'][1]))
			elif frame['frame_type'] == 'append_frame':
				for typeinfo in frame['stack']:
					if typeinfo[0] == 'ITEM_Object':
						typeinfo[1] = classfile.getSetInlinedConstant(createConstant('CONSTANT_Class', typeinfo[1]))
			elif frame['frame_type'] == 'full_frame':
				for typeinfo in frame['locals_stack']:
					if typeinfo[0] == 'ITEM_Object':
						typeinfo[1] = classfile.getSetInlinedConstant(createConstant('CONSTANT_Class', typeinfo[1]))
				for typeinfo in frame['stack']:
					if typeinfo[0] == 'ITEM_Object':
						typeinfo[1] = classfile.getSetInlinedConstant(createConstant('CONSTANT_Class', typeinfo[1]))




	def unpackStackFrame(self, data):
		frame_type, = struct.unpack('>B', data[0:1])
		data = data[1:]
		if frame_type >= 0 and frame_type <= 63:
			return { 'frame_type' : 'same_frame', 'offset_delta' : frame_type }, data
		elif frame_type >= 64 and frame_type <= 127:
			typeinfo, data = self.unpackStackTypeInfo(data)
			return { 'frame_type' : 'same_locals_1_stack_item_frame', 'offset_delta' : frame_type - 64, 'stack' : typeinfo }, data
		elif frame_type == 247:
			offset_delta, = struct.unpack('>H', data[0:2])
			data = data[2:]
			typeinfo, data = self.unpackStackTypeInfo(data)
			return { 'frame_type' : 'same_locals_1_stack_item_frame_extended', 'offset_delta' : offset_delta, 'stack' : typeinfo }, data
		elif frame_type >= 248 and frame_type <= 250:
			offset_delta, = struct.unpack('>H', data[0:2])
			data = data[2:]
			locals_absent = 251 - frame_type
			return { 'frame_type' : 'chop_frame', 'offset_delta' : offset_delta, 'locals_absent' : locals_absent }, data
		elif frame_type == 251:
			offset_delta, = struct.unpack('>H', data[0:2])
			data = data[2:]
			return { 'frame_type' : 'same_frame_extended', 'offset_delta' : offset_delta }, data
		elif frame_type >= 252 and frame_type <= 254:
			offset_delta, = struct.unpack('>H', data[0:2])
			data = data[2:]
			locals_appended = frame_type - 251
			stack = []
			for i in range(locals_appended):
				typeinfo, data = self.unpackStackTypeInfo(data)
				stack.append(typeinfo)
			return {
				'frame_type' : 'append_frame',
				'offset_delta' : offset_delta,
				# 'locals_appended' : locals_appended,
				'stack' : stack,
			}, data
		elif frame_type == 255:
			offset_delta, number_of_locals = struct.unpack('>HH', data[0:4])
			data = data[4:]
			locals_stack = []
			for i in range(number_of_locals):
				typeinfo, data = self.unpackStackTypeInfo(data)
				locals_stack.append(typeinfo)
			number_of_stack, = struct.unpack('>H', data[0:2])
			data = data[2:]
			stack = []
			for i in range(number_of_stack):
				typeinfo, data = self.unpackStackTypeInfo(data)
				stack.append(typeinfo)
			return {
				'frame_type' : 'full_frame',
				'offset_delta' : offset_delta,
				# 'number_of_locals' : number_of_locals,
				'locals_stack' : locals_stack,
				# 'number_of_stack' : number_of_stack,
				'stack' : stack,
			}, data

		else:
			raise Exception ("invalid stack frame type: "+str(frame_type))

	def unpackStackTypeInfo(self, data):
		variable_type, = struct.unpack('>B', data[0:1])
		if variable_type == 0:
			return ['ITEM_Top'], data[1:]
		elif variable_type == 1:
			return ['ITEM_Integer'], data[1:]
		elif variable_type == 2:
			return ['ITEM_Float'], data[1:]
		elif variable_type == 3:
			return ['ITEM_Double'], data[1:]
		elif variable_type == 4:
			return ['ITEM_Long'], data[1:]
		elif variable_type == 5:
			return ['ITEM_Null'], data[1:]
		elif variable_type == 6:
			return ['ITEM_UninitializedThis'], data[1:]
		elif variable_type == 7:
			const, = struct.unpack('>H', data[1:3])
			return ['ITEM_Object', const], data[3:]
		elif variable_type == 8:
			offset, = struct.unpack('>H', data[1:3])
			return ['ITEM_Uninitialized', offset], data[3:]
		else:
			raise Exception ("unknown variable type: "+str(variable_type))


	def packStackFrame(self, stackframe):
		# frame_type, = struct.unpack('>B', data[0:1])
		# data = data[1:]
		if stackframe['frame_type'] == 'same_frame':
			return struct.pack('>B', stackframe['offset_delta'])
		# if frame_type >= 0 and frame_type <= 63:
			# return { 'frame_type' : 'same_frame', 'offset_delta' : frame_type }, data
		elif stackframe['frame_type'] == 'same_locals_1_stack_item_frame':
			return struct.pack('>B', stackframe['offset_delta'] + 64) + self.packStackTypeInfo(stackframe['stack'])
		# elif frame_type >= 64 and frame_type <= 127:
			# typeinfo, data = 
			# return { 'frame_type' : 'same_locals_1_stack_item_frame', 'offset_delta' : , 'stack' : typeinfo }, data
		elif stackframe['frame_type'] == 'same_locals_1_stack_item_frame_extended':
			return struct.pack('>BH', 247, stackframe['offset_delta']) + self.packStackTypeInfo(stackframe['stack'])
		# elif frame_type == 247:
		# 	offset_delta, = struct.unpack('>H', data[0:2])
		# 	data = data[2:]
		# 	typeinfo, data = self.unpackStackTypeInfo(data)
		# 	return { 'frame_type' : 'same_locals_1_stack_item_frame_extended', 'offset_delta' : offset_delta, 'stack' : typeinfo }, data
		elif stackframe['frame_type'] == 'chop_frame':
			return struct.pack('>BH', 251 - stackframe['locals_absent'], stackframe['offset_delta'])
		# elif frame_type >= 248 and frame_type <= 250:
		# 	offset_delta, = struct.unpack('>H', data[0:2])
		# 	data = data[2:]
		# 	locals_absent = 251 - frame_type
		# 	return { 'frame_type' : 'chop_frame', 'offset_delta' : offset_delta, 'locals_absent' : locals_absent }, data
		elif stackframe['frame_type'] == 'same_frame_extended':
			return struct.pack('>BH', 251, stackframe['offset_delta'])
		# elif frame_type == 251:
		# 	offset_delta, = struct.unpack('>H', data[0:2])
		# 	data = data[2:]
		# 	return { 'frame_type' : 'same_frame_extended', 'offset_delta' : offset_delta }, data
		elif stackframe['frame_type'] == 'append_frame':
			return struct.pack('>BH', 251 + len(stackframe['stack']), stackframe['offset_delta']) +\
					b''.join( self.packStackTypeInfo(typeinfo) for typeinfo in stackframe['stack'] )
		# elif frame_type >= 252 and frame_type <= 254:
		# 	offset_delta, = struct.unpack('>H', data[0:2])
		# 	data = data[2:]
		# 	locals_appended = frame_type - 251
		# 	stack = []
		# 	for i in range(locals_appended):
		# 		typeinfo, data = self.unpackStackTypeInfo(data)
		# 		stack.append(typeinfo)
		# 	return {
		# 		'frame_type' : 'append_frame',
		# 		'offset_delta' : offset_delta,
		# 		# 'locals_appended' : locals_appended,
		# 		'stack' : stack,
		# 	}, data
		elif stackframe['frame_type'] == 'full_frame':
			return struct.pack('>BHH', 255, stackframe['offset_delta'], len(stackframe['locals_stack'])) +\
					b''.join( self.packStackTypeInfo(typeinfo) for typeinfo in stackframe['locals_stack'] ) +\
					struct.pack('>H', len(stackframe['stack'])) + b''.join( self.packStackTypeInfo(typeinfo) for typeinfo in stackframe['stack'] )
		# elif frame_type == 255:
			# offset_delta, number_of_locals = struct.unpack('>HH', data[0:4])
			# data = data[4:]
			# locals_stack = []
			# for i in range(number_of_locals):
			# 	typeinfo, data = self.unpackStackTypeInfo(data)
			# 	locals_stack.append(typeinfo)
			# number_of_stack, = struct.unpack('>H', data[0:2])
			# data = data[2:]
			# stack = []
			# for i in range(number_of_stack):
			# 	typeinfo, data = self.unpackStackTypeInfo(data)
			# 	stack.append(typeinfo)
			# return {
			# 	'frame_type' : 'full_frame',
			# 	'offset_delta' : offset_delta,
			# 	# 'number_of_locals' : number_of_locals,
			# 	'locals_stack' : locals_stack,
			# 	# 'number_of_stack' : number_of_stack,
			# 	'stack' : stack,
			# }, data

		else:
			raise Exception ("invalid stack frame type: "+stackframe['frame_type'])

	def packStackTypeInfo(self, typeinfo):
		# variable_type, = struct.unpack('>B', data[0:1])
		if typeinfo[0] == 'ITEM_Top':
			return struct.pack('>B', 0)
		elif typeinfo[0] == 'ITEM_Integer':
			return struct.pack('>B', 1)
		# elif variable_type == 1:
		# 	return ['ITEM_Integer'], data[1:]
		elif typeinfo[0] == 'ITEM_Float':
			return struct.pack('>B', 2)
		# elif variable_type == 2:
		# 	return ['ITEM_Float'], data[1:]
		elif typeinfo[0] == 'ITEM_Double':
			return struct.pack('>B', 3)
		# elif variable_type == 3:
		# 	return ['ITEM_Double'], data[1:]
		elif typeinfo[0] == 'ITEM_Long':
			return struct.pack('>B', 4)
		# elif variable_type == 4:
		# 	return ['ITEM_Long'], data[1:]
		elif typeinfo[0] == 'ITEM_Null':
			return struct.pack('>B', 5)
		# elif variable_type == 5:
		# 	return ['ITEM_Null'], data[1:]
		elif typeinfo[0] == 'ITEM_UninitializedThis':
			return struct.pack('>B', 6)
		# elif variable_type == 6:
		# 	return ['ITEM_UninitializedThis'], data[1:]
		elif typeinfo[0] == 'ITEM_Object':
			return struct.pack('>BH', 7, typeinfo[1])
		# elif variable_type == 7:
		# 	const = struct.unpack('>H', data[1:3])
		# 	return ['ITEM_Object', const], data[3:]
		elif typeinfo[0] == 'ITEM_Uninitialized':
			return struct.pack('>BH', 8, typeinfo[1])
		# elif variable_type == 8:
		# 	offset = struct.unpack('>H', data[1:3])
		# 	return ['ITEM_Uninitialized', offset], data[3:]
		else:
			raise Exception ("unknown typeinfo type: "+str(typeinfo[0]))

	def unpackAttribute(self, data):
		attributeNameIndex, attributeLength = struct.unpack('>HI', data[:6])
		attributeData = data[6 : 6 + attributeLength]
		return ClassFileAttribute(attributeNameIndex, attributeData), data[6+attributeLength:]
	def packAttribute(self, attribute):
		data = struct.pack('>HI', attribute.nameIndex, len(attribute.data))
		data += attribute.data
		return data

	def __str__(self):
		return 'ClassFileMethod(\n\taccessFlags='+str(self.accessFlags)+\
			',\n\tnameIndex='+str(self.nameIndex)+\
			',\n\tdescriptorIndex='+str(self.descriptorIndex)+\
			',\n\tattributes=['+', '.join([ str(o) for o in self.attributes ])+\
			'],\n\tcode='+str(self.codeStructure)+'\n)'


class ClassFileAttribute(object):
	def __init__(self, nameIndex, data):
		self.nameIndex = nameIndex
		self.data = data
		self.inlined = False
	def link(self, classfile):
		self.nameIndex = classfile.constantFromIndex(self.nameIndex, 'CONSTANT_Utf8')
	def unlink(self, classfile):
		self.nameIndex = classfile.constantToIndex(self.nameIndex, 'CONSTANT_Utf8')
	def inline(self):
		self.inlined = True
		self.name = self.nameIndex.string
	def uninline(self, classfile):
		self.inlined = False
		self.nameIndex = classfile.getSetInlinedConstant(createConstant('CONSTANT_Utf8', self.name))
	def __str__(self):
		return 'ClassFileAttribute(nameIndex='+str(self.nameIndex)+', data='+str(self.data)+')'




























class ClassFile(ClassFileObject):
	def __init__(self):
		pass
		# self.filepath = filepath
		# self.unpackClassFile()

	def fromFile(self, filepath):
		self.filepath = filepath
		self.unpackClassFile(filepath)

	def toFile(self, filepath=None):
		if filepath is None:
			filepath = self.filepath

		self.packClassFile(filepath)



	def getFieldsByName(self, name, descriptor=None):
		'''
			returns a list of ClassFileField objects matching the name (and optionally descriptor)
			requires the classfile to be inlined
		'''
		if descriptor is None:
			return [ field for field in self.fields if field.name == name ]
		else:
			return [ field for field in self.fields if field.name == name and field.descriptor == descriptor ]

	def getMethodsByName(self, name=None, descriptor=None):
		'''
			returns a list of ClassFileMethod objects matching the name (and optionally descriptor)
			requires the classfile to be inlined
		'''
		return [ method for method in self.methods if (name is None or method.name == name) and (descriptor is None or method.descriptor == descriptor) ]

	# takes a class-file format constant index and returns the given constant
	# the constType option allows safely retrieving a specific type of constant
	def constantFromIndex(self, index, constType='*'):
		if index < 1 or index > len(self.constants):
			raise Exception('out-of-bounds constant index '+str(index)+' for constType "'+constType+'"')
		const = self.constants[index - 1]
		if constType != '*' and const.tagName != constType:
			raise Exception('invalid constant type at index '+str(index)+': "'+const.tagName+'" (expected "'+constType+'")')
		return const

	# takes a constant object and retrieves the associated class-file format index
	# the constType option allows safely storing a specific type of constant
	def constantToIndex(self, const, constType='*'):
		if constType != '*' and const.tagName != constType:
			raise Exception('invalid constant type: "'+const.tagName+'" (expected "'+constType+'"')
		try:
			index = self.constants.index(const) + 1
		except ValueError:
			raise Exception("attempt to get index from missing constant: "+str(const))
		return index

	# returns an equivalent constant or stores the given constant if an equivalent isn't found and returns it
	def getSetInlinedConstant(self, const):
		try:
			index = self.constants.index(const)
			return self.constants[index]
		except ValueError:
			self.constants.append(const)
			return const



	def unpackClassFile(self, filepath):
		try:
			self.handle = open(filepath, 'rb')

			# read the file header
			data = self.handle.read(10)
			fileStructure = {}
			fileStructure['magic'], fileStructure['version_minor'], fileStructure['version_major'], fileStructure['const_count'] = struct.unpack('>4sHHH', data)
			
			# extract the constants
			constants = []
			i = 1
			while i < fileStructure['const_count']:
				const = self.unpackConstant()
				constants.append(const)
				# print ('#', i, 'of', fileStructure['const_count'], const) # DEBUG UNPACK
				i += 1
				if const.tagName == 'CONSTANT_Long' or const.tagName == 'CONSTANT_Double':
					# longs and doubles take up two constant slots
					# because the guy that designed this format is an idiot
					i += 1
					constants.append(None)
					
			fileStructure['constants'] = constants

			# more header data
			data = self.handle.read(8)
			fileStructure['access_flags'], fileStructure['this_class'], fileStructure['super_class'], fileStructure['interface_count'] = struct.unpack('>HHHH', data)

			# extract interface indicies
			fileStructure['interfaces'] = []
			for _ in range(fileStructure['interface_count']):
				data = self.handle.read(2)
				index, = struct.unpack('>H', data)
				fileStructure['interfaces'].append(index)

			# extract fields
			data = self.handle.read(2)
			fileStructure['fields_count'], = struct.unpack('>H', data)
			fileStructure['fields'] = [ self.unpackField() for _ in range(fileStructure['fields_count']) ]


			# extract methods
			data = self.handle.read(2)
			fileStructure['methods_count'], = struct.unpack('>H', data)
			fileStructure['methods'] = [ self.unpackMethod() for _ in range(fileStructure['methods_count']) ]

			# extract attributes
			data = self.handle.read(2)
			fileStructure['attributes_count'], = struct.unpack('>H', data)
			fileStructure['attributes'] = [ self.unpackAttribute() for _ in range(fileStructure['attributes_count']) ]

			# used to store everything in fileStructure, but it's more efficient to store everything in instance variables
			# self.fileStructure = fileStructure
			self.handle.close()


			# transfer all the necessary data
			self.constants = fileStructure['constants']
			self.interfaces = fileStructure['interfaces']
			self.fields = fileStructure['fields']
			self.methods = fileStructure['methods']
			self.attributes = fileStructure['attributes']

			self.magic = fileStructure['magic']
			self.version_major = fileStructure['version_major']
			self.version_minor = fileStructure['version_minor']

			self.access_flags = fileStructure['access_flags']
			self.this_class = fileStructure['this_class']
			self.super_class = fileStructure['super_class']

		except Exception as e:
			raise Exception('exception ('+str(type(e))+') occured while unpacking class file "'+self.filepath+'":\n\t' + str(e))

	def unpackConstant(self):
		data = self.handle.read(1)
		tagType, = struct.unpack('B', data)
		const = ClassFileConstant(tagType)

		# unpack some more data for the constant
		if const.tagName == 'CONSTANT_Class':
			data = self.handle.read(2)
			const.nameIndex, = struct.unpack('>H', data)
		elif const.tagName == 'CONSTANT_String':
			data = self.handle.read(2)
			const.stringIndex, = struct.unpack('>H', data)
		elif const.tagName == 'CONSTANT_Utf8':
			data = self.handle.read(2)
			const.length, = struct.unpack('>H', data)
			data = self.handle.read(const.length)
			const.string = data.decode('utf8')
		elif const.tagName == 'CONSTANT_Integer':
			data = self.handle.read(4)
			const.value, = struct.unpack('>i', data)
		elif const.tagName == 'CONSTANT_Float':
			data = self.handle.read(4)
			const.value, = struct.unpack('>f', data)
		elif const.tagName == 'CONSTANT_Long':
			data = self.handle.read(8)
			const.value, = struct.unpack('>q', data)
		elif const.tagName == 'CONSTANT_Double':
			data = self.handle.read(8)
			const.value, = struct.unpack('>d', data)
		elif const.tagName == 'CONSTANT_Fieldref' or const.tagName == 'CONSTANT_Methodref' or const.tagName == 'CONSTANT_InterfaceMethodref':
			data = self.handle.read(4)
			const.classIndex, const.nameAndTypeIndex, = struct.unpack('>HH', data)
		elif const.tagName == 'CONSTANT_NameAndType':
			data = self.handle.read(4)
			const.nameIndex, const.descriptorIndex, = struct.unpack('>HH', data)
		elif const.tagName == 'CONSTANT_MethodHandle':
			data = self.handle.read(3)
			const.referenceKind, const.referenceIndex, = struct.unpack('>BH', data)
		elif const.tagName == 'CONSTANT_MethodType':
			data = self.handle.read(2)
			const.descriptorIndex, = struct.unpack('>H', data)
		elif const.tagName == 'CONSTANT_InvokeDynamic':
			data = self.handle.read(4)
			const.bootstrapIndex, const.nameAndTypeIndex, = struct.unpack('>HH', data)

		return const

	def unpackField(self):
		data = self.handle.read(8)
		accessFlags, nameIndex, descriptorIndex, attributesCount = struct.unpack('>HHHH', data)
		attributes = [ self.unpackAttribute() for _ in range(attributesCount) ]
		return ClassFileField(accessFlags, nameIndex, descriptorIndex, attributes)

	def unpackMethod(self):
		data = self.handle.read(8)
		accessFlags, nameIndex, descriptorIndex, attributesCount = struct.unpack('>HHHH', data)
		attributes = [ self.unpackAttribute() for _ in range(attributesCount) ]
		return ClassFileMethod(accessFlags, nameIndex, descriptorIndex, attributes)


	def unpackAttribute(self):
		data = self.handle.read(6)
		attributeNameIndex, attributeLength = struct.unpack('>HI', data)
		attributeData = self.handle.read(attributeLength)
		return ClassFileAttribute(attributeNameIndex, attributeData)

	def packClassFile(self, filepath):
		try:
			# file writing
			self.handle = open(filepath, 'wb')

			# pack header
			data = struct.pack('>4sHHH', self.magic, self.version_minor, self.version_major, len(self.constants) + 1)
			self.handle.write(data)
			
			# pack constants
			for const in self.constants:
				if const is not None:
					self.handle.write(self.packConstant(const))
			
			# pack more header
			data = struct.pack('>HHHH', self.access_flags, self.this_class, self.super_class, len(self.interfaces))
			self.handle.write(data)

			# pack interface indicies
			for interface in self.interfaces:
				self.handle.write(struct.pack('>H', interface))

			# pack fields
			self.handle.write(struct.pack('>H', len(self.fields)))
			for field in self.fields:
				self.handle.write(self.packField(field))

			# pack methods
			self.handle.write(struct.pack('>H', len(self.methods)))
			for method in self.methods:
				self.handle.write(self.packMethod(method))

			# pack attributes
			self.handle.write(struct.pack('>H', len(self.attributes)))
			for attribute in self.attributes:
				self.handle.write(self.packAttribute(attribute))

			self.handle.close()
		except Exception as e:
			raise Exception('exception ('+str(type(e))+') occured while packing class file "'+self.filepath+'":\n\t' + str(e))

	def packConstant(self, const):
		data = struct.pack('B', const.tagType)

		# unpack some more data for the constant
		if const.tagName == 'CONSTANT_Class':
			data += struct.pack('>H', const.nameIndex)
		elif const.tagName == 'CONSTANT_String':
			data += struct.pack('>H', const.stringIndex)
		elif const.tagName == 'CONSTANT_Utf8':
			strdata = const.string.encode()
			data += struct.pack('>H', len(strdata))
			data += strdata
		elif const.tagName == 'CONSTANT_Integer':
			data += struct.pack('>i', const.value)
		elif const.tagName == 'CONSTANT_Float':
			data += struct.pack('>f', const.value)
		elif const.tagName == 'CONSTANT_Long':
			data += struct.pack('>q', const.value)
		elif const.tagName == 'CONSTANT_Double':
			data += struct.pack('>d', const.value)
		elif const.tagName == 'CONSTANT_Fieldref' or const.tagName == 'CONSTANT_Methodref' or const.tagName == 'CONSTANT_InterfaceMethodref':
			data += struct.pack('>HH', const.classIndex, const.nameAndTypeIndex)
		elif const.tagName == 'CONSTANT_NameAndType':
			data += struct.pack('>HH', const.nameIndex, const.descriptorIndex)
		elif const.tagName == 'CONSTANT_MethodHandle':
			data += struct.pack('>BH', const.referenceKind, const.referenceIndex)
		elif const.tagName == 'CONSTANT_MethodType':
			data += struct.pack('>H', const.descriptorIndex)
		elif const.tagName == 'CONSTANT_InvokeDynamic':
			data += struct.pack('>HH', const.bootstrapIndex, const.nameAndTypeIndex)

		return data

	def packField(self, field):
		data = struct.pack('>HHHH', field.accessFlags, field.nameIndex, field.descriptorIndex, len(field.attributes))
		for attribute in field.attributes:
			data += self.packAttribute(attribute)
		return data

	def packMethod(self, method):
		data = struct.pack('>HHHH', method.accessFlags, method.nameIndex, method.descriptorIndex, len(method.attributes))
		for attribute in method.attributes:
			data += self.packAttribute(attribute)
		return data


	def packAttribute(self, attribute):
		data = struct.pack('>HI', attribute.nameIndex, len(attribute.data))
		data += attribute.data
		return data



	def unpackAccessFlags(self):
		flags = []
		code = self.access_flags
		if code & 0x0001: # Declared public; may be accessed from outside its package.
			flags.append('ACC_PUBLIC')
		if code & 0x0010: # Declared final; no subclasses allowed.
			flags.append('ACC_FINAL')
		if code & 0x0020: # Treat superclass methods specially when invoked by the invokespecial instruction.
			flags.append('ACC_SUPER')
		if code & 0x0200: # Is an interface, not a class.
			flags.append('ACC_INTERFACE')
		if code & 0x0400: # Declared abstract; must not be instantiated.
			flags.append('ACC_ABSTRACT')
		if code & 0x1000: # Declared synthetic; not present in the source code.
			flags.append('ACC_SYNTHETIC')
		if code & 0x2000: # Declared as an annotation type.
			flags.append('ACC_ANNOTATION')
		if code & 0x4000: # Declared as an enum type.
			flags.append('ACC_ENUM')
		self.access_flags = flags

	def packAccessFlags(self):
		flags = self.access_flags
		code = 0
		for flag in flags:
			if flag == 'ACC_PUBLIC': # Declared public; may be accessed from outside its package.
				code |= 0x0001
			elif flag == 'ACC_FINAL': # Declared final; no subclasses allowed.
				code |= 0x0010
			elif flag == 'ACC_SUPER': # Treat superclass methods specially when invoked by the invokespecial instruction.
				code |= 0x0020
			elif flag == 'ACC_INTERFACE': # Is an interface, not a class.
				code |= 0x0200
			elif flag == 'ACC_ABSTRACT': # Declared abstract; must not be instantiated.
				code |= 0x0400
			elif flag == 'ACC_SYNTHETIC': # Declared synthetic; not present in the source code.
				code |= 0x1000
			elif flag == 'ACC_ANNOTATION': # Declared as an annotation type.
				code |= 0x2000
			elif flag == 'ACC_ENUM': # Declared as an enum type.
				code |= 0x4000
			else:
				raise Exception('invalid flag for file.access_flags:'+flag)
		self.access_flags = code


	def linkClassFile(self):
		try:
			self.unpackAccessFlags()

			self.this_class = self.constantFromIndex(self.this_class, 'CONSTANT_Class')
			self.super_class = self.constantFromIndex(self.super_class, 'CONSTANT_Class')

			self.interfaces = [ self.constantFromIndex(index, 'CONSTANT_Class') for index in self.interfaces ]


			for const in self.constants:
				if const is not None: # can be None due to Long and Double constants creating holes
					const.link(self)

			for field in self.fields:
				field.link(self)

			for attribute in self.attributes:
				attribute.link(self)

			for method in self.methods:
				method.link(self)

			# for method in self.methods:
			# 	method.unpackCodeAttribute(self)


			# unpack and link SourceFile attribute if it exists
			sourcefile = self.getAttributeByName('SourceFile')
			if sourcefile is not None:
				sourcefileIndex, = struct.unpack('>H', sourcefile.data)
				sourcefile.data = self.constantFromIndex(sourcefileIndex, 'CONSTANT_Utf8')
		except Exception as e:
			raise Exception('exception ('+str(type(e))+') occured while linking class file "'+self.filepath+'":\n\t' + str(e))




	def unlinkClassFile(self):
		try:
			# unlink and pack SourceFile attribute if it exists
			sourcefile = self.getAttributeByName('SourceFile')
			if sourcefile is not None:
				sourcefileIndex = self.constantToIndex(sourcefile.data, 'CONSTANT_Utf8')
				sourcefile.data = struct.pack('>H', sourcefileIndex)


			# for method in self.methods:
			# 	method.packCodeAttribute(self)

			for method in self.methods:
				method.unlink(self)

			for field in self.fields:
				field.unlink(self)

			for attribute in self.attributes:
				attribute.unlink(self)


			self.packAccessFlags()

			self.this_class = self.constantToIndex(self.this_class, 'CONSTANT_Class')
			self.super_class = self.constantToIndex(self.super_class, 'CONSTANT_Class')

			# indexes = []
			# for interface in self.interfaces:
			# 	if interface.tagName != 'CONSTANT_Class':
			# 		raise Exception('invalid constant type for file.interface['+str(index)+']:'+interface.tagName)
			# 	const = self.constants[index - 1]
			# 	indexes.append(self.constants.index(interface) + 1)
			self.interfaces = [ self.constantToIndex(interface, 'CONSTANT_Class') for interface in self.interfaces ]

			for const in self.constants:
				if const is not None: # can be None due to Long and Double constants creating holes
					const.unlink(self)
		except Exception as e:
			raise Exception('exception ('+str(type(e))+') occured while unlinking class file "'+self.filepath+'":\n\t' + str(e))


	def inlineClassFile(self):
		try:
			for const in self.constants:
				if const is not None: # can be None due to Long and Double constants creating holes
					const.inline()
			for const in self.constants:
				if const is not None: # can be None due to Long and Double constants creating holes
					const.setInlined(True)

			for field in self.fields:
				field.inline()
			for method in self.methods:
				method.inline()
			for attribute in self.attributes:
				attribute.inline()
			self.interfaces = [ interface.nameIndex.string for interface in self.interfaces ]

			self.this_class = self.this_class.classname
			self.super_class = self.super_class.classname

			# inline SourceFile attribute if it exists
			sourcefile = self.getAttributeByName('SourceFile')
			if sourcefile is not None:
				sourcefile.data = sourcefile.data.string
		except Exception as e:
			raise Exception('exception ('+str(type(e))+') occured while inlining class file "'+self.filepath+'":\n\t' + str(e))

	def uninlineClassFile(self):
		try:
			# uninline SourceFile attribute if it exists
			sourcefile = self.getAttributeByName('SourceFile')
			if sourcefile is not None:
				sourcefile.data = self.getSetInlinedConstant(createConstant('CONSTANT_Utf8', sourcefile.data))

			self.this_class = self.getSetInlinedConstant(createConstant('CONSTANT_Class', self.this_class))
			self.super_class = self.getSetInlinedConstant(createConstant('CONSTANT_Class', self.super_class))

			for field in self.fields:
				field.uninline(self)
			for method in self.methods:
				method.uninline(self)
			for attribute in self.attributes:
				attribute.uninline(self)
			self.interfaces = [ self.getSetInlinedConstant(createConstant('CONSTANT_Class', interface)) for interface in self.interfaces ]

			for const in self.constants:
				if const is not None: # can be None due to Long and Double constants creating holes
					const.uninline(self)
			for const in self.constants:
				if const is not None: # can be None due to Long and Double constants creating holes
					const.setInlined(False)
		except Exception as e:
			raise Exception('exception ('+str(type(e))+') occured while uninlining class file "'+self.filepath+'":\n\t' + str(e))


	def linkBytecode(self):
		try:
			for method in self.methods:
				if 'ACC_ABSTRACT' not in method.accessFlags:
					method.codeStructure['code'] = classbytecode.decompileAndLink(method.codeStructure['code'], self)
		except Exception as e:
			raise Exception('exception ('+str(type(e))+') occured while linking bytecode of class file "'+self.filepath+'":\n\t' + str(e))
	def unlinkBytecode(self):
		try:
			for method in self.methods:
				if 'ACC_ABSTRACT' not in method.accessFlags:
					method.codeStructure['code'] = classbytecode.unlinkAndCompile(method.codeStructure['code'], self)
		except Exception as e:
			raise Exception('exception ('+str(type(e))+') occured while unlinking bytecode of class file "'+self.filepath+'":\n\t' + str(e))




def openFile(filepath):
	file = ClassFile()
	file.fromFile(filepath)
	return file

