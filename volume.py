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
		root = Directory(is_root=True)
		root_block = root.blocks[0]
		self.drive.write_block(0, ''.join(self.bitmap) + root_block)

	def reconnect(self):
		self.drive.reconnect()
	
	def disconnect(self):
		self.drive.disconnect()

	def create_file(self, n, name):
		block = self.read_block(n)
		dir = Directory.create_directory(block)
		created_entry = False
		for i in range(0, len(dir.entries)):
			if dir.entries[i].is_empty():
				created_entry = True
				dir.entries[i] = Entry(name=name)
				break
		if not created_entry:
			return False
		block = ''
		for i in range(0, len(dir.entries)):
			block += dir.entries[i].entry
		if n == 0:
			self.drive.write_block(0, ''.join(self.bitmap) + block)
		else:
			self.drive.write_block(n, block)
		return True
	
	def write_block(self, n, data):
		self.drive.write_block(n, data)
		
	def read_block(self, n):
		block = self.drive.read_block(n)
		if n == 0:
			return block[128:]
		return block
