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
	data=table_name
	h=[]
	d=[]
	for i in colname[0]:
		h.append(i)
		d.append(data[i])

	t_matrix = zip(*d)
	table = tabulate(t_matrix, h, tablefmt="fancy_grid")
	return data[colname[0]]

##### to do ######
def select_single_noarithmetic(table_name,col,cond):
	data=table_name
	if(cond[0]=='>'):
		s=data[data[col]>cond[1]]
	elif(cond[0]=='<'):
		s=data[data[col]<cond[1]]
	elif(cond[0]=='='):
		s=data[data[col]==cond[1]]
	elif(cond[0]=='<='):
		s=data[data[col]<=cond[1]]
	elif(cond[0]=='>='):
		s=data[data[col]>=cond[1]]
	elif(cond[0]=='!='):
		s=data[data[col]!=cond[1]]
	# s=data[data[col]>5]
	print(s)
	# for i in range(len(s)):
	# 	s[i][5]=s[i][5]+5
	# return data[(data['itemid']>75) | (data['qty']>2)]
def select_multiple_noarithmetic(table_name,col,ops,const,t):
	data=table_name
	if t == 'or':
		s=False
		l=[s]
		for i in range(len(col)):
			if ops[i] == '>':
				b = (data[col[i]]>int(const[i]))
			elif ops[i] == '<':
				b = data[col[i]]<int(const[i])
			elif ops[i] == '=':
				b = data[col[i]]==int(const[i])
			elif ops[i] == '<=':
				b = data[col[i]]<=int(const[i])
			elif ops[i] == '>=':
				b = data[col[i]]>=int(const[i])
			elif ops[i] == '!=':
				b = data[col[i]]!=int(const[i])
			l=l|b
		print(data[l])
	if t == 'and':
		s=False
		l=[s]
		for i in range(len(col)):
			if ops[i] == '>':
				b = (data[col[i]]>int(const[i]))
			elif ops[i] == '<':
				b = data[col[i]]<int(const[i])
			elif ops[i] == '=':
				b = data[col[i]]==int(const[i])
			elif ops[i] == '<=':
				b = data[col[i]]<=int(const[i])
			elif ops[i] == '>=':
				b = data[col[i]]>=int(const[i])
			elif ops[i] == '!=':
				b = data[col[i]]!=int(const[i])
			l=l&b
		print(data[l])
		# print((data['time']>50) | (data['qty']<30))

def select_single_arithmetic(table_name,col,arithop,a_const,r_const,op):
	data=table_name
	print(col)
	# s=data[data[col]>int(r_const)]
	# print(s)
	# for i in range(len(s)):
	# 	s[i][5]=s[i][5]+5

# def select_multiple_noarithmetic():

#selection, projection, count, sum and avg aggregates
def getAverage(table_name,colname):
	data=table_name
	average=np.mean(data[colname])
	return average

def moving_average(table_name,colname, n):
	data = table_name
	ret = np.cumsum(data[colname[0]], dtype=float)
	n=int(n)
	ret[n:] = ret[n:] - ret[:-n]
	return ret[n - 1:] / n

def moving_sum(table_name,colname, n):
	data = table_name
	ret = np.cumsum(data[colname[0]], dtype=float)
	n=int(n)
	ret[n:] = ret[n:] - ret[:-n]
	print(ret[n-1:])
	return ret[n - 1:]

# def avgGroup(filename,*colname):
# 	head,data=importfile(filename)
# 	s=colname[0]
# 	h=[]
# 	d=[]
# 	for i in colname:
# 		h.append(i)
# 		d.append(data[i])
# 	t_matrix = zip(*d)
# 	np.array([(k, np.array(list(g), dtype=data[h].dtype).view(np.recarray)[h[0]].mean())
#           for k, g in groupby(np.sort(data[h], order=h[0]).view(np.recarray),
#                               itemgetter(h[0]))], dtype=data[h].dtype)

def getSum(filename,colname):
	head,data=importfile(filename)
	s=np.sum(data[colname])
	return s

def sumGroup(table_name, colname):
	data=table_name
	s=colname[0]
	h=colname
	u_ij, inv_ij = np.unique(data[h[1:]], return_inverse=True)
	totals=np.zeros(len(u_ij))
	np.add.at(totals, inv_ij, data[h[0]])
	flat_list = [item for sublist in u_ij for item in sublist]
	tab = [totals,flat_list]
	t_matrix = zip(*tab)
	t = [h,t_matrix]
	to_return = [totals,u_ij]
	print(u_ij)
	print(t_matrix)
	table = tabulate(t_matrix, h, tablefmt="fancy_grid")
	# print(table)
	return totals

def concateCols(filename,*colname):
	head,data=importfile(filename)
	h=[]
	d=[]
	for i in head:
		h.append(i)

# def getGroupBy(filename,*colname):
# 	head,data=importfile(filename)
# 	np.groupby()

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
			# print(table)
		elif(params[2].startswith("select")):
			p = params[2]
			table_name = table[p[p.find('(')+1:].strip(',')]
			cond = params[3:]
			if ('+' in cond) or ('*' in cond) or ('/' in cond) or ('-' in cond):
				if '(' not in cond[0]:
					if(params[3] in table_name[0]):
						col = params[3].strip('[,()]')
						arithop = params[4].strip('[,()]')
						a_const= params[5].strip('[,()]')
						r_const=params[7].strip('[,()]')
						op=params[6].strip('[,()]')
					else:
						col = params[5].strip('[,()]')
						arithop=params[6].strip('[,()]')
						a_const=params[7].strip('[,()]')
						r_const=params[3].strip('[,()]')
						op=params[4].strip('[,()]')
					d=select_single_arithmetic(table_name,col,arithop,a_const,r_const,op)	
					
			else:
				if '(' not in cond[0]:
					#separate col and conditions
					if(params[3] in table_name[0]):
						col = params[3]
					else:
						col = params[5]
					condition = params[4:]
					final_condition = [j.strip('[,()]') for j in condition]
					final_condition = [i for i in final_condition if i] 
					d=select_single_noarithmetic(table_name,col,final_condition)
				else:
					cols =[]
					const=[]
					op=[]
					#or conditions
					if('or' in cond):
						for i in range(len(cond)):
							cond[i]=cond[i].strip('[,()]')
							if cond[i] in table_name[0][0]:
								cols.append(cond[i])
							elif cond[i] in ['>','<','=','<=','>=']:
								op.append(cond[i])
							elif cond[i].isdigit():
								const.append(cond[i])
						d=select_multiple_noarithmetic(table_name,cols,op,const,'or')
					elif('and' in cond):
						for i in range(len(cond)):
							cond[i].strip('[,()]')
							if cond[i] in table_name[0]:
								cols.append(cond[i])
							elif cond[i] in ['>','<','=','<=','>=']:
								op.append(cond[i])
							elif cond[i].isdigit():
								const.append(cond[i])
						d=select_multiple_noarithmetic(table_name,cols,op,const,'and')	

			#only one condition
			# if '(' not in somestring: 
			# # print(table[p[p.find('(')+1:].strip(',')])
			# #more than one condition
			# table_name = table[p[p.find('(')+1:].strip(',')]
			# conditions = params[3:]
			# d=select(table_name[1],conditions)
			# table[params[0]]=d

		elif(params[2].startswith("project")):
			p = params[2:]
			res = [sub.replace('project', "") for sub in p] 
			stripped_list = [j.split(',') for j in res]
			final_args = [[x.strip('[,()]') for x in l] for l in stripped_list]
			final_args = [[i for i in l if i] for l in final_args] 
			final_args = [j for sub in final_args for j in sub]
			table_name = table[final_args[0]]
			column_names = final_args[1:]
			d=projection(table_name,column_names)
			table[params[0]]=d

		elif(params[2].startswith("avg")):
			p = params[2:]
			res = [sub.replace('avg', "") for sub in p] 
			stripped_list = [j.split(',') for j in res]
			final_args = [[x.strip('[,()]') for x in l] for l in stripped_list]
			final_args = [[i for i in l if i] for l in final_args] 
			final_args = [j for sub in final_args for j in sub]
			table_name = table[final_args[0]]
			column_names = final_args[1:]
			d=getAverage(table_name,column_names[0])
			table[params[0]]=d

		elif(params[2].startswith("sumgroup")):
			p = params[2:]
			res = [sub.replace('sumgroup', "") for sub in p] 
			stripped_list = [j.split(',') for j in res]
			final_args = [[x.strip('[,()]') for x in l] for l in stripped_list]
			final_args = [[i for i in l if i] for l in final_args] 
			final_args = [j for sub in final_args for j in sub]
			table_name = table[final_args[0]]
			column_names = final_args[1:]
			d=sumGroup(table_name,column_names)
			table[params[0]]=d

		# elif(params[2].startswith("avggroup")):
		# 	p = params[2:]
		# 	table_name = table[(p[0].split('('))[1].split(',')[0]]
		# 	args = params[3:]
		# 	final_args = [j.strip('[,()]') for j in args]
		# 	final_args = [i for i in final_args if i] 
		# 	d=avgGroup(table_name[1],final_args)
		# 	table[params[0]]=d

		elif(params[2].startswith("movavg")):
			p = params[2:]
			res = [sub.replace('movavg', "") for sub in p] 
			stripped_list = [j.split(',') for j in res]
			final_args = [[x.strip('[,()]') for x in l] for l in stripped_list]
			final_args = [[i for i in l if i] for l in final_args] 
			final_args = [j for sub in final_args for j in sub]
			table_name = table[final_args[0]]
			length = len(final_args)
			d=moving_average(table_name,final_args[1:length-1],final_args[length-1])
			table[params[0]]=d

		elif(params[2].startswith("movsum")):
			p = params[2:]
			res = [sub.replace('movsum', "") for sub in p] 
			stripped_list = [j.split(',') for j in res]
			final_args = [[x.strip('[,()]') for x in l] for l in stripped_list]
			final_args = [[i for i in l if i] for l in final_args] 
			final_args = [j for sub in final_args for j in sub]
			table_name = table[final_args[0]]
			length = len(final_args)
			d=moving_sum(table_name,final_args[1:length-1],final_args[length-1])
			table[params[0]]=d

		# elif(st.find("Btree")!=-1):
		# 	p = params[2]
		# 	table_name = table[p[p.find('(')+1:].strip(',')]
		# 	column = params[3]
		# 	d=Btree(table_name,column)
		# 	table[params[0]]=d

		# elif(st.find("Hash")!=-1):
		# 	p = params[2]
		# 	table_name = table[p[p.find('(')+1:].strip(',')]
		# 	column = params[3]
		# 	d=Hash(table_name,column)
		# 	table[params[0]]=d
		


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

