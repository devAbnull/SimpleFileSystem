import drive
import array
import os

class TinyDOS:

	def __init__(self):
		self.volume = None

	def main(self):
		pass

	def format(self, name):
		pass

	def reconnect(self, name):
		pass

	def ls(self, path):
		pass

	def mkfile(self, path):
		pass

	def mkdir(self, path):
		pass

	def append(self, path, data):
		pass

	def print(self, path):
		pass

	def delfile(self, path):
		pass

	def deldir(self, path):
		pass

	def quit(self):
		pass

class Volume:

	# [line[i:i+n] for i in range(0, len(line), n)] <= string to array seperated by n characters
	# ''.join(list) <= list to string with '' between elements

	EMPTY_BITMAP = '-' for _ in range(128)

	def __init__(self, name):
		# Initialize block 0 with root directory and block bitmap information
		Volume.EMPTY_BITMAP[0] = '+'

	def format(self):
		pass

class Directory:
	
	def __init__(self, entries=[Entry.FILE_ENTRY for _ in range(0, 8)]):
		self.entries = entries
		for i in range(8 - (len(self.entries) % 8)):
			self.entries.append(Entry.FILE_ENTRY)
		

class Entry:
	DIRECTORY_ENTRY = 'd:         0000:000 000 000 000 000 000 000 000 000 000 000 000 '
	FILE_ENTRY = 'f:         0000:000 000 000 000 000 000 000 000 000 000 000 000 '

	def __init__(self, name, length='0000', blocks=['000' for _ in range(0, 12)], isFile=True):
		# Check input for acceptable formatting
		if len(name) > 8:
			raise IOError('Entry name cannot be longer than 8 characters')
		if ' ' in name:
			raise IOError('Entry name must not contain a space')
		if len(length) != 4 or !length.isnumeric():
			raise RuntimeError('Invalid length syntax passed to entry')
		if len(blocks) != 12:
			raise RuntimeError('Invalid blocks syntax passed to entry')
		for i in range len(blocks):
			if len(blocks[i]) != 3 or !blocks[i].isnumeric():
				raise RuntimeError('Invalid block syntax in block ', i)
		# Create entry
		for i in range(8 - len(name)):
			name += ' '
		self.name = name
		self.length = length
		self.blocks = blocks
		if isFile:
			self.type = 'f:'
		else:
			self.type = 'd:'
		self.entry = self.type + self.name + ' ' + self.length + ':' + ' '.join(self.blocks) + ' '

	def refresh_entry(self):
		self.entry = self.type + self.name + ' ' + self.length + ':' + ' '.join(self.blocks) + ' '

	def get_entry(self):
		return self.entry

	def add_block(self, block):
		if len(block) != 3 or !block.isnumeric():
			raise RuntimeError('Invalid block syntax passed to entry')
		next_block = 0
		for i in range(0, len(self.blocks)):
			if '000' in self.blocks[i]:
				next_block = i
		self.blocks[next_block] = block
		self.refresh_entry()

	def get_blocks(self):
		blocks = []
		for i in range(len(self.blocks)):
			if not '000' in self.blocks[i]:
				blocks.append(int(self.blocks[i]))
		return blocks

	def set_length(self, length):
		if len(block) != 4 or !block.isnumeric():
			raise RuntimeError('Invalid length syntax passed to entry')
		self.length = length
		self.refresh_entry()

if __name__ == '__main__':
	pass