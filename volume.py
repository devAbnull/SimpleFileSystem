from drive import *
from entry import *
from directory import *

class Volume:

	# [line[i:i+n] for i in range(0, len(line), n)] <= string to array seperated by n characters
	# ''.join(list) <= list to string with '' between elements

	EMPTY_BITMAP = ['-'] * 128

	def __init__(self, name):
		# Initialize block 0 with root directory and block bitmap information
		self.bitmap = Volume.EMPTY_BITMAP
		self.bitmap[0] = '+'
		self.drive = Drive(name)

	def format(self):
		self.drive.format()
		root = Directory(True, [], 0)
		self.write_block(0, root.block)

	def reconnect(self):
		self.drive.reconnect()
		root = self.drive.read_block(0)
		bitmap_string = root[:128]
		self.bitmap = list(bitmap_string)

	def disconnect(self):
		if self.drive.file is None:
			return
		self.drive.disconnect()

	def assign_block(self, entry):
		for i in range(1, len(self.bitmap)):
			if self.bitmap[i] == '-':
				self.bitmap[i] = '+'
				entry.add_block(i)
				self.update_entry(entry.name, entry)
				self.update_bitmap()
				return i
		raise IOError('Cannot allocate more memory to specified file/directory')

	def update_entry(self, name, entry):
		block = self.read_block(entry.read_block)
		dir = Directory.create_directory(block, entry.read_block)
		dir.update_entry(name, entry)
		self.write_block(entry.read_block, dir.block)

	def update_bitmap(self):
		root_block = self.read_block(0)
		self.drive.write_block(0, ''.join(self.bitmap) + root_block)

	def write_block(self, n, data):
		if n == 0:
			self.drive.write_block(0, ''.join(self.bitmap) + data)
			return
		self.drive.write_block(n, data)
		
	def read_block(self, n):
		block = self.drive.read_block(n)
		if n == 0:
			return block[128:]
		return block
