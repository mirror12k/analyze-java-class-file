
import struct


constantTagNames = {
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


class ClassFileConstant(object):
	def __init__(self, tagType):
		self.tagType = tagType
		self.tagName = constantTagNames[tagType]

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
	def __str__(self):
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




class ClassFileObject(object):
	def getAttributeByName(self, name):
		for attribute in self.attributes:
			if attribute.nameIndex.string == name:
				return attribute


class ClassFileField(ClassFileObject):
	def __init__(self, accessFlags, nameIndex, descriptorIndex, attributes):
		self.accessFlags = accessFlags
		self.nameIndex = nameIndex
		self.descriptorIndex = descriptorIndex
		self.attributes = attributes
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
			entry['catch_type'] = classfile.constantFromIndex(entry['catch_type'])
			codeStructure['exception_table'][i] = entry
		data = data[2 + 8 * codeStructure['exception_table_length']:]

		codeStructure['attributes_count'], = struct.unpack('>H', data[:2])
		data = data[2:]
		codeStructure['attributes'] = []
		for i in range(codeStructure['attributes_count']):
			attribute, data, = self.unpackAttribute(data)
			classfile.linkAttribute(attribute)
			codeStructure['attributes'].append(attribute)

		if len(data) > 0:
			raise Exception("invalid data on the end of Code attribute: "+str(data))

		self.codeStructure = codeStructure

	def packCodeAttribute(self, classfile):
		attribute = self.getAttributeByName('Code')
		codeStructure = self.codeStructure
		data = b''

		data += struct.pack('>HHL', codeStructure['max_stack'], codeStructure['max_locals'], codeStructure['code_length'])
		data += codeStructure['code']

		data += struct.pack('>H', codeStructure['exception_table_length'])
		for entry in codeStructure['exception_table']:
			entry['catch_type'] = classfile.constantToIndex(entry['catch_type'])
			data += struct.pack('>HHHH', entry['start_pc'], entry['end_pc'], entry['handler_pc'], entry['catch_type'])

		data += struct.pack('>H', codeStructure['attributes_count'])
		for attribute in codeStructure['attributes']:
			classfile.unlinkAttribute(attribute)
			data += self.packAttribute(attribute)

		attribute.data = data




	def unpackAttribute(self, data):
		attributeNameIndex, attributeLength = struct.unpack('>HI', data[:6])
		attributeData = data[6 : 6 + attributeLength]
		return ClassFileAttribute(attributeNameIndex, attributeData), data[6+attributeLength:]
	def packAttribute(self, attribute):
		data = struct.pack('>HI', attribute.nameIndex, len(attribute.data))
		data += attribute.data
		return data


	def __str__(self):
		return 'ClassFileMethod(accessFlags='+str(self.accessFlags)+\
			',nameIndex='+str(self.nameIndex)+\
			',descriptorIndex='+str(self.descriptorIndex)+\
			',attributes='+str([ str(o) for o in self.attributes ])+\
			',code='+str(self.codeStructure)+')'


class ClassFileAttribute(object):
	def __init__(self, nameIndex, data):
		self.nameIndex = nameIndex
		self.data = data
	def __str__(self):
		return 'ClassFileAttribute(nameIndex='+str(self.nameIndex)+')'





class ClassFile(object):
	def __init__(self, filepath):
		self.filepath = filepath

		self.unpackClassFile()



	def constantFromIndex(self, index, constType='*'):
		if index < 1 or index > len(self.fileStructure['constants']):
			raise Exception('out-of-bounds constant index '+str(index)+' for constType "'+constType+'"')
		const = self.fileStructure['constants'][index - 1]
		if constType != '*' and const.tagName != constType:
			raise Exception('invalid constant type at index '+str(index)+': "'+const.tagName+'" (expected "'+constType+'"')
		return const

	def constantToIndex(self, const, constType='*'):
		if constType != '*' and const.tagName != constType:
			raise Exception('invalid constant type: "'+const.tagName+'" (expected "'+constType+'"')
		index = self.fileStructure['constants'].index(const) + 1
		return index





	def unpackClassFile(self):
		self.handle = open(self.filepath, 'rb')

		data = self.handle.read(10)
		fileStructure = {}
		fileStructure['magic'], fileStructure['version_minor'], fileStructure['version_major'], fileStructure['const_count'] = struct.unpack('>4sHHH', data)
		
		constants = []
		for i in range(1, fileStructure['const_count']):
			const = self.unpackConstant()
			constants.append(const)
			i += 1
			if const.tagName == 'CONSTANT_Long' or const.tagName == 'CONSTANT_Double':
				# longs and doubles take up two constant slots
				# because the guy that designed this format is an idiot
				i += 1
				constants.append(None)
				
		fileStructure['constants'] = constants

		data = self.handle.read(8)
		fileStructure['access_flags'], fileStructure['this_class'], fileStructure['super_class'], fileStructure['interface_count'] = struct.unpack('>HHHH', data)

		fileStructure['interfaces'] = []
		for _ in range(fileStructure['interface_count']):
			data = self.handle.read(2)
			index, = struct.unpack('>H', data)
			fileStructure['interfaces'].append(index)

		data = self.handle.read(2)
		fileStructure['fields_count'], = struct.unpack('>H', data)
		fileStructure['fields'] = [ self.unpackField() for _ in range(fileStructure['fields_count']) ]


		data = self.handle.read(2)
		fileStructure['methods_count'], = struct.unpack('>H', data)
		fileStructure['methods'] = [ self.unpackMethod() for _ in range(fileStructure['methods_count']) ]

		data = self.handle.read(2)
		fileStructure['attributes_count'], = struct.unpack('>H', data)
		fileStructure['attributes'] = [ self.unpackAttribute() for _ in range(fileStructure['attributes_count']) ]


		self.fileStructure = fileStructure
		self.handle.close()

		self.linkClass()

	def linkClass(self):
		flags = []
		code = self.fileStructure['access_flags']
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
		self.fileStructure['access_flags'] = flags

		self.fileStructure['this_class'] = self.constantFromIndex(self.fileStructure['this_class'], 'CONSTANT_Class')
		self.fileStructure['super_class'] = self.constantFromIndex(self.fileStructure['super_class'], 'CONSTANT_Class')

		self.fileStructure['interfaces'] = [ self.constantFromIndex(index, 'CONSTANT_Class') for index in self.fileStructure['interfaces'] ]

		self.linkClassConstants()

		for field in self.fileStructure['fields']:
			self.linkField(field)

		for method in self.fileStructure['methods']:
			self.linkMethod(method)

		for attribute in self.fileStructure['attributes']:
			self.linkAttribute(attribute)

		for method in self.fileStructure['methods']:
			method.unpackCodeAttribute(self)

	def linkField(self, field):
		flags = []
		code = field.accessFlags
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
		field.accessFlags = flags

		field.nameIndex = self.constantFromIndex(field.nameIndex, 'CONSTANT_Utf8')
		field.descriptorIndex = self.constantFromIndex(field.descriptorIndex, 'CONSTANT_Utf8')

		for attribute in field.attributes:
			self.linkAttribute(attribute)

	def linkMethod(self, method):
		flags = []
		code = method.accessFlags
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
		method.accessFlags = flags

		method.nameIndex = self.constantFromIndex(method.nameIndex, 'CONSTANT_Utf8')
		method.descriptorIndex = self.constantFromIndex(method.descriptorIndex, 'CONSTANT_Utf8')

		for attribute in method.attributes:
			self.linkAttribute(attribute)

	def linkAttribute(self, attribute):
		attribute.nameIndex = self.constantFromIndex(attribute.nameIndex, 'CONSTANT_Utf8')

	def linkClassConstants(self):
		consts = self.fileStructure['constants']
		for const in consts:
			const.link(self)

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

	def packClassFile(self):
		self.unlinkClass()

		self.handle = open(self.filepath, 'wb')

		data = struct.pack('>4sHHH', self.fileStructure['magic'], self.fileStructure['version_minor'], self.fileStructure['version_major'], self.fileStructure['const_count'])
		self.handle.write(data)
		
		for const in self.fileStructure['constants']:
			if const is not None:
				self.handle.write(self.packConstant(const))
		
		data = struct.pack('>HHHH', self.fileStructure['access_flags'], self.fileStructure['this_class'], self.fileStructure['super_class'], self.fileStructure['interface_count'])
		self.handle.write(data)

		for interface in self.fileStructure['interfaces']:
			self.handle.write(struct.pack('>H', interface))

		self.handle.write(struct.pack('>H', self.fileStructure['fields_count']))
		for field in self.fileStructure['fields']:
			self.handle.write(self.packField(field))

		self.handle.write(struct.pack('>H', self.fileStructure['methods_count']))
		for method in self.fileStructure['methods']:
			self.handle.write(self.packMethod(method))

		self.handle.write(struct.pack('>H', self.fileStructure['attributes_count']))
		for attribute in self.fileStructure['attributes']:
			self.handle.write(self.packAttribute(attribute))

		self.handle.close()

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



	def unlinkClass(self):

		for method in self.fileStructure['methods']:
			method.packCodeAttribute(self)



		for field in self.fileStructure['fields']:
			self.unlinkField(field)

		for method in self.fileStructure['methods']:
			self.unlinkMethod(method)

		for attribute in self.fileStructure['attributes']:
			self.unlinkAttribute(attribute)


		flags = self.fileStructure['access_flags']
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
		self.fileStructure['access_flags'] = code

		self.fileStructure['this_class'] = self.constantToIndex(self.fileStructure['this_class'], 'CONSTANT_Class')
		self.fileStructure['super_class'] = self.constantToIndex(self.fileStructure['super_class'], 'CONSTANT_Class')

		indexes = []
		for interface in self.fileStructure['interfaces']:
			if interface.tagName != 'CONSTANT_Class':
				raise Exception('invalid constant type for file.interface['+str(index)+']:'+interface.tagName)
			const = self.fileStructure['constants'][index - 1]
			indexes.append(self.fileStructure['constants'].index(interface) + 1)
		self.fileStructure['interfaces'] = indexes

		self.unlinkClassConstants()

	def unlinkField(self, field):
		code = 0
		for flag in field.accessFlags:
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
		field.accessFlags = code
		field.nameIndex = self.constantToIndex(field.nameIndex, 'CONSTANT_Utf8')
		field.descriptorIndex = self.constantToIndex(field.descriptorIndex, 'CONSTANT_Utf8')

		for attribute in field.attributes:
			self.unlinkAttribute(attribute)

	def unlinkMethod(self, method):
		code = 0
		for flag in method.accessFlags:
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
		method.accessFlags = code

		method.nameIndex = self.constantToIndex(method.nameIndex, 'CONSTANT_Utf8')
		method.descriptorIndex = self.constantToIndex(method.descriptorIndex, 'CONSTANT_Utf8')

		for attribute in method.attributes:
			self.unlinkAttribute(attribute)

	def unlinkAttribute(self, attribute):
		attribute.nameIndex = self.constantToIndex(attribute.nameIndex, 'CONSTANT_Utf8')


	def unlinkClassConstants(self):
		consts = self.fileStructure['constants']
		for const in consts:
			const.unlink(self)





def openFile(*args):
	return ClassFile(*args)

