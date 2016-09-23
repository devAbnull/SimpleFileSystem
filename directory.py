from entry import *

class Directory:
	
	def __init__(self, is_root, entries, read_block):
		self.is_root = is_root
		self.entries = entries[:]
		self.read_block = read_block
		self.block = ''
		total_entries = 0
		if self.is_root:
			total_entries = 6
		else:
			total_entries = 8
		for i in range(len(self.entries), total_entries):
			new_entry = Entry('', '0000', ['000' for i in range(0, 12)], True, read_block)
			self.entries.append(new_entry)
		for i in range(0, total_entries):
			self.block += (self.entries[i].entry)

	@staticmethod
	def create_directory(string, read_block):
		string_entries = [string[i:i+64] for i in range(0, len(string), 64)]
		entries = []
		for i in range(0, len(string_entries)):
			entries.append(Entry.create_entry(string_entries[i], read_block))
		return Directory((len(string_entries) == 6), entries, read_block)

	def add_entry(self, entry):
		for i in range(0, len(self.entries)):
			if self.entries[i].entry == Entry.FILE_ENTRY:
				self.entries[i] = entry
				self.entries[i].read_block = self.read_block
				self.refresh_block()
				return True
		return False
	
	def update_entry(self, name, entry):
		for i in range(0, len(self.entries)):
			if self.entries[i].matches(name):
				self.entries[i] = entry
				self.entries[i].read_block = self.read_block
				self.entries[i].refresh_entry()
				self.refresh_block()
				return True
		return False

	def refresh_block(self):
		self.block = ''
		for i in range(0, len(self.entries)):
			self.block += (self.entries[i].entry)