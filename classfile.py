
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




class StringConstant(object):
	def __init__(self, string):
		self.string = string
	def __str__(self):
		return "StringConstant('"+self.string+"')"

class ClassConstant(object):
	def __init__(self, className):
		self.className = className
	def __str__(self):
		return "ClassConstant('"+self.className+"')"

class MethodConstant(object):
	def __init__(self, methodName, methodType, methodClass):
		self.methodName = methodName
		self.methodType = methodType
		self.methodClass = methodClass
	def __str__(self):
		return "MethodConstant("+self.methodClass+" -> "+self.methodName+" : "+self.methodType+" )"

class ClassFileField(object):
	def __init__(self, accessFlags, nameIndex, descriptorIndex, attributes):
		self.accessFlags = accessFlags
		self.nameIndex = nameIndex
		self.descriptorIndex = descriptorIndex
		self.attributes = attributes
	def __str__(self):
		return 'ClassFileField(accessFlags='+str(self.accessFlags)+\
			',nameIndex='+str(self.nameIndex)+\
			',descriptorIndex='+str(self.descriptorIndex)+\
			',attributes='+str(self.attributes)+')'

class ClassFileMethod(object):
	def __init__(self, accessFlags, nameIndex, descriptorIndex, attributes):
		self.accessFlags = accessFlags
		self.nameIndex = nameIndex
		self.descriptorIndex = descriptorIndex
		self.attributes = attributes
	def __str__(self):
		return 'ClassFileMethod(accessFlags='+str(self.accessFlags)+\
			',nameIndex='+str(self.nameIndex)+\
			',descriptorIndex='+str(self.descriptorIndex)+\
			',attributes='+str(self.attributes)+')'


class ClassFileAttribute(object):
	def __init__(self, nameIndex, data):
		self.nameIndex = nameIndex
		self.data = data
		# self.tagName = constantTagNames[tagType]
	def __str__(self):
		return 'ClassFileAttribute(nameIndex='+str(self.nameIndex)+')'





class ClassFile(object):
	def __init__(self, filepath):
		self.filepath = filepath

		self.unpackClassFile()

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
		if code & 0x0001:
			flags.append('ACC_PUBLIC')
		if code & 0x0010:
			flags.append('ACC_FINAL')
		if code & 0x0020:
			flags.append('ACC_SUPER')
		if code & 0x0200:
			flags.append('ACC_INTERFACE')
		if code & 0x0400:
			flags.append('ACC_ABSTRACT')
		if code & 0x1000:
			flags.append('ACC_SYNTHETIC')
		if code & 0x2000:
			flags.append('ACC_ANNOTATION')
		if code & 0x4000:
			flags.append('ACC_ENUM')
		self.fileStructure['access_flags'] = flags

		self.fileStructure['this_class'] = self.constantFromIndex(self.fileStructure['this_class'], 'CONSTANT_Class')
		self.fileStructure['super_class'] = self.constantFromIndex(self.fileStructure['super_class'], 'CONSTANT_Class')

		self.fileStructure['interfaces'] = [ self.constantFromIndex(index, 'CONSTANT_Class') for index in self.fileStructure['interfaces'] ]

		self.linkClassConstants()


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

	def linkClassConstants(self):
		consts = self.fileStructure['constants']
		for const in consts:
			if const.tagName == 'CONSTANT_Class':
				const.nameIndex = self.constantFromIndex(const.nameIndex, 'CONSTANT_Utf8')
			elif const.tagName == 'CONSTANT_String':
				const.stringIndex = self.constantFromIndex(const.stringIndex, 'CONSTANT_Utf8')
			elif const.tagName == 'CONSTANT_Methodref' or const.tagName == 'CONSTANT_Fieldref' or const.tagName == 'CONSTANT_InterfaceMethodref':
				const.classIndex = self.constantFromIndex(const.classIndex, 'CONSTANT_Class')
				const.nameAndTypeIndex = self.constantFromIndex(const.nameAndTypeIndex, 'CONSTANT_NameAndType')
			elif const.tagName == 'CONSTANT_NameAndType':
				const.nameIndex = self.constantFromIndex(const.nameIndex, 'CONSTANT_Utf8')
				const.descriptorIndex = self.constantFromIndex(const.descriptorIndex, 'CONSTANT_Utf8')
			elif const.tagName == 'CONSTANT_Utf8' or const.tagName == 'CONSTANT_Integer' or const.tagName == 'CONSTANT_Float'\
				or const.tagName == 'CONSTANT_Long' or const.tagName == 'CONSTANT_Double':
				pass
			else:
				raise Exception ("unknown tag type: ", const.tagName)


	def unlinkClass(self):
		flags = self.fileStructure['access_flags']
		code = 0
		for flag in flags:
			if flag == 'ACC_PUBLIC':
				code |= 0x0001
			elif flag == 'ACC_FINAL':
				code |= 0x0010
			elif flag == 'ACC_SUPER':
				code |= 0x0020
			elif flag == 'ACC_INTERFACE':
				code |= 0x0200
			elif flag == 'ACC_ABSTRACT':
				code |= 0x0400
			elif flag == 'ACC_SYNTHETIC':
				code |= 0x1000
			elif flag == 'ACC_ANNOTATION':
				code |= 0x2000
			elif flag == 'ACC_ENUM':
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

	def unlinkClassConstants(self):
		consts = self.fileStructure['constants']
		for const in consts:
			if const.tagName == 'CONSTANT_Class':
				const.nameIndex = self.constantToIndex(const.nameIndex, 'CONSTANT_Utf8')
			elif const.tagName == 'CONSTANT_String':
				const.stringIndex = self.constantToIndex(const.stringIndex, 'CONSTANT_Utf8')
			elif const.tagName == 'CONSTANT_Methodref' or const.tagName == 'CONSTANT_Fieldref' or const.tagName == 'CONSTANT_InterfaceMethodref':
				const.classIndex = self.constantToIndex(const.classIndex, 'CONSTANT_Class')
				const.nameAndTypeIndex = self.constantToIndex(const.nameAndTypeIndex, 'CONSTANT_NameAndType')
			elif const.tagName == 'CONSTANT_NameAndType':
				const.nameIndex = self.constantToIndex(const.nameIndex, 'CONSTANT_Utf8')
				const.descriptorIndex = self.constantToIndex(const.descriptorIndex, 'CONSTANT_Utf8')
			elif const.tagName == 'CONSTANT_Utf8' or const.tagName == 'CONSTANT_Integer' or const.tagName == 'CONSTANT_Float'\
				or const.tagName == 'CONSTANT_Long' or const.tagName == 'CONSTANT_Double':
				pass
			else:
				raise Exception ("unknown tag type: ", const.tagName)

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




def openFile(*args):
	return ClassFile(*args)

