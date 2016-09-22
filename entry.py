# One entry is 64 bytes
class Entry:
	DIRECTORY_ENTRY = 'd:         0000:000 000 000 000 000 000 000 000 000 000 000 000 '
	FILE_ENTRY = 'f:         0000:000 000 000 000 000 000 000 000 000 000 000 000 '

	def __init__(self, name, length, blocks, is_file, read_block):
		# Check input for acceptable formatting
		if len(name) > 8:
			raise IOError(('Entry name cannot be longer than 8 characters', name, len(name)))
		for i in range(0, len(name)):
			if name[i].isspace():
				if not name[i:].isspace():
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
		self.is_file = is_file
		self.name = name
		self.length = length
		self.blocks = blocks[:]
		self.read_block = read_block
		if is_file:
			self.file_type = 'f:'
		else:
			self.file_type = 'd:'
		self.entry = self.file_type + self.name + ' ' + self.length + ':' + ' '.join(self.blocks) + ' '

	@staticmethod
	def create_entry(string, read_block):
		file_type = string[:2]
		if file_type != 'f:' and file_type != 'd:':
			raise RuntimeError('Invalid file type used to create entry', file_type)
		is_file = True
		if file_type == 'd:':
			is_file = False
		name = string[2:10]
		length = string[11:15]
		blocks = string[16:63].split(' ')
		return Entry(name, length, blocks, is_file, read_block)

	def refresh_entry(self):
		self.entry = self.file_type + self.name + ' ' + self.length + ':' + ' '.join(self.blocks) + ' '

	def add_block(self, block_int):
		if block_int < 1 or block_int > 127:
			raise RuntimeError('Invalid block number passed to entry')
		block = str(block_int)
		for i in range(0, 3 - len(block)):
			block = '0' + block
		next_block = 13
		for i in range(0, len(self.blocks)):
			if self.blocks[i] == '000':
				next_block = i
				break
		if next_block == 13:
			raise RuntimeError('File/Directory is full')
		self.blocks[next_block] = block
		if not self.is_file:
			self.increment_length(512)
		self.refresh_entry()

	def get_blocks(self):
		blocks = []
		for i in range(len(self.blocks)):
			n = int(self.blocks[i])
			if n != 0:
				blocks.append(n)
		return blocks

	def set_length(self, length):
		if len(block) != 4 or not block.isnumeric():
			raise RuntimeError('Invalid length syntax passed to entry')
		self.length = length
		self.refresh_entry()

	def increment_length(self, increment):
		length_int = int(self.length)
		length_int += increment
		self.length = str(length_int)
		for i in range(len(self.length), 4):
			self.length = '0' + self.length

	def matches(self, name):
		return self.name.strip() == name.strip()