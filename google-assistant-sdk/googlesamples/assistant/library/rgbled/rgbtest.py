import rgb

rgb.setup(11,9,10,100)

while True:
	r = input("Red Value: ")
	g = input("Green Value: ")
	b = input("Blue Value: ")
	rgb.changeto(r,g,b,0.008)