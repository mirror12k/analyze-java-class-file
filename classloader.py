


import shutil

import classfile
from java_code_tools import *


class ClassFileLoader(object):
	def __init__(self, filepath='.', backupOnWrite=True):
		self.filepath = filepath + '/'
		self.filecache = {}
		self.backupOnWrite = backupOnWrite
	def setFilepath(self, filepath):
		self.filepath = filepath + '/'
	def verifyClassname(self, classname, file):
		if classNameToCode(file.this_class) == classname:
			return
		else:
			raise Exception('invalid classfile ['+classNameToCode(file.this_class)+'] loaded by classname "'+classname+'"')
	def loadClassByName(self, name, forceReferesh=False):
		if forceReferesh or name not in self.filecache:
			filepath = self.filepath + name.replace('.', '/') + '.class'
			cf = classfile.openFile(filepath)
			cf.linkClassFile()
			cf.inlineClassFile()

			self.verifyClassname(name, cf)
			self.filecache[name] = { 'filepath' : filepath, 'classfile' : cf }
		return self.filecache[name]['classfile']
	def loadClassByPath(self, filepath):
		cf = classfile.openFile(self.filepath + filepath)
		cf.linkClassFile()
		cf.inlineClassFile()

		classname = classNameToCode(cf.this_class)
		self.filecache[classname] = { 'filepath' : filepath, 'classfile' : cf }
		return self.filecache[classname]['classfile']
	def loadClass(self, classpath):
		if '/' in classpath or classpath.endswith('.class'):
			return self.loadClassByPath(classpath)
		else:
			return self.loadClassByName(classpath)
	def storeClass(self, file):
		if self.backupOnWrite:
			classname = classNameToCode(file.this_class)
			filepath = self.filecache[classname]['filepath']
			shutil.move(filepath, filepath+'.bak')
		file.uninlineClassFile()
		file.unlinkClassFile()
		file.toFile()


