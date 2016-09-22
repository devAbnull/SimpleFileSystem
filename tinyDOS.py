from volume import *
from entry import *
from directory import *
import readline

class TinyDOS:

	def __init__(self):
		self.volume = None

	def main(self):
		self.input = ''
		while self.input != 'quit':
			self.input = input(' > ')
			try:
				split_input = self.input.split(' ')
				if len(split_input) > 2:
					split_input = [split_input[0], split_input[1], ' '.join(split_input[2:])]
				if split_input[0] == 'format':
					if len(split_input) < 2:
						raise IOError('Not enough arguments passed')
					self.format(split_input[1])
				elif split_input[0] == 'reconnect':
					if len(split_input) < 2:
						raise IOError('Not enough arguments passed')
					self.reconnect(split_input[1])
				elif self.volume == None:
					raise IOError('Please format a new drive or reconnect a drive first.')
				elif split_input[0] == 'ls':
					if len(split_input) < 2:
						self.ls('')
						continue
					self.ls(split_input[1])
				elif split_input[0] == 'mkfile':
					if len(split_input) < 2:
						raise IOError('Not enough arguments passed')
					self.mkfile(split_input[1])
				elif split_input[0] == 'mkdir':
					if len(split_input) < 2:
						raise IOError('Not enough arguments passed')
					self.mkdir(split_input[1])
				elif split_input[0] == 'append':
					if len(split_input) < 3:
						raise IOError('Not enough arguments passed')
					self.append(split_input[1], split_input[2])
				elif split_input[0] == 'print':
					if len(split_input) < 2:
						raise IOError('Not enough arguments passed')
					self.print(split_input[1])
				elif split_input[0] == 'delfile':
					if len(split_input) < 2:
						raise IOError('Not enough arguments passed')
					self.delfile(split_input[1])
				elif split_input[0] == 'deldir':
					if len(split_input) < 2:
						raise IOError('Not enough arguments passed')
					self.deldir(split_input[1])
				elif split_input[0] == 'quit':
					self.quit()
				else:
					print('Command ',split_input[0],'not recognized')
			except (IOError, RuntimeError) as e:
				print('Error: %s' % e)

	def format(self, name):
		if self.volume is not None:
			self.volume.disconnect()
		self.volume = Volume(name)
		self.volume.format()

	def reconnect(self, name):
		if self.volume is not None:
			self.volume.disconnect()
		self.volume = Volume(name)
		self.volume.reconnect()

	def ls(self, path_as_string):
		path = path_as_string.split('/')
		dirs = []
		if len(path) > 0:
			dir_entry = self.find_entry(path)
			dirs = [Directory.create_directory(self.volume.read_block(i), i) for i in dir_entry.get_blocks()]
		else:
			dirs.append(Directory.create_directory(self.volume.read_block(0), 0))
		print('name:     type:  size:')
		for dir in dirs:
			for entry in dir.entries:
				if not entry.name.isspace():
					name = entry.name
					for i in range(0, 10 - len(name)):
						name += ' '
					file_type = entry.file_type
					for i in range(0, 7 - len(file_type)):
						file_type += ' '
					size = entry.length
					print(name + file_type + size)

	def mkfile(self, path_as_string):
		self.mkentry(path_as_string, True)

	def mkdir(self, path_as_string):
		self.mkentry(path_as_string, False)

	def mkentry(self, path_as_string, is_file):
		path = path_as_string.split('/')
		entry = Entry(path[len(path)-1], '0000', ['000' for i in range(0, 12)], is_file, 0)
		parent_path = [path[i] for i in range(0, len(path)-1)]
		if len(parent_path) > 0:
			dir_entry = self.find_entry(parent_path)
			dir_blocks = dir_entry.get_blocks()
			dir = None
			for i in range(0, len(dir_blocks)):
				block = self.volume.read_block(dir_blocks[i])
				dir = Directory.create_directory(block, dir_blocks[i])
				if dir.add_entry(entry):
					self.volume.write_block(dir.read_block, dir.block)
					return
			new_block = self.volume.assign_block(dir_entry)
			entry.read_block = new_block
			dir = Directory(False, [entry], new_block)
			self.volume.write_block(new_block, dir.block)
		else:
			block = self.volume.read_block(0)
			dir = Directory.create_directory(block, 0)
			if dir.add_entry(entry):
				self.volume.write_block(dir.read_block, dir.block)
				return
			else:
				raise IOError('Root directory is full, write failed')

	def append(self, path_as_string, data):
		entry = self.find_entry(path_as_string.split('/'))
		if not entry.is_file:
			raise IOError('Cannot append to a directory')
		entry_contents = []
		for i in entry.get_blocks():
			if i != 0:
				content = self.volume.read_block(i).rstrip()
				if len(content) < 512:
					remainder = 512 - len(content)
					content += data[:remainder]
					entry.increment_length(512 - len(content) - remainder)
					data = data[remainder:]
					for j in range(0, 512 - len(content)):
						content += ' '
					self.volume.write_block(i, content)
		if len(data) > 0:
			data_blocks = [data[i:i+512] for i in range(0, len(data), 512)]
			for i in range(0, len(data_blocks)):
				new_block = self.volume.assign_block(entry)
				entry.increment_length(len(data_blocks[i]))
				for j in range(0, 512 - len(data_blocks[i])):
						data_blocks[i] += ' '
				self.volume.write_block(new_block, data_blocks[i])
		self.volume.update_entry(entry)

	def print(self, path_as_string):
		path = path_as_string.split('/')
		entry = self.find_entry(path)
		entry_content = ''
		for i in entry.get_blocks():
			if i != 0:
				entry_content += self.volume.read_block(i).strip()
		print(entry_content)

	def delfile(self, path_as_string):
		pass

	def deldir(self, path_as_string):
		pass

	def quit(self):
		self.volume.disconnect()

	def find_entry(self, path):
		blocks = [0]
		dir = None
		entry = None
		for i in range(0, len(path)):
			entry = None
			for j in range(0, len(blocks)):
				block = self.volume.read_block(blocks[j])
				dir = Directory.create_directory(block, blocks[j])
				for k in range(0, len(dir.entries)):
					if dir.entries[k].matches(path[i]):
						entry = dir.entries[k]
						blocks = dir.entries[k].get_blocks()
						break
				if entry is not None:
					break
		if entry is None:
			raise IOError('Cannot find specified file/directory')
		return entry


if __name__ == '__main__':
	tinydos = TinyDOS()
	tinydos.main()