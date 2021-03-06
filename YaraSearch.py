# Yara search on the current file and create bookmarks and EOL comments for findings.
#@author Thomas Roth code@stacksmashing.net
#@category Search.YARA
#@keybinding
#@menupath Search.YARA search
#@toolbar

import os
import subprocess
import tempfile
import os
import csv
from ghidra.program.model.listing import CodeUnit

def add_bookmark_comment(addr, text):
	cu = currentProgram.getListing().getCodeUnitAt(addr)
	createBookmark(addr, "yara", text)
	cu.setComment(CodeUnit.EOL_COMMENT, text)

file_location = currentProgram.getDomainFile().getMetadata()["Executable Location"]

try:
	rule_location = askFile("Select YARA rule", "Search").getPath()
	current_rule = None
	output = subprocess.check_output(["yara", "--print-string-length", rule_location, file_location], stderr=None)
	for line in output.splitlines():
		if line.startswith("0x"):
			if current_rule:
				addr_int = int(line.split(":")[0][2:], 16)
				addr = currentProgram.minAddress.add(addr_int)
				add_bookmark_comment(addr, current_rule)
		else:
			print(line)
			current_rule = line.split(" ")[0]

except Exception as e:
	print("Failed")
	print(e)

