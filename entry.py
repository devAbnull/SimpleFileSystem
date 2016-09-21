# One entry is 64 bytes
class Entry:
	DIRECTORY_ENTRY = 'd:         0000:000 000 000 000 000 000 000 000 000 000 000 000 '
	FILE_ENTRY = 'f:         0000:000 000 000 000 000 000 000 000 000 000 000 000 '

	def __init__(self, name='', length='0000', blocks=['000' for _ in range(0, 12)], is_file=True):
		# Check input for acceptable formatting
		if len(name) > 8:
			raise IOError(('Entry name cannot be longer than 8 characters', name, len(name)))
		if ' ' in name and not name.isspace():
			raise IOError('Entry name must not contain a space')
		if len(length) != 4 or not length.isnumeric():
			raise RuntimeError('Invalid length syntax passed to entry')
		if len(blocks) != 12:
			raise RuntimeError('Invalid blocks syntax passed to entry')
		for i in range(len(blocks)):
			if len(blocks[i]) != 3 or not blocks[i].isnumeric():
				raise RuntimeError('Invalid block syntax in block ', i)
		# Create entry
		for i in range(0, 8 - len(name)):
			name += ' '
		self.name = name
		self.length = length
		self.blocks = blocks
		if is_file:
			self.file_type = 'f:'
		else:
			self.file_type = 'd:'
		self.entry = self.file_type + self.name + ' ' + self.length + ':' + ' '.join(self.blocks) + ' '

	@staticmethod
	def create_entry(string):
		file_type = string[:2]
		if file_type != 'f:' and file_type != 'd:':
			raise RuntimeError('Invalid file type used to create entry', file_type)
		is_file = True
		if file_type == 'd:':
			is_file = False
		name = string[2:10]
		length = string[11:15]
		blocks = string[16:63].split(' ')
		return Entry(name=name,length=length,blocks=blocks,is_file=is_file)

	def refresh_entry(self):
		self.entry = self.file_type + self.name + ' ' + self.length + ':' + ' '.join(self.blocks) + ' '

	def add_block(self, block):
		if len(block) != 3 or not block.isnumeric():
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
		if len(block) != 4 or not block.isnumeric():
			raise RuntimeError('Invalid length syntax passed to entry')
		self.length = length
		self.refresh_entry()

	def is_empty(self):
		return self.name.isspace()

	def is_entry(self, name):
		return self.name == name