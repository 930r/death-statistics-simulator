import csv
from scipy.stats import beta
import numpy as np
import pylab


#this generates an array of ages of death
#lx = average life expectancy
#population = how many hundreds of ages to generate
#i think i got the curve pretty well except no infant deaths but whatever
def lxsample(lx, population):
	max_time = lx*1.3
	min_time = 0
	a, b = 10, 3.5
	sample = min_time + beta.rvs(a, b, size=round(population*100)) * (max_time - min_time)
	return sample

firstyear = 1900
lastyear = 2020

#COMMENT THIS OUT TO SKIP OVER SIMULATING DEATHS (it can take a while)
##################################################################################################
#starting out the file with the years on each line
f = open("routput.csv",'w')
for i in range(lastyear-firstyear+1):
	f.write(f"{firstyear+i}\n")
f.close()
f = open("loutput.csv",'w')
for i in range(lastyear-firstyear+1):
	f.write(f"{firstyear+i}\n")
f.close()

#legend
# row[0] = year
# row[1] = percentage of left handed people
# row[2] = life expectancy
# row[3] = total population divided by a billion
#adding each simulated death to the line of the year they died in, each death is represented by an integer which is the age they died at
with open('stats.csv') as csvfile:
	for row in csv.reader(csvfile):
		year=int(row[0])
		plh=float(row[1])
		lx=float(row[2])
		population=float(row[3])

		rsample = lxsample(lx, population*(100-plh))
		print(f"year={year}")

		with open('routput.csv', 'r') as file:
			data = file.readlines()
		for i in rsample:
			yearofdeath= round(i)+year
			if(yearofdeath >= lastyear):
				continue
			data[yearofdeath-firstyear]=data[yearofdeath-firstyear].rstrip("\n")+f", {round(i)}\n"
		with open('routput.csv', 'w') as file:
			file.writelines( data )
		#doing the same thing but for the left handed population
		lsample = lxsample(lx, population*plh)
		with open('loutput.csv', 'r') as file:
			data = file.readlines()
		for i in lsample:
			yearofdeath= round(i)+year
			if(yearofdeath >= lastyear):
				continue
			data[yearofdeath-firstyear]=data[yearofdeath-firstyear].rstrip("\n")+f", {round(i)}\n"
		with open('loutput.csv', 'w') as file:
			file.writelines( data )
##################################################################################################
#this is where we output to the console, it would have been better to do it in a file so the tabs would stay as tabs but who cares
#just use this regex to turn the spaces into tabs so you can paste it in a spreadsheet
#([ \t]+)

with open('routput.csv', 'r') as file:
	rdata = file.readlines()
with open('loutput.csv', 'r') as file:
	ldata = file.readlines()

raverage=[]
laverage=[]
for i in range(lastyear-firstyear):
	for j, x in enumerate(rdata[i].split(',')):
		if j == 0:
			continue
		raverage.append(int(x.rstrip("\n")))
	for j, x in enumerate(ldata[i].split(',')):
		if j == 0:
			continue
		laverage.append(int(x.rstrip("\n")))
	print(f"{i+firstyear}\t{np.mean(raverage)}\t{np.mean(laverage)}")
	raverage.clear()
	laverage.clear()


