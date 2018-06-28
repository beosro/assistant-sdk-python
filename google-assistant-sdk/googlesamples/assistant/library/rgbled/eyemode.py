import rgb

def changemode(m):
	file = open("mode.txt","w")
	mode = str(m)
	file.write(mode)
	file.close
