#!/usr/bin/python3
import os,sys,time,threading,formlayout
os.environ['http_proxy']=''
from PIL import Image
import urllib.request
import PyQt4 as pyqt
import argparse

def subtract_lists(a, b):
    """ Subtracts two lists. Throws ValueError if b contains items not in a """
    # Terminate if b is empty, otherwise remove b[0] from a and recurse
    return a if len(b) == 0 else [a[:i] + subtract_lists(a[i+1:], b[1:]) 
                                  for i in [a.index(b[0])]][0]

def use_command_line_args(args, citation_fields, chosentype_idx, dirname):
	commandlinefields=list(args.__dict__)
	cite_fields_covered_in_command_line=[]
	for i in commandlinefields:
		for j in citation_fields[chosentype_idx]:
			if i==j:
				cite_fields_covered_in_command_line.append(i)
	datalist=[]
	for i in cite_fields_covered_in_command_line:
		datalist.append((i,args.__dict__[i]))
	cite_fields_not_covered=[]
	for i in citation_fields[chosentype_idx]:
		add=True
		for j in cite_fields_covered_in_command_line:
			if i==j:
				add=False
		if add==True:
			cite_fields_not_covered.append(i)

	for i in  cite_fields_not_covered:
		if i=="citationkey":
			datalist.append((i, dirname))
		else:
			datalist.append((i, ""))
	return datalist

def parse_cmd_line(description, arguments):
	parser=argparse.ArgumentParser(description=description)
	for i in arguments:
		parser.add_argument("--"+i[0], metavar='string', type=str, help=i[1])
	args=parser.parse_args()
	return args

def camerastatus():
	#return 1 if memory has been updated , return 0 if it has not been updated
	response = int(urllib.request.urlopen("http://192.168.0.1/command.cgi?op=102").read())
	return response

def listofphotos():
	lst = urllib.request.urlopen("http://192.168.0.1/command.cgi?op=100&DIR=/DCIM/101MSDCF").read().decode("utf-8").split("\r\n")
	ret=[]
	for i in lst:
		ret.append(i.split(","))
	ret.pop(0)
	ret.pop(len(ret)-1)
	return ret

def is_dir_name_new(dirname,subdirs):
	#XXXXFix this to check for spaces or other weird things in directory name. Also, probably a more efficient way to to this function. Maybe in os.
	ret=True
	for i in subdirs:
		if dirname==i:
			ret=False	
	return ret

def try_command_line(args,varname):
	try:
		var=args.__dict__[varname]
	except AttributeError:
		var=""	
	
	return var

def new_archive_file(args): #start/end are for the different windows. Variables are not segregated along those lines, just the visuals.
#start------------------------------  #get name of desired subdir, and make sure it is unique
	subdirs=[dr for dr in os.listdir(os.getcwd()) if os.path.isdir(dr)]

	archdir=try_command_line(args,"fondsname")
	print("XXX", archdir)
	dirname=formlayout.fedit([("Archive directory", archdir)],title="CSDH 2014 : Daniel Simeone", comment="Choose a name for the directory (no spaces).")[0]
	while not is_dir_name_new(dirname,subdirs):
		dirname=formlayout.fedit([("Archive directory", "")],title="CSDH 2014 : Daniel Simeone", comment="ERROR. Directory already exists. Choose a new name for the directory (no spaces).")[0]
#end------------------------------
#start---------------------------
	#the citation type goes with the corresponding set of citation fields
	citation_types=["article", "book", "misc"]
	citation_desc=["For journal articles.", "For monographs.", "For other types of material."]
	#ensure that citationkey is the in the first entry. For all the rest, the order is arbitrary
	citation_fields=[
			["citationkey","author","title","journal","number","year"],
			["citationkey", "author", "title", "year", "publisher", "address"],
			["citationkey","author","title","year","pages","howpublished"]
			]
	chosentype=formlayout.fedit([("Bibliographic type", ["article"] +  citation_types)],title="CSDH 2014 : Daniel Simeone", comment="Choose type of bibliographic entry.")[0]
#end---------------------
#start--------------------
	chosentype_idx=-1
	for i in range(len(citation_types)):
		if str(citation_types[i])==str(chosentype):
			chosentype_idx=i
	
	datalist=use_command_line_args(args, citation_fields, chosentype_idx, dirname)

	field_data=formlayout.fedit(datalist,"CSDH 2014 : Daniel Simeone")

	bibfile=("@"+citation_types[chosentype_idx]+"{" + field_data[0] +",\n")
	for i in range(len(field_data)-1):
		bibfile+=citation_fields[chosentype_idx][i+1] + " =  {" + field_data[i+1] + "},\n"
	bibfile+="}\n"
	#now, create directory dirname and write citation.bib to dirname - we do it now to make sure that it the next screen crashes, we've saved user data - if no changes are made in next screen, then this write is the only write. If some are, then the file is re-written.
	os.makedirs(dirname)	
	with open(dirname+"/citation.bib", "w") as text_file:
		text_file.write(bibfile)
#end -------------------------
#start------------------------

	bibfile_ed=formlayout.fedit([("Bibtex Entry",bibfile)],"CSDH 2014 : Daniel Simeone",comment="This is the BibTeX entry that will be used. Edit it as need.")[0]
	if bibfile!=bibfile_ed:
		with open(dirname+"/citation.bib", "w") as text_file:
			text_file.write(bibfile_ed)
#end---------------------------		
	return dirname

def get_new_photos(self):
	currentphotos=listofphotos()
	newphotos=subtract_lists(currentphotos, self.initialphotos)
	for i in newphotos:
		imageurl=("http://192.168.0.1" + i[0] + "/" + i[1])
		os.system("wget "+ imageurl)	
		os.system("mv "+i[1] +  " ./" + self.dirname)
		imagefilename="./"  + self.dirname + "/" + i[1]
		os.system("killall display") # TODO XXX  make this a proper subprocess, and don't killall....
		size = 1680, 1050
		im = Image.open(imagefilename)
		#im2=im.resize(size, Image.ANTIALIAS)
		im.show()
		self.totaldownloaded+=1
		self.filesdownloaded.append(i[1])
	self.initialphotos=currentphotos#so we don't download them twice
			
class GetPhotos(threading.Thread):
	def run(self):
		self.alive = True
		self.totaldownloaded=0
		self.filesdownloaded=[]
		self.initialphotos=listofphotos()
		while self.alive:
			camstat=camerastatus()
			if camstat==1:
				get_new_photos(self)
			time.sleep(7)
	def stop(self):
		get_new_photos(self)
		self.alive = False
		self.join()

class MsgBox(pyqt.QtGui.QWidget):
	def __init__(self):
		super(MsgBox, self).__init__()
		self.initUI()
	def initUI(self):               
		qbtn = pyqt.QtGui.QPushButton('Take pictures. Click here when done', self)
		qbtn.clicked.connect(pyqt.QtCore.QCoreApplication.instance().quit)
		qbtn.move(10, 10)       
		self.setGeometry(300, 300, 270, 50)
		self.setWindowTitle('CSDH 2014 : Daniel Simeone')    
		self.show()

if __name__ == '__main__':
	photothread = GetPhotos() # Creates a threading object that will loop around looking for newly taken photos, and then run wget to retrieve them

	args=parse_cmd_line("Rapid file archiving using an SD card", [["fondsname","unique name of the directory and the keyname"], ["author", "author name"], ["title", "title"], ["year", "year"]])


	photothread.dirname=new_archive_file(args) # Runs the forms to collect the bibliographic information, creates and writes the citation.bib file to the indicated dirname, and returns that dirname to a variable of the threading object so that the photographs will be written to the correct directory


	photothread.start()  # After the bibliographic info has been collected, begins the photo transfer process. 
	app = pyqt.QtGui.QApplication(sys.argv) #Creates the environment for the message box during photo taking.
	ex = MsgBox() #Creates the message box
	app.exec_()#Waits till clicked for done.
	photothread.alive=False # Kills the photo downloading instance. 
	os.system("killall display")#just to make sure the display isn't still there...

