


import classfile


class ClassFileLoader(object):
	def __init__(self, filepath='.'):
		self.filepath = filepath + '/'
		self.filecache = {}
	def loadClassByName(self, name, forceReferesh=False):
		if forceReferesh or name not in self.filecache:
			filepath = self.filepath + name.replace('.', '/') + '.class'
			cf = classfile.openFile(filepath)
			cf.linkClassFile()
			cf.inlineClassFile()
			self.filecache[name] = { 'filepath' : filepath, 'classfile' : cf }
		return self.filecache[name]['classfile']

