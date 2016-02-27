
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
		s = 'ClassFileConstant<'+self.tagName+'>('
		if self.nameIndex is not None:
			s += 'nameIndex=' + str(self.nameIndex) + ','
		elif self.descriptorIndex is not None:
			s += 'descriptorIndex=' + str(self.descriptorIndex) + ','
		elif self.classIndex is not None:
			s += 'classIndex=' + str(self.classIndex) + ','
		elif self.nameAndTypeIndex is not None:
			s += 'nameAndTypeIndex=' + str(self.nameAndTypeIndex) + ','
		elif self.stringIndex is not None:
			s += 'stringIndex=' + str(self.stringIndex) + ','
		elif self.value is not None:
			s += 'value=' + str(self.value) + ','
		elif self.string is not None:
			s += 'string=' + str(self.string) + ','
		elif self.referenceKind is not None:
			s += 'referenceKind=' + str(self.referenceKind) + ','
		elif self.referenceIndex is not None:
			s += 'referenceIndex=' + str(self.referenceIndex) + ','
		s += ')'
		return s


class ClassFile(object):
	def __init__(self, filepath, mode='rb'):
		self.filepath = filepath
		self.mode = mode

		self.handle = open(self.filepath, self.mode)
		self.parse()
	def parse(self):
		header = self.unpackHeader()
		self.header = header
	def unpackHeader(self):
		data = self.handle.read(10)
		header = {}
		header['magic'], header['versionMajor'], header['versionMinor'], header['constCount'] = struct.unpack('>4sHHH', data)
		
		i = 1
		constants = []
		while i < header['constCount']:
			const = self.unpackConstant()
			if const.tagName == 'CONSTANT_Long' or const.tagName == 'CONSTANT_Double':
				# longs and doubles take up two constant slots
				# because the guy that designed this format is an idiot
				i += 1
			constants.append(const)
			i += 1
		header['constants'] = constants
		return header
	def unpackConstant(self):
		data = self.handle.read(1)
		tagType, = struct.unpack('B', data)
		const = ClassFileConstant(tagType)

		# unpack some more data for the constant
		if const.tagName == 'CONSTANT_Class':
			data = self.handle.read(2)
			nameIndex, = struct.unpack('>H', data)
			const.nameIndex = nameIndex
		elif const.tagName == 'CONSTANT_String':
			data = self.handle.read(2)
			stringIndex, = struct.unpack('>H', data)
			const.stringIndex = stringIndex
		elif const.tagName == 'CONSTANT_Utf8':
			data = self.handle.read(2)
			length, = struct.unpack('>H', data)
			data = self.handle.read(length)
			const.string = data.decode('utf8')
		elif const.tagName == 'CONSTANT_Integer':
			data = self.handle.read(4)
			value, = struct.unpack('>i', data)
			const.value = value
		elif const.tagName == 'CONSTANT_Float':
			data = self.handle.read(4)
			value, = struct.unpack('>f', data)
			const.value = value
		elif const.tagName == 'CONSTANT_Long':
			data = self.handle.read(8)
			value, = struct.unpack('>q', data)
			const.value = value
		elif const.tagName == 'CONSTANT_Double':
			data = self.handle.read(8)
			value, = struct.unpack('>d', data)
			const.value = value
		elif const.tagName == 'CONSTANT_Fieldref' or const.tagName == 'CONSTANT_Methodref' or const.tagName == 'CONSTANT_InterfaceMethodref':
			data = self.handle.read(4)
			classIndex, nameAndTypeIndex, = struct.unpack('>HH', data)
			const.classIndex = classIndex
			const.nameAndTypeIndex = nameAndTypeIndex
		elif const.tagName == 'CONSTANT_NameAndType':
			data = self.handle.read(4)
			nameIndex, descriptorIndex, = struct.unpack('>HH', data)
			const.nameIndex = nameIndex
			const.descriptorIndex = descriptorIndex
		elif const.tagName == 'CONSTANT_MethodHandle':
			data = self.handle.read(3)
			referenceKind, referenceIndex, = struct.unpack('>BH', data)
			const.referenceKind = referenceKind
			const.referenceIndex = referenceIndex
		elif const.tagName == 'CONSTANT_MethodType':
			data = self.handle.read(2)
			descriptorIndex, = struct.unpack('>H', data)
			const.descriptorIndex = descriptorIndex
		elif const.tagName == 'CONSTANT_InvokeDynamic':
			data = self.handle.read(4)
			bootstrapIndex, nameAndTypeIndex, = struct.unpack('>HH', data)
			const.bootstrapIndex = bootstrapIndex
			const.nameAndTypeIndex = nameAndTypeIndex

		return const


def openFile(*args):
	return ClassFile(*args)

