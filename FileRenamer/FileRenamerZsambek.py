import csv
import os

baseDir="D:/Dropbox/Prog/Fotozás/FileRenamer/img"
os.chdir(baseDir)

def getCSV(path):
	results=[]
	with open(path, newline='',encoding='utf-8') as csvfile:
		orders = csv.reader(csvfile, delimiter=',')
		for row in orders:
			results.append(row)
	return results
def getFileList(path):
	results=[]
	for fname in os.listdir(path):
		results.append(fname.split("."))
	return results
	
def renameFiles (table, files):
	processed=0
	for x in table:
		for y in files:
			if x[4]==y[0]:
				processed+=1
				#os.rename(y[0]+"."+y[1], (x[1]+"_"+x[2]+"_"+x[3]+"."+y[1]))
				print("Renaming: "+y[0]+"."+y[1]+" -> "+(x[1]+"_"+x[2]+"_"+x[3]+"."+y[1]))
	if (processed==0):
		print("Nothing to do")


table=getCSV("../list.csv")
files=getFileList(".")
renameFiles(table,files)
input("Waiting for enter")



