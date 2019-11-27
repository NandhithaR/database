import numpy as np
from tabulate import tabulate
import numpy.lib.recfunctions as rfn
# from operator import itemgetter
# from itertools import groupby
from collections import defaultdict
# from BTrees.OOBTree import OOBTree
import re

hashmap={}
# btree = OOBTree()
collection=[]
def Hash(data,colname):
	if key in hashmap:
		collection[hashmap[key]]['value'] = value
	else:
		collection = np.append(collection, np.array([(key,value)], dtype=collection.dtype))
		hashmap[key] = len(collection) - 1 
# def Btree(data,colname):


#check if string can be converted to float
def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False
#Import a vertical bar delimited file into an array-table
def importfile(filename):
	file_array=np.genfromtxt(filename,dtype=None,delimiter='|',names=True)
	#headers=[file_array.dtype.names,file_array.dtype]
	dtypes=[file_array.dtype]
	headers=[file_array.dtype.names]
	return file_array
	

def exportfile():
	x = np.arange(0, 10, 1)
	c = np.savetxt('geekfile1.txt', x, delimiter =',') 
	a = open("geekfile1.txt", 'r')# open file in read mode 
	print("the file contains:") 
	print(a.read()) 
	return a

#sort by columns
def sortColumns(filename,colname):
	head,data=importfile(filename)
	# f=l[1:,[1]]
	data.sort(order=colname)
	return data

def projection(table_name,*colname):
	#head,data=importfile(filename)
	data=table_name
	h=[]
	d=[]
	for i in colname:
		h.append(i)
		d.append(data[i])
	t_matrix = zip(*d)
	table = tabulate(t_matrix, h, tablefmt="fancy_grid")
	return table

##### to do ######
def select(table_name,*arg):
	data=table_name
	print(arg)
	# s=data[data['qty']==2]
	# for i in range(len(s)):
	# 	s[i][5]=s[i][5]+5
	# return data[(data['itemid']>75) | (data['qty']>2)]

#selection, projection, count, sum and avg aggregates
def getAverage(filename,colname):
	head,data=importfile(filename)
	average=np.mean(data[colname])
	return average

def moving_average(filename,colname, n):
	head,data=importfile(filename)
	ret = np.cumsum(data[colname], dtype=float)
	ret[n:] = ret[n:] - ret[:-n]
	return ret[n - 1:] / n

def moving_sum(filename,colname, n):
	head,data=importfile(filename)
	ret = np.cumsum(data[colname], dtype=float)
	ret[n:] = ret[n:] - ret[:-n]
	return ret[n - 1:]

def avgGroup(filename,*colname):
	head,data=importfile(filename)
	s=colname[0]
	h=[]
	d=[]
	for i in colname:
		h.append(i)
		d.append(data[i])
	t_matrix = zip(*d)
	np.array([(k, np.array(list(g), dtype=data[h].dtype).view(np.recarray)[h[0]].mean())
          for k, g in groupby(np.sort(data[h], order=h[0]).view(np.recarray),
                              itemgetter(h[0]))], dtype=data[h].dtype)

def getSum(filename,colname):
	head,data=importfile(filename)
	s=np.sum(data[colname])
	return s


def sumGroup(filename, *colname):
	head,data=importfile(filename)
	s=colname[0]
	h=[]
	d=[]
	for i in colname:
		h.append(i)
		d.append(data[i])
	t_matrix = zip(*d)
	u_ij, inv_ij = np.unique(data[h[1:]], return_inverse=True)
	# Create a totals array. You could do the fancy ijv_dtype thing if you wanted.
	totals=np.zeros(len(u_ij))
	np.add.at(totals, inv_ij, data[h[0]])
	return totals

def concateCols(filename,*colname):
	head,data=importfile(filename)
	h=[]
	d=[]
	for i in head:
		h.append(i)

def getGroupBy(filename,*colname):
	head,data=importfile(filename)
	np.groupby()

#sumgroup, avggroup, moving avg, moving sum, group by, join


if __name__ == "__main__":
	table={}
	st = ""
	print("Enter quit to exit")
	while(st!="quit"):
		st = raw_input()
		params=st.split(" ")
		#call function
		if(st.find("inputfromfile")!=-1):
			p = params[2]
			filename = p[p.find('(')+1:p.find(')')]+".txt"
			d=importfile(filename)
			table[params[0]]=d
			print(table)
		elif(st.find("select")!=-1):
			p = params[2]
			#only one condition
			# print(table[p[p.find('(')+1:].strip(',')])
			#more than one condition
			table_name = table[p[p.find('(')+1:].strip(',')]
			conditions = params[3:]
			d=select(table_name,conditions)
			table[params[0]]=d
		elif(st.find("project")!=-1):
			p = params[2]
			table_name = table[p[p.find('(')+1:].strip(',')]
			column_names = params[3:]
			d=projection(table_name,column_names)
			table[params[0]]=d
		elif(st.find("avg")!=-1):
			p = params[2]
			table_name = table[p[p.find('(')+1:].strip(',')]
			column = params[3]
			d=getAverage(table_name,column)
			table[params[0]]=d
		elif(st.find("sumgroup")!=-1):
			p = params[2]
			table_name = table[p[p.find('(')+1:].strip(',')]
			args = params[3:]
			d=sumGroup(table_name,args)
			table[params[0]]=d
		elif(st.find("avggroup")!=-1):
			p = params[2]
			table_name = table[p[p.find('(')+1:].strip(',')]
			args = params[3:]
			d=avgGroup(table_name,args)
			table[params[0]]=d
		elif(st.find("movavg")!=-1):
			length = len(params)
			p = params[2]
			table_name = table[p[p.find('(')+1:].strip(',')]
			args = params[3:length-1]
			val = params[length-1]
			d=moving_average(table_name,args,val)
			table[params[0]]=d
		elif(st.find("movsum")!=-1):
			length = len(params)
			p = params[2]
			table_name = table[p[p.find('(')+1:].strip(',')]
			args = params[3:length-1]
			val = params[length-1]
			d=moving_sum(table_name,args,val)
			table[params[0]]=d
		elif(st.find("Btree")!=-1):
			p = params[2]
			table_name = table[p[p.find('(')+1:].strip(',')]
			column = params[3]
			d=Btree(table_name,column)
			table[params[0]]=d
		elif(st.find("Hash")!=-1):
			p = params[2]
			table_name = table[p[p.find('(')+1:].strip(',')]
			column = params[3]
			d=Hash(table_name,column)
			table[params[0]]=d
		


#    head,data=importfile('sampledata.txt')
#    sortColumns('sampledata.txt','qty')
#    getAverage('sampledata.txt','qty')
#    projection('sampledata.txt','qty','saleid','itemid')
#    getSum('sampledata.txt','qty')
#    select('sampledata.txt','qty=5')
#    sumGroup('sampledata.txt','qty','pricerange')
#    moving_average('sampledata.txt','qty',3)
#    moving_sum('sampledata.txt','qty',3)
# #    parseSelect('(time > 50) or (qty < 30)')
#    Hash(data,'itemid') 
#    Hash(data,'qty')
#    head1,data1=importfile('datasample.txt')
#    Hash(data1,'Q')

