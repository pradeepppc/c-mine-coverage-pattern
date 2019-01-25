import os

for i in range(10,100,10):
	maxOR = str(i/100.0)
	os.system("python cmine_new.py 0.075 0.5 "+maxOR+"  ../dataset/bmspos/bmspos_1.25L.txt bmspos_1.25L.txt ./")

for i in range(10,100,10):
	minCS = str(i/100.0)
	os.system("python cmine_new.py 0.075 "+minCS+" 0.7 ../dataset/bmspos/bmspos_1.25L.txt bmspos_1.25L.txt ./")

for i in range(5,101,5):
	size = str(i+100/100.0)
	os.system("python cmine_new.py 0.075 0.5 0.7 ../dataset/bmspos/bmspos_"+size+"L.txt bmspos_new_"+size+"L.txt ./")
