
import struct



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
		return header



def openFile(*args):
	return ClassFile(*args)

