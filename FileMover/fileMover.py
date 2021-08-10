import csv
import os
import re

baseDir="./img"
os.chdir(baseDir)

def getCSV(path):
 results=[]
 with open(path, newline='',encoding='utf-8') as csvfile:
  orders = csv.reader(csvfile, delimiter=';')
  for row in orders:
    for item in row:
     matchObj= re.match(r"([0-9][0-9][0-9])",item,re.M|re.I)
     if matchObj is not None:
       results.append(item);
 return results
    
def getFileList(path):
 results=[]
 for fname in os.listdir(path):
  fname=fname.replace('.','_').split('_')
  if fname[-1]=="jpg" or fname[-1]=="NEF":
    results.append(fname)
 return results
 
def moveFiles (selected, files):
 processed=0
 for file in files:
  contains = 0
  for select in selected:   
   if select == file[1]:
    contains=1
  if contains==0:
   print (str(file[1])+" nincs kivalaszva")
   os.rename("./"+file[0]+"_"+file[1]+"."+file[2],"./trash/"+file[0]+"_"+file[1]+"."+file[2])
    
selectedPhotos=getCSV("../list.csv")
files=getFileList(".")
moveFiles(selectedPhotos,files)
#input("Waiting for enter")