#Inner Config
led1=11
led2=13
led3=15
button1=17
trigger1=19
trigger2=21
#Instructions
#mCode and mLetter use the same call to convert to each other. ex: "e"="." e=mLetter[5] and mCode[5]=.
#conf1 -- Choose whether to encrypt text or decrypt morse
#conf2 -- decide whether to input a sentance or to grap from a file
#conf3 -- choose if to output results to a file
#conf4 -- Decide if to send output resulting morse to the GPIO LEDs
conf4="f"
from system import clear
#variables/tables
mLetter = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ",", ".", "?", "/", "@", "=", ":", "'", "(", ")", "-", "+", " "]
mCode = [".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", ".---", "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", ".-.", "...", "-", "..-", "...-", ".--", "-..-", "-.--", "--..", "-----", ".----", "..---", "...--", "....-", ".....", "-....", "--...", "---..", "----.", "--..--", "-.-.-.", "..--..", "-..-.", ".--.-.", "-...-", "---...", ".----.", "-.--.", "-.--.-", "-....-", ".-.-.", "_"]
def txt2mrs(text):
	text = text.lower()	
	for x in range (0, len(text)):
		for y in range (0, 38):
			if text[x] == mLetter[y]:
				print mCode[y],
				if conf3=="t":
					open(outFile+".txt", "w").write(mCode[y]+" ")
				if conf4=="t":
					gpio.setmode(gpio.BOARD)
					gpio.setup(led1, gpio.OUT)
					gpio.setup(led2, gpio.OUT)
					gpio.setup(led3, gpio.OUT)
					for z in range (0, len(mcode[y])):
						if mcode[y][z]==".":
							gpio.output(11, True)
							gpio.output(13, True)
							gpio.output(15, True)
							sleep(0.25)
						elif mcode[y][z]=="-":
							gpio.output(11, True)
							gpio.output(13, True)
							gpio.output(15, True)
							sleep(0.5)
						gpio.output(11, False)
						gpio.output(13, False)
						gpio.output(15, False)
						sleep(1)
					gpio.cleanup()
def mrs2txt(text):
	text=text.split(" ")
	for x in range (0, len(text)):
		for y in range (0, 38):
			if text[x] == mCode[y]:
				print mLetter[y],
				if conf3=="t":
					open(outFile+".txt", "w").write(mLetter[y]+" ")
def inMorse():
	print "Hold Trigger1 to start reading, release when done with message."
	print "Hold Trigger2 to start a block for decrypting characters"
	print "Press/Hold Button1 to input ./-"
	gpio.setmode(gpio.BOARD)
#	gpio.setup(trigger1, gpio.IN)
#	gpio.setup(trigger2, gpio.IN)
#	gpio.setup(button1, gpio.IN)
#	mPhrase=[]
#	run=True
#	while run:
#		if gpio.input(trigger1):
#			while gpio.input(trigger1):
#				while gpio.input(trigger2):
#					clock=0
#					mChar=[]
#					while gpio.input(button1):
#						sleep(0.1)
#						clock=+1
#					if (clock>0 and clock<5):
#						mChar.append(".")
#					elif clock<5:
#						mChar.append("-")
#					clock=0
#				mPhrase.append(str(''.join(mChar[:])))
#				del mChar[:]
#			return str(' '.join(mPhrase[:]))
#			run=False
#screen
run=True
while run:
	clear()
	print "----------------------------------------------------------------"
	print "                   Morse Code Transcriber"
	print "----------------------------------------------------------------"
	print "\n\n\n\n"
	conf1 = input("Which Input Mode: 1) text 2) morse 3) exit: ")
	if conf1==3:
		break
	conf2 = raw_input("Input from file: [t/f] lowercase: ").lower
	conf3=raw_input("Output to file? [t/f]: ").lower
	if conf3=="t":
			outFile=raw_input("Type name of output file: (no .txt) ")
	conf4=raw_input("Use GPIO [t/f]: ").lower
	if conf4=="t":
		try:
			import RPi.GPIO as gpio
			from time import sleep
		except:
			print "waiting on GPIO API"
			conf4="f"
	if conf1==1:
		if conf2=="t":
			dir=raw_input("Set Directory: ")
			termIn=open(dir, "r").read().lower()
		elif conf2=="f":
			termIn = raw_input("Enter Message to Encrypt: ")
		txt2mrs(termIn)
	elif conf1==2:
		if conf2=="t":
			dir=raw_input("Set Directory: ")
			termIn=open(dir, "r").read()
#		elif conf2=="f" and conf4=="t":
#			termin=inMorse()
		elif conf2=="f":
			termIn = raw_input("Enter Code to Decrypt: ")
		mrs2txt(termIn)
	cont=raw_input("Run again? [t/f]: ").lower
	if cont=="t":
		run=True
	else:
		run=False
		print "Goodbye"