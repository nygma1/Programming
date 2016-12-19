#Inner Config
led1=11		#parts made in a variable as a way of config incase you have that hardware, but on a different pin
led2=13
led3=15
button1=12
trigger1=14
trigger2=16
#Instructions
#mCode and mLetter use the same call to convert to each other. ex: "e"="." e=mLetter[5] and mCode[5]=.
#conf1 # Choose whether to encrypt text or decrypt morse
conf2=False # decide whether to input a sentance or to grap from a file
conf3=False # choose if to output results to a file
conf4=False # Decide if to send output resulting morse to the GPIO LEDs

#variables/tables
inpLetter={'a':'.-','b':'-...','c':'-.-.','d':'-..','e':'.','f':'..-.','g':'--.','h':'....','i':'..','j':'.---','k':'-.-','l':'.-..','m':'--','n':'-.','o':'---','p':'.--.','q':'--.-','r':'.-.','s':'...','t':'-','u':'..-','v':'...-','w':'.--','x':'-..-','y':'-.--','z':'--..','1':'.----','2':'..---','3':'...--','4':'....-','5':'.....','6':'-....','7':'--...','8':'---..','9':'----.','0':'-----','.':'.-.-.-','?':'..--..','.':'.-.-.-',',':'--..--',':':'---...','?':'..--..',"'":'.----.','-':'-....-','/':'-..-.','@':'.--.-.','=':'-...-','(':'-.--.',')':'-.--.-','+':'.-.-.',' ':'_'}	#this table made by Joe Fields
inpMorse={}
for x in inpLetter: inpMorse[inpLetter[x]]=x #this effectively reverses the previous table
def txt2mrs(text):
	text=str(text.lower()) #security filter to reduce crash rates
	outMrs=[]
	for x in text:
		if x in inpLetter: outMrs.append(inpLetter[x])	#a filter to reduce errors. it first checks each character on whether it is in the dictionary. if the character doesnt exist (like '_') it'll skip adding it to the output, otherwise itll send to output
	outMrs=str(' '.join(x for x in outMrs))
	if conf3: open(outFile, "w").write(outMrs)	#if config 3 was turned on, itll also write the code to a new file of your specification
#	if conf4:
#		gpio.setmode(gpio.BOARD)
#		gpio.setup(led1, gpio.OUT)
#		if led2!=nil: gpio.setup(led2, gpio.OUT)
#		if led3!=nil: gpio.setup(led3, gpio.OUT)
#		for x in outMrs:
#			if x==".":
#				gpio.output(13, True)
#				gpio.output(15, True)
#				sleep(0.25)
#			elif x=="-":
#				gpio.output(11, True)
#				gpio.output(13, True)
#				gpio.output(15, True)
#				sleep(0.5)
#			elif x="_":
#				gpio.output(11, False)
#				gpio.output(13, False)
#				gpio.output(15, False)
#				sleep(1)
#			gpio.output(11, False)
#			gpio.output(13, False)
#			gpio.output(15, False)
#			sleep(1)
#		gpio.cleanup()
	return outMrs	#replaced print system with return statements and compiling the whole list to one string
def mrs2txt(text):
	text=text.split(" ")	#splits groups of morse to be read as individual characters
	outTxt=[]
	for x in text:
		if x in inpMorse: outTxt.append(inpMorse[x])	#same filter as text
	outTxt=str(''.join(x for x in outTxt))	#thanks to this, theres no more spaces in between letters, now allowing perfects sentances to be transcribed without any manual work
	if conf3: open(outFile, "w").write(outTxt)	#same as text
	return outTxt
def inMorse():	#this function makes a special text that inputs from the gpio, and outputs a morse string
	print "Hold Trigger1 to start reading, release when done with message."
	print "Hold Trigger2 to start a block for decrypting characters"
	print "Press/Hold Button1 to input ./- hashtags will help you see what you input"
#	gpio.setmode(gpio.BOARD)
#	gpio.setup(trigger1, gpio.IN)
#	gpio.setup(trigger2, gpio.IN)
#	gpio.setup(button1, gpio.IN)
#	mPhrase=[]
#	while True:	#it has a run here to wait for the user to hold trigger1 and start process. without it, if youre not fast enough, itll end before you even start
#		if gpio.input(trigger1):	#this is how the script knows that trigger1 is held and the process is started
#			while gpio.input(trigger1):
#				while gpio.input(trigger2):
#					clock=0
#					mChar=[]
#					while gpio.input(button1):	#simple hold switch where itll be active as long as you hold it, but will stop once ou release it
#						sleep(0.1)		#this is a simple clock that waits 0.1 seconds and adds 1; 1 second=10 clock
#						clock=+1
#						if clock=2: print '#',		#at 0.2 seconds, itll print a hashtag telling you itll be a dot, then at 0.5 seconds,
#						if clock=5: print '#'		#itll add another hashtag and no more, telling you its now a dash
#					if clock<=2: mChar.append("_")	#after button release, categorizes what to return to the output list
#					elif (clock>2 and clock<5): mChar.append(".")
#					elif clock<5: mChar.append("-")
#					clock=0	#resets the clock
#				mPhrase.append(str(''.join(str(x) for x in mChar)))	#after block trigger released, compiles cataloged ./- to make a character and puts it into the final list
#				del mChar[:]	#resets the character list
#			return str(' '.join(str(x) for x in mPhrase))
#			break
#screen
while True:
	print "----------------------------------------------------------------"
	print "   Morse Code Transcriber"
	print "----------------------------------------------------------------"
	print "\n\n\n\n"
	conf1 = input("Which Input Mode: 1) text 2) morse 3) exit: ")	#by using input, limited users choices for characters, limiting ways to fail input (still possible though)
	if conf1==3:	#if option 3 the program will immediatly close incase if either you accidentally reran it or you need to go in a hurry
		break
	c2 = raw_input("Input from file: [t/f]: ").lower()
	if (c2=="t" or c2=="true" or c2=="1"): conf2=True	#advanced filter to allow multiple ways to input option while making any other inputed character automatically false (put 'cat' in any [t/f] input and itll automatically be False)
	if conf2:
		dir=raw_input("Set Directory: ")
		try:	#attempts to find file specified, if the file given exists, it uses it.
			termIn=open(dir, "r").read()
		except:	#otherwise it turns off and switches to terminal input mode
			print "error: no file exists"
			conf2=False
	c3=raw_input("Output to file? [t/f]: ")
	if (c3=="t" or c3=="true" or c3=="1"): conf3=True
	if conf3:
			outFile=raw_input("Type name of output file: ")	#removed automatically making output in .txt format to give user more otions in what file to save it as
	c4=raw_input("Use GPIO [t/f]: ").lower()
	if (c4=="t" or c4=="true" or c4=="1"): conf4=True
	if conf4:	#if user asks for gpio to be used, itll first check to see if its possible to get the modules. If it isnt, itll turn it back to False
		try:
			import RPi.GPIO as gpio
			from time import sleep
		except:
			print "waiting on GPIO API"
			conf4=False
	if conf1==1:
		if not conf2:
			termIn = raw_input("Enter Message to Encrypt: ")
		print txt2mrs(termIn)
	elif conf1==2:
#		if conf2==False and conf4:	#will input through GPIO if file input is false and GPIO is true
#			termin=inMorse()
		if not conf2:
			termIn=raw_input("Enter Code to Decrypt: ")
		print mrs2txt(termIn)
	cont=raw_input("Run again? [t/f]: ").lower()
	if (cont=="t" or cont=="true" or cont=="1"): run=True
	else: break
print "Goodbye"
