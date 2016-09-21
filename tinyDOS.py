from volume import *
from entry import *
from directory import *
import readline

class TinyDOS:

	def __init__(self):
		self.volume = None

	def main(self):
		self.input = input(' > ')
		while self.input != 'quit':
			split_input = self.input.split(' ')
			if split_input[0] == 'format':
				self.format(split_input[1])
			elif split_input[0] == 'reconnect':
				self.reconnect(split_input[1])
			elif split_input[0] == 'ls':
				self.ls(split_input[1])
			elif split_input[0] == 'mkfile':
				self.mkfile(split_input[1])
			elif split_input[0] == 'mkdir':
				self.mkdir(split_input[1])
			elif split_input[0] == 'append':
				self.append(split_input[1])
			elif split_input[0] == 'print':
				self.print(split_input[1])
			elif split_input[0] == 'delfile':
				self.delfile(split_input[1])
			elif split_input[0] == 'deldir':
				self.deldir(split_input[1])
			self.input = input(' > ')

	def format(self, name):
		self.volume = Volume(name)
		self.volume.format()

	def reconnect(self, name):
		pass

	def ls(self, path_as_string):
		pass

	def mkfile(self, path_as_string):
		path = path_as_string.split('/')
		block_num = self.find_block(path)
		file_name = path[len(path)-1]
		if block_num == 0:
			self.volume.create_file(0, file_name)
		else:
			dir_entry = Entry()
			block = self.volume.read_block(blocks_num)
			dir = Directory.create_directory(block)
			for i in range(0, len(dir.entries)):
				if dir.entries[i].is_entry(path[len(path) - 1]):
					dir_entry = dir.entries[i]
					break
			file_created = False
			empty_block = 13
			for i in range(0, len(dir_entry.blocks)):
				if dir_entry.blocks[i] == '000':
					if empty_block == 13:
						empty_block = i
					continue
				if volume.create_file(int(dir_entry.blocks[i]), file_name):
					file_created = True
					break
			if not file_created:
				if empty_block == 13:
					raise IOError('Directory does not have any more available space')
				# Assign block to dir
				self.volume.create_file(empty_block, file_name)


	def mkdir(self, path_as_string):
		pass

	def append(self, path_as_string, data):
		pass

	def print(self, path_as_string):
		pass

	def delfile(self, path_as_string):
		pass

	def deldir(self, path_as_string):
		pass

	def quit(self):
		pass

	def seperate_block(self, block):
		entries = []
		for i in range(0, len(block), 64):
			entries.append(block[i:i+64])
		return entries

	def find_block(self, path):
		if len(path) > 1:
			blocks = [0]
			for i in range (0, len(path) - 1):
				for j in range(0, len(blocks)):
					dir_found = False
					block = self.volume.read_block(blocks[j])
					dir = Directory.create_directory(block)
					for k in range(0, len(dir.entries)):
						if dir.entries[k].is_entry(path[i]):
							if i == (len(path) - 1):
								return blocks[j]
							blocks = []
							for l in range(0, len(dir.entries)):
								blocks.append(int(dir.entries[l]))
							dir_found = True
						if dir_found:
							break
					if dir_found:
						break
		else:
			return 0


if __name__ == '__main__':
	tinydos = TinyDOS()
	tinydos.main()