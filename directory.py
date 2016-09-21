from entry import *

class Directory:
	
	def __init__(self, is_root=False, entries=[Entry() for i in range(0,6)]):
		self.entries = entries
		self.blocks = list()
		if is_root:
			self.total_entries = 6
			for i in range(len(self.entries), 6):
				self.entries.append(Entry.FILE_ENTRY)
			self.blocks.append('')
			for i in range(0, 6):
				self.blocks[0] += (self.entries[i].entry)
		else:
			self.total_entries = 8
			for i in range(8 - (len(self.entries) % 8)):
				self.entries.append(Entry.FILE_ENTRY)
			for i in range(0, len(self.entries)/8 - 1):
				if i > len(self.blocks):
					self.blocks.append('')
				else:
					self.blocks[i] = ''
				for j in range(i*8, i*8 + 8):
					self.blocks[i] += (self.entries[j].entry)
	
	@staticmethod
	def create_directory(string):
		string_entries = [string[i:i+64] for i in range(0, len(string), 64)]
		entries = []
		for i in range(0, len(string_entries)):
			entries.append(Entry.create_entry(string_entries[i]))
		return Directory(is_root=(len(string_entries) == 6), entries=entries)

	def add_entry(self, entry):
		for i in self.entries:
			if self.entries[i].get_entry() == Entry.FILE_ENTRY:
				self.entries[i] = entry
				self.refresh_blocks()
				return
		self.entries.append(entry)
		for i in range(len(self.entries), len(self.entries)+7):
				self.entries.append(Entry.FILE_ENTRY)
		self.refresh_blocks()

	def refresh_blocks(self):
		if is_root:
			self.blocks[0] = ''
			for i in range(0, 6):
				self.blocks[0].append(self.entries[i].get_entry)
		else:
			for i in range(0, len(self.entries)/8):
				self.blocks[i] = ''
				for j in range(i*8, i*8 + 8):
					self.blocks[i].append(self.entries[j].get_entry)