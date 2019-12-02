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
counter = 0
def Hash(table_name,col_name):
	key, value = col_name, table_name[col_name]
	#get the key value pair and store in HashTable
	if key in hashmap:
		collection[hashmap[key]]['value'] = value
	else:
		collection = np.append(collection, np.array([(key,value)], dtype=collection.dtype))
		hashmap[key] = len(collection) - 1 
	print(hashmap)
	print(collection)
	# elif operation == 'search':
	# 	parameters = each_line[each_line.find('(')+1:each_line.find(')')]
	# 	key = int(parameters)
	# if key in hashmap and hashmap[key] != -1:
	# 	search_answers.append(collection[hashmap[key]]['value'])
	# 	print(collection[hashmap[key]]['value'])
	# else:
	# 	search_answers.append("not present")
	# 	print("not present")
	# total_time = time.time() - start_time

# def Btree(data,colname):

def getJoin(table1,table2,args):
	head1=table1.dtype.names
	head2=table2.dtype.names
	data1=table1
	data2=table2
	s = ""
	for i in args:
		s+=i
	#multiple join
	if 'and' in s:
		print("mutiple join")
	#single join
	else:
		(left,right) = s.split("=")
		(left_file,left_col) = left.split(".")
		(right_file,right_col) = right.split(".")
		index1 = head1.index(left_col)
		index2 = head2.index(right_col)
		# j = []
		# l = []
		# # j=np.array([data1,data2])
		# # print(j)
		col_first=[]
		col_sec=[]
		first = data1[left_col]
		second = data2[right_col]
		temp = np.intersect1d(first,second)
		for a in temp:
			if(a in data1[left_col]):
				# ind_left = np.where(data1[left_col] == a)
				# print(ind_left)
				col_first.append(data1[left_col])
		# 		j.append(data1[ind_left])
		print(col_first)
		# 	if(a in data2[right_col]):
		# 		ind_right = np.where(data2[right_col] == a)
		# 		l.append(data2[ind_left])
		# 	n.append(m)
		# print(m)
		# first=[]
		# second=[]
		# indfirst=0
		# print(l[0])

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
def findrelop(s):
	if '>' in s:
		relop = '>'
	elif '<' in s:
		relop = '<'
	elif '=' in s:
		relop = '='
	elif '>=' in s:
		relop = '>='
	elif '<=' in s:
		relop = '<='
	elif '!=' in s:
		relop = '!='
	return relop

def getSelect(table_name,args):
	s = ""
	data=table_name
	for i in args:
		s+=i
	if ('or' in s) and ('+' in s or '-' in s or '*' in s or '/' in s):
		cond=s.split('or')
		l=[True]

		for i in range(len(cond)):
			op=findrelop(cond[i])
			c=cond[i].split(op)
			if c[0].isdigit():
				cols=c[1]
				const=c[0]
			else:
				cols=c[0]
				const=c[1]
			if '+' in cols:
				col =cols.split('+')
				for i in range(len(data[col[0]])):
					data[col[0]][i] = data[col[0]][i] + int(col[1])
			if '-' in cols:
				col =cols.split('-')
				for i in range(len(data[col[0]])):
					data[col[0]][i] = data[col[0]][i] - int(col[1])
			if '/' in cols:
				col =cols.split('/')
				for i in range(len(data[col[0]])):
					data[col[0]][i] = data[col[0]][i] / float(col[1])
			if '*' in cols:
				col =cols.split('*')
				for i in range(len(data[col[0]])):
					data[col[0]][i] = data[col[0]][i] * float(col[1])

			if op == '>':
				b = (data[col[0]]>int(const))
			elif op == '<':
				b = data[col[0]]<int(const)
			elif op == '=':
				b = data[col[0]]==int(const)
			elif op == '<=':
				b = data[col[0]]<=int(const)
			elif op == '>=':
				b = data[col[0]]>=int(const)
			elif op == '!=':
				b = data[col[0]]!=int(const)
			l=l|b
		return data[l]
		print(data[l])
	elif ('and' in s) and ('+' in s or '-' in s or '*' in s or '/' in s):
		cond=s.split('and')
		l=[True]

		for i in range(len(cond)):
			op=findrelop(cond[i])
			c=cond[i].split(op)
			if c[0].isdigit():
				cols=c[1]
				const=c[0]
			else:
				cols=c[0]
				const=c[1]
			if '+' in cols:
				col =cols.split('+')
				for i in range(len(data[col[0]])):
					data[col[0]][i] = data[col[0]][i] + int(col[1])
			if '-' in cols:
				col =cols.split('-')
				for i in range(len(data[col[0]])):
					data[col[0]][i] = data[col[0]][i] - int(col[1])
			if '/' in cols:
				col =cols.split('/')
				for i in range(len(data[col[0]])):
					data[col[0]][i] = data[col[0]][i] / float(col[1])
			if '*' in cols:
				col =cols.split('*')
				for i in range(len(data[col[0]])):
					data[col[0]][i] = data[col[0]][i] * float(col[1])

			if op == '>':
				b = (data[col[0]]>int(const))
			elif op == '<':
				b = data[col[0]]<int(const)
			elif op == '=':
				b = data[col[0]]==int(const)
			elif op == '<=':
				b = data[col[0]]<=int(const)
			elif op == '>=':
				b = data[col[0]]>=int(const)
			elif op == '!=':
				b = data[col[0]]!=int(const)
			l=l&b
		return data[l]
	elif '+' in s or '-' in s or '*' in s or '/' in s:
		# s=data[data[col]>int(r_const)]
		print(s)
		if '>' in s:
			relop = '>'
			s=s.split('>')
		elif '<' in s:
			relop = '<'
			s=s.split('<')
		elif '=' in s:
			relop = '='
			s=s.split('=')
		elif '>=' in s:
			relop = '>='
			s=s.split('>=')
		elif '<=' in s:
			relop = '<='
			s=s.split('<=')
		elif '!=' in s:
			relop = '!='
			s=s.split('!=')
		print(s)
		if s[0].isdigit():
			const=s[0]
			col=s[1]
		else:
			const=s[1]
			col=s[0]
		#split col-name arithmetic operation and const
		if '+' in col:
			col =col.split('+')
			for i in range(len(data[col[0]])):
				data[col[0]][i] = data[col[0]][i] + int(col[1])
		if '-' in col:
			col =col.split('-')
			for i in range(len(data[col[0]])):
				data[col[0]][i] = data[col[0]][i] - int(col[1])
		if '/' in col:
			col =col.split('/')
			for i in range(len(data[col[0]])):
				data[col[0]][i] = data[col[0]][i] / float(col[1])
		if '*' in col:
			col =col.split('*')
			for i in range(len(data[col[0]])):
				data[col[0]][i] = data[col[0]][i] * float(col[1])
		
		if relop=='>':
			ans = data[data[col[0]]>int(const)]
		elif relop=='<':
			ans = data[data[col[0]]<int(const)]
		elif relop=='=':
			ans = data[data[col[0]]==int(const)]
		elif relop=='>=':
			ans = data[data[col[0]]<=int(const)]
		elif relop=='<=':
			ans = data[data[col[0]]<=int(const)]
		elif relop=='!=':
			ans = data[data[col[0]]!=int(const)]
		return ans
		# for i in range(len(s)):
		# 	s[i][5]=s[i][5]+5
	elif 'or' in s:
		cond=s.split('or')
		# cols=[]
		v=True
		l=[v]
		# const=[]
		for i in range(len(cond)):
			op=findrelop(cond[i])
			c=cond[i].split(op)
			if c[0] in data.dtype.names:
				# cols.append(c[0])
				cols=c[0]
				# const.append(c[1])
				const=c[1]
			else:
				# cols.append(c[1])
				cols=c[1]
				# const.append(c[0])
				const=c[0]

			if op == '>':
				b = (data[cols]>int(const))
			elif op == '<':
				b = data[cols]<int(const)
			elif op == '=':
				b = data[cols]==int(const)
			elif op == '<=':
				b = data[cols]<=int(const)
			elif op == '>=':
				b = data[cols]>=int(const)
			elif op == '!=':
				b = data[cols]!=int(const)
			l=l|b
		return data[l]

			# if cond[i] in table_name[0][0]:
			# 	cols.append(cond[i])
			# elif cond[i] in ['>','<','=','<=','>=']:
			# 	op.append(cond[i])
			# elif cond[i].isdigit():
			# 	const.append(cond[i])
	elif 'and' in s:
		cond=s.split('and')
		# cols=[]
		v=True
		l=[v]
		# const=[]
		for i in range(len(cond)):
			op=findrelop(cond[i])
			c=cond[i].split(op)
			if c[0] in data.dtype.names:
				# cols.append(c[0])
				cols=c[0]
				# const.append(c[1])
				const=c[1]
			else:
				# cols.append(c[1])
				cols=c[1]
				# const.append(c[0])
				const=c[0]

			if op == '>':
				b = (data[cols]>int(const))
			elif op == '<':
				b = data[cols]<int(const)
			elif op == '=':
				b = data[cols]==int(const)
			elif op == '<=':
				b = data[cols]<=int(const)
			elif op == '>=':
				b = data[cols]>=int(const)
			elif op == '!=':
				b = data[cols]!=int(const)
			l=l&b
		return data[l]
	else:
		if '>' in s:
			relop = '>'
			s=s.split('>')
		elif '<' in s:
			relop = '<'
			s=s.split('<')
		elif '=' in s:
			relop = '='
			s=s.split('=')
		elif '>=' in s:
			relop = '>='
			s=s.split('>=')
		elif '<=' in s:
			relop = '<='
			s=s.split('<=')
		elif '!=' in s:
			relop = '!='
			s=s.split('!=')
		
		if s[0] in table_name.dtype.names:
			col=s[0]
			const=s[1]
		else:
			col=s[1]
			const=s[0]
		if relop=='>':
			ans = data[data[col]>int(const)]
		elif relop=='<':
			ans = data[data[col]<int(const)]
		elif relop=='=':
			ans = data[data[col]==int(const)]
		elif relop=='>=':
			ans = data[data[col]<=int(const)]
		elif relop=='<=':
			ans = data[data[col]<=int(const)]
		elif relop=='!=':
			ans = data[data[col]!=int(const)]
		return ans
	# h = data.dtype.names
	# table = tabulate(ans, h, tablefmt="fancy_grid")
	# return ans
	
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
	l = data[colname].dtype
	flat_list = [item for sublist in u_ij for item in sublist]
	tab = np.array([totals,flat_list])
	t_matrix = zip(*tab)
	# np.rec.fromarrays(t_matrix.transpose(), dtype=l)
	# new_array = np.core.records.fromrecords(t_matrix,
    #                                     names='qty,pricerange',
    #                                     formats='<i8,S10')
	# v1 = np.array(t_matrix, dtype=l)
	# a[['x','y']].dtype
	# print(data[colname].dtype)
	# ll= np.array(t_matrix)
	# np.array([tuple(x) for x in ll],dtype=l)
	# new_array = np.array(t_matrix)
	# print(new_array)
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
		if(st.startswith("Hash")):
			res = st.replace("Hash","")
			res=res.strip('[,()]').split(',')
			table_name=res[0]
			table_name = table[table_name]
			col_name=res[1]
			d=Hash(table_name,col_name)
			table[params[0]]=d
		elif(st.startswith("Btree")):
			res = st.replace("Btree","")
			res=res.strip('[,()]').split(',')
			table_name=res[0]
			table_name = table[table_name]
			col_name=res[1]
			d=Btree(table_name,col_name)
			table[params[0]]=d
		elif(st.find("inputfromfile")!=-1):
			p = params[2]
			filename = p[p.find('(')+1:p.find(')')]+".txt"
			d=importfile(filename)
			table[params[0]]=d
			# print(table)
		elif(params[2].startswith("select")):
			p = params[2:]
			res = [sub.replace('select', "") for sub in p] 
			stripped_list = [j.split(',') for j in res]
			final_args = [[x.strip('[,()]') for x in l] for l in stripped_list]
			final_args = [[i for i in l if i] for l in final_args] 
			final_args = [j for sub in final_args for j in sub]
			table_name = table[final_args[0]]
			d=getSelect(table_name,final_args[1:])
			table[params[0]]=d

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
		elif(params[2].startswith("join")):
			p = params[2:]
			res = [sub.replace('join', "") for sub in p] 
			stripped_list = [j.split(',') for j in res]
			final_args = [[x.strip('[,()]') for x in l] for l in stripped_list]
			final_args = [[i for i in l if i] for l in final_args] 
			final_args = [j for sub in final_args for j in sub]
			table_name1 = table[final_args[0]]
			table_name2 = table[final_args[1]]
			args = final_args[2:]
			# length = len(final_args)
			d=getJoin(table_name1,table_name2,args)
			# table[params[0]]=d
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

		
			# d=Hash(table_name,column)
			# table[params[0]]=d
		


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

