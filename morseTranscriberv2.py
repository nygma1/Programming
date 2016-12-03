#Instructions
#mCode and mLetter use the same call to convert to each other. ex: "e"="." e=mLetter[5] and mCode[5]=.
#conf1 -- Choose whether to encrypt text or decrypt morse
#conf2 -- decide whether to input a sentance or to grap from a file
#conf3 -- choose if to output results to a file
#conf4 -- Decide if to send output resulting morse to the GPIO LEDs

#variables/tables
mLetter = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ",", ".", "?", "/", "@", "=", ":", "'", "(", ")", "-", "+"]
mCode = [".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", ".---", "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", ".-.", "...", "-", "..-", "...-", ".--", "-..-", "-.--", "--..", "-----", ".----", "..---", "...--", "....-", ".....", "-....", "--...", "---..", "----.", "--..--", "-.-.-.", "..--..", "-..-.", ".--.-.", "-...-", "---...", ".----.", "-.--.", "-.--.-", "-....-", ".-.-."]
def txt2mrs(text):
	text = text.lower()
	conf4=raw_input("Use GPIO? [t/f]: ")
	gpo=conf4
	if gpo=="t":
		try:
			import RPi.GPIO as gpio
			from time import sleep
		except:
			print "waiting on GPIO API"
			gpo="f"
	for x in range (0, len(text)):
		for y in range (0, 38):
			if text[x] == mLetter[y]:
				print mCode[y],
				if conf3=="t":
					open(outFile+".txt", "w").write(mCode[y]+" ")
				if gpo=="t":
					gpio.setmode(gpio.BOARD)
					gpio.setup(11, gpio.OUT)
					gpio.setup(13, gpio.OUT)
					gpio.setup(15, gpio.OUT)
					for z in range (0, len(mcode[y])):
						if mcode[y][z]==".":
							gpio.output(11, True)
							gpio.output(13, True)
							gpio.output(15, True)
							sleep(1)
							gpio.output(11, False)
							gpio.output(13, False)
							gpio.output(15, False)
							sleep(0.5)
						elif mcode[y][z]=="-":
							gpio.output(11, True)
							gpio.output(13, True)
							gpio.output(15, True)
							sleep(2)
							gpio.output(11, False)
							gpio.output(13, False)
							gpio.output(15, False)
							sleep(0.5)
					gpio.cleanup()
def mrs2txt(text):
	text=text.split(" ")
	for x in range (0, len(text)):
		for y in range (0, 38):
			if text[x] == mCode[y]:
				print mLetter[y],
				if conf3=="t":
					open(outFile+".txt", "w").write(mLetter[y]+" ")
	
#screen
print "----------------------------------------------------------------"
print "                   Morse Code Transcriber"
print "----------------------------------------------------------------"
print "\n\n\n\n"
conf1 = raw_input("Which Input Mode: 1) text 2) morse: ")
conf2 = raw_input("Input from file: [t/f] lowercase: ")
conf3=raw_input("Output to file? [t/f]: ")
if conf3=="t":
		outFile=raw_input("Type name of output file: (no .txt) ")
if conf1=="1":
	if conf2=="t":
		dir=raw_input("Set Directory: ")
		termIn=open(dir, "r").read().lower()
	elif conf2=="f":
		termIn = raw_input("Enter Message to Encrypt: ")
	txt2mrs(termIn)
elif conf1=="2":
	if conf2=="t":
		dir=raw_input("Set Directory: ")
		termIn=open(dir, "r").read()
	elif conf2=="f":
		termIn = raw_input("Enter Code to Decrypt: ")
	mrs2txt(termIn)
