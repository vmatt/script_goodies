import csv
import os
import subprocess

def runcmd(cmd):
	x = subprocess.call(cmd,stdout=subprocess.PIPE, shell=True)
		
def list_files(path):
	for path, dirs, files in os.walk(path):
		print (path.replace("img/",""))
		for f in files:
			print (f+" "+get_half_width(path+"/"+f)+"px")

def get_half_width(filename):
	dim = subprocess.Popen(["identify","-format","%w",filename], stdout=subprocess.PIPE).communicate()[0].decode(encoding="UTF-8")
	dim = float(dim)
	dimHalf=dim/2
	dimShiftedToLeft=int(dimHalf-((dim/100*int(blur_width))/2))
	return(str(dimShiftedToLeft))
	
def get_height(filename):
	dim = subprocess.Popen(["identify","-format","%h",filename], stdout=subprocess.PIPE).communicate()[0].decode(encoding="UTF-8")
	return(dim)

def get_csv(path):
	one=0
	two=0
	three=0
	fullList=[];
	with open(path, newline='') as csvfile:
		orders = csv.reader(csvfile, delimiter=';', quotechar='|')
		#	counting pics/person	
		for row in orders:
			array=[0,0,0,0]
			array[0]=row[0]
			if row[1]:
				array[1]=int(row[1])
			if row[2]:
				array[2]=int(row[2])
			if row[3]:
				array[3]=int(row[3])
			fullList.append(array)
	return(fullList)

def side2side(fpath1,fpath2,output):
	output=completeFolder+"/"+output+".jpg"
	height1=get_height(fpath1)
	height2=get_height(fpath2)
	
	if height1!=height2:
		print("DIFFHEIGHT!!!")
	print("Merge:	"+fpath1+"			"+fpath2+"			"+output)
	runcmd("convert \""+fpath1+"\" \""+fpath2+"\" -resize x"+height1+" +append "+output)
	height3=get_height(output)
	#runcmd("convert "+output+" +repage -gravity south -crop x274 "+output)
	runcmd("convert "+output+" +repage -gravity south -crop x2527+0+211! "+output)
	print("Blur :	"+fpath1+"			"+fpath2+"			"+output)
	runcmd("convert "+output+" -region "+blur_width+"x100%+"+get_half_width(output)+"+0 -blur 35x10 "+output)
	
	

def do_the_array(array):
	for row in array:
		if row[1]>0:
			push_new_pics(row[0],"1.jpg",row[1])
		if row[2]>0:
			push_new_pics(row[0],"2.jpg",row[2])
		if row[3]>0:
			push_new_pics(row[0],"3.jpg",row[3])
			
def push_new_pics(name,file,howmany):
	for x in range(0,howmany):
		generatablePicList.append(folderPath+"/"+name+"/"+file)	
		
def generate_all_pics(array):
	a=0
	for i in range(0,len(array),2):
		#print(str(i)+"	"+array[i]+"	"+array[i+1])
		side2side(array[i],array[i+1],str(a))
		a=a+1
		
#HERE STARTS THE MAGIC
generatablePicList=[]
blur_width="1"
folderPath="img"
completeFolder="img/_fin2"

#megrendelések beolvasása csvből
orders=get_csv("list.csv")
#a beolvasott táblázat alapján a push_new_pics fgv segítségével létrehozunk egy új tömböt, amiben már darabpontosan benne vannak a fájlelérési utak
do_the_array(orders)
#generatablePicList=generatablePicList[-2:]   
#a generatablePicList tömbből kinyert adatok alapján a side2side fgv segítségével kettesével egymás mellé pakoljuk, és elmossuk a közepét az egyesített képeknek
generate_all_pics(generatablePicList)