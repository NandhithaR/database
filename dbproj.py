import numpy as np
from tabulate import tabulate
import numpy.lib.recfunctions as rfn
from operator import itemgetter
from itertools import groupby
from collections import defaultdict
# from BTrees.OOBTree import OOBTree
import re

hashmap={}
# btree = OOBTree()
collection=[]
counter = 0
def Hash(table_name,col_name):
	key, value = col_name, table_name[col_name]
	hashmap[key] = value

# def Btree(data,colname):

def getJoin(table1,table2,args):
	head1=table1.dtype.names
	head2=table2.dtype.names
	data1=table1
	data2=table2
	s = ""
	for i in args:
		s+=i
	#multiple join with arithmetic
	if ('and' in s) and ('+' in s or '-' in s or '*' in s or '/' in s):
		cond=s.split('and')
		cond = [x.strip(' ') for x in cond]
		cond = [x.strip('[,()]') for x in cond]
		# cols=[]
		v=True
		l=[]
		f=[]
		relop_list =[]
		for i in range(len(cond)):
			relop=findrelop(cond[i])
			# relop_list[i]=relop
			c=cond[i].split(relop)
			c=[x.strip(' ') for x in c]
			(left_file,left_col) = c[0].split(".")
			(left_file,left_col) = [x.strip(' ') for x in (left_file,left_col)]
			(right_file,right_col) = c[1].split(".")
			(right_file,right_col) = [x.strip(' ') for x in (right_file,right_col)]
			
			l=[]
			if('+' in s or '-' in s or '*' in s or '/' in s):
				if '+' in left_col:
					col =left_col.split('+')
					col=[x.strip(' ') for x in col]
					left_col=col[0]
					for j in range(len(data1[col[0]])):
						data1[col[0]][j] = data1[col[0]][j] + int(col[1])
				if '-' in left_col:
					col =left_col.split('-')
					col=[x.strip(' ') for x in col]
					left_col=col[0]
					for j in range(len(data1[col[0]])):
						data1[col[0]][j] = data1[col[0]][j] - int(col[1])
				if '/' in left_col:
					col =left_col.split('/')
					col=[x.strip(' ') for x in col]
					left_col=col[0]
					for j in range(len(data1[col[0]])):
						data1[col[0]][j] = data1[col[0]][j] / float(col[1])
				if '*' in left_col:
					col =left_col.split('*')
					col=[x.strip(' ') for x in col]
					left_col=col[0]
					for j in range(len(data1[col[0]])):
						data1[col[0]][j] = data1[col[0]][j] * float(col[1])

				if '+' in right_col:
					col =right_col.split('+')
					col=[x.strip(' ') for x in col]
					right_col=col[0]
					for j in range(len(data2[col[0]])):
						data2[col[0]][j] = data2[col[0]][j] + int(col[1])
				if '-' in right_col:
					col =right_col.split('-')
					col=[x.strip(' ') for x in col]
					right_col=col[0]
					for j in range(len(data2[col[0]])):
						data2[col[0]][j] = data2[col[0]][j] - int(col[1])
				if '/' in right_col:
					col =right_col.split('/')
					col=[x.strip(' ') for x in col]
					right_col=col[0]
					for j in range(len(data2[col[0]])):
						data2[col[0]][j] = data2[col[0]][j] / float(col[1])
				if '*' in right_col:
					col =right_col.split('*')
					col=[x.strip(' ') for x in col]
					right_col=col[0]
					for j in range(len(data2[col[0]])):
						data2[col[0]][j] = data2[col[0]][j] * float(col[1])
			l=[]
			for d2 in data2[right_col]:
				b_rows=[]
				for d1 in data1[left_col]:
					if relop == '<':
						b=(d1<d2)
					if relop == '<=':
						b=(d1<=d2)
					if relop == '>':
						b=(d1>d2)
					if relop == '>=':
						b=(d1>=d2)
					if relop == '=':
						b=(d1==d2)
					if relop == '!=':
						b=(d1!=d2)
					b_rows.append(b)
				l.append(b_rows)
			f.append(l)
		ll=np.array(f)
		for row in ll:
			# print(row)
			ll = ll & row
		# print(ll[0])
		l=[]
		for row in ll[0]:
			l.append(np.bitwise_or.reduce(row))
		# print(l)
		# d = np.array(l)			
	#single join with arithmetic
	elif ('+' in s or '-' in s or '*' in s or '/' in s):
		relop = findrelop(s)
		(left,right) = s.split(relop)
		(left,right) = [x.strip(' ') for x in (left,right)]
		(left_file,left_col) = left.split(".")
		(right_file,right_col) = right.split(".")
		if('+' in s or '-' in s or '*' in s or '/' in s):
			if '+' in left_col:
				col =left_col.split('+')
				left_col=col[0]
				for i in range(len(data1[col[0]])):
					data1[col[0]][i] = data1[col[0]][i] + int(col[1])
			if '-' in left_col:
				col =left_col.split('-')
				left_col=col[0]
				for i in range(len(data1[col[0]])):
					data1[col[0]][i] = data1[col[0]][i] - int(col[1])
			if '/' in left_col:
				col =left_col.split('/')
				left_col=col[0]
				for i in range(len(data1[col[0]])):
					data1[col[0]][i] = data1[col[0]][i] / float(col[1])
			if '*' in left_col:
				col =left_col.split('*')
				left_col=col[0]
				for i in range(len(data1[col[0]])):
					data1[col[0]][i] = data1[col[0]][i] * float(col[1])

		if('+' in s or '-' in s or '*' in s or '/' in s):
			if '+' in right_col:
				col =right_col.split('+')
				right_col=col[0]
				for i in range(len(data2[col[0]])):
					data2[col[0]][i] = data2[col[0]][i] + int(col[1])
			if '-' in right_col:
				col =right_col.split('-')
				right_col=col[0]
				for i in range(len(data2[col[0]])):
					data2[col[0]][i] = data2[col[0]][i] - int(col[1])
			if '/' in right_col:
				col =right_col.split('/')
				right_col=col[0]
				for i in range(len(data2[col[0]])):
					data2[col[0]][i] = data2[col[0]][i] / float(col[1])
			if '*' in right_col:
				col =right_col.split('*')
				right_col=col[0]
				for i in range(len(data2[col[0]])):
					data2[col[0]][i] = data2[col[0]][i] * float(col[1])
		l=[]
		for d2 in data2[right_col]:
			for d1 in data1[left_col]:
				if relop == '<':
					b=(d1<d2)
					if(b==True):
						break
				if relop == '<=':
					b=(d1<=d2)
					if(b==True):
						break
				if relop == '>':
					b=(d1>d2)
					if(b==True):
						break
				if relop == '>=':
					b=(d1>=d2)
					if(b==True):
						break
				if relop == '=':
					b=(d1==d2)
					if(b==True):
						break
				if relop == '!=':
					b=(d1!=d2)
					if(b==True):
						break
			l.append(b)
		# print(l)
		
	#multiple join
	elif 'and' in s:
		cond=s.split('and')
		cond = [x.strip(' ') for x in cond]
		cond = [x.strip('[,()]') for x in cond]
		print(cond)
		cols=[]
		v=True
		l=[]
		f=[]
		column_left_list = []
		column_right_list = []
		relop_list =[]
		for i in range(len(cond)):
			relop=findrelop(cond[i])
			# relop_list[i]=relop
			c=cond[i].split(relop)
			(left_file,left_col) = c[0].split(".")
			(left_file,left_col) = [x.strip(' ') for x in (left_file,left_col)]
			(right_file,right_col) = c[1].split(".")
			(right_file,right_col) = [x.strip(' ') for x in (right_file,right_col)]
			l=[]
			for d2 in data2[right_col]:
				b_rows=[]
				for d1 in data1[left_col]:
					if relop == '<':
						b=(d1<d2)
					if relop == '<=':
						b=(d1<=d2)
					if relop == '>':
						b=(d1>d2)
					if relop == '>=':
						b=(d1>=d2)
					if relop == '=':
						b=(d1==d2)
					if relop == '!=':
						b=(d1!=d2)
					b_rows.append(b)
				# print(b_rows)
				# ll = np.array(b_rows)
				# if len(l)==0:
				# 	l=np.array(ll)
				# else:
				# 	l=l&ll
				# print(l)
				l.append(b_rows)
			f.append(l)
			#print(l)
		#print(f)
		ll=np.array(f)
		for row in ll:
			# print(row)
			ll = ll & row
		# print(ll[0])
		l=[]
		for row in ll[0]:
			l.append(np.bitwise_or.reduce(row))

	#single join
	else:
		relop = findrelop(s)
		(left,right) = s.split(relop)
		(left,right) = [x.strip(' ') for x in (left,right)]
		(left_file,left_col) = left.split(".")
		(right_file,right_col) = right.split(".")
		print(right_col)
		b=True
		l=[]
		value=[]
		for d2 in data2[right_col]:
			for d1 in data1[left_col]:
				if relop == '<':
					b=(d1<d2)
					if(b==True):
						break
				if relop == '<=':
					b=(d1<=d2)
					if(b==True):
						break
				if relop == '>':
					b=(d1>d2)
					if(b==True):
						break
				if relop == '>=':
					b=(d1>=d2)
					if(b==True):
						break
				if relop == '=':
					b=(d1==d2)
					if(b==True):
						break
				if relop == '!=':
					b=(d1!=d2)
					if(b==True):
						break
			l.append(b)
		print(l)
	second = []
	first = []
	for i in data1:
		first.append(i)
	for t in range(len(l)):
		if l[t]:
			second.append(data2[0:][t])
		# else:
		# 	second.append([0] * len(data2[0]))
		#change the dtypes.names of the two arrays and then merge them
	first_dtype_name=[]
	second_dtype_name = []
	for i in data1.dtype.names:
		first_dtype_name.append(str(left_file)+'_'+str(i))
	for i in data2.dtype.names:
		second_dtype_name.append(str(right_file)+'_'+str(i))

	first_final = np.array(first, dtype=data1.dtype)
	first_final.dtype.names = first_dtype_name

	second_final = np.array(second, dtype=data2.dtype)
	second_final.dtype.names = second_dtype_name
		
	data=[first_final,second_final]

	d=rfn.merge_arrays([first_final,second_final])
	print(d)
	return rfn.merge_arrays([second_final,first_final])
		
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
	c = np.savetxt('geekfile1.txt', x, delimiter ='|') 
	a = open("geekfile1.txt", 'r')# open file in read mode 
	print("the file contains:") 
	print(a.read()) 
	return a

#sort by columns
def sortColumns(table_name,colname):
	data = table_name
	data.sort(order=colname)
	print(data)
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
	print(table)
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
		cond = [x.strip(' ') for x in cond]
		cond = [x.strip('[,()]') for x in cond]
		l=[False]
		for i in range(len(cond)):
			op=findrelop(cond[i])
			c=cond[i].split(op)
			c = [x.strip(' ') for x in c]
			if c[0].isdigit():
				cols=c[1]
				const=c[0]
			else:
				cols=c[0]
				const=c[1]
			if '+' in cols:
				col =cols.split('+')
				col = [x.strip(' ') for x in col]
				cols=col[0]
				for i in range(len(data[col[0]])):
					data[col[0]][i] = data[col[0]][i] + int(col[1])
			if '-' in cols:
				col =cols.split('-')
				col = [x.strip(' ') for x in col]
				cols=col[0]
				for i in range(len(data[col[0]])):
					data[col[0]][i] = data[col[0]][i] - int(col[1])
			if '/' in cols:
				col =cols.split('/')
				col = [x.strip(' ') for x in col]
				cols=col[0]
				for i in range(len(data[col[0]])):
					data[col[0]][i] = data[col[0]][i] / float(col[1])
			if '*' in cols:
				col =cols.split('*')
				col = [x.strip(' ') for x in col]
				cols=col[0]
				for i in range(len(data[col[0]])):
					data[col[0]][i] = data[col[0]][i] * float(col[1])
			print(col[0])
			if op == '>':
				b = (data[cols]>int(const))
				print(b)
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
		print(data[l])
		return data[l]
		
	elif ('and' in s) and ('+' in s or '-' in s or '*' in s or '/' in s):
		cond=s.split('and')
		cond = [x.strip(' ') for x in cond]
		cond = [x.strip('[,()]') for x in cond]
		l=[True]
		for i in range(len(cond)):
			op=findrelop(cond[i])
			c=cond[i].split(op)
			c = [x.strip(' ') for x in c]
			if c[0].isdigit():
				cols=c[1]
				const=c[0]
			else:
				cols=c[0]
				const=c[1]
			if '+' in cols:
				col =cols.split('+')
				col = [x.strip(' ') for x in col]
				cols=col[0]
				for i in range(len(data[col[0]])):
					data[col[0]][i] = data[col[0]][i] + int(col[1])
			if '-' in cols:
				col =cols.split('-')
				col = [x.strip(' ') for x in col]
				cols=col[0]
				for i in range(len(data[col[0]])):
					data[col[0]][i] = data[col[0]][i] - int(col[1])
			if '/' in cols:
				col =cols.split('/')
				col = [x.strip(' ') for x in col]
				cols=col[0]
				for i in range(len(data[col[0]])):
					data[col[0]][i] = data[col[0]][i] / float(col[1])
			if '*' in cols:
				col =cols.split('*')
				col = [x.strip(' ') for x in col]
				cols=col[0]
				for i in range(len(data[col[0]])):
					data[col[0]][i] = data[col[0]][i] * float(col[1])
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
		print(data[l])
		return data[l]
	elif '+' in s or '-' in s or '*' in s or '/' in s:
		# s=data[data[col]>int(r_const)]
		# print(s)
		if '>' in s:
			relop = '>'
			s=s.split('>')
			s = [x.strip(' ') for x in s]
		elif '<' in s:
			relop = '<'
			s=s.split('<')
			s = [x.strip(' ') for x in s]
		elif '=' in s:
			relop = '='
			s=s.split('=')
			s = [x.strip(' ') for x in s]
		elif '>=' in s:
			relop = '>='
			s=s.split('>=')
			s = [x.strip(' ') for x in s]
		elif '<=' in s:
			relop = '<='
			s=s.split('<=')
			s = [x.strip(' ') for x in s]
		elif '!=' in s:
			relop = '!='
			s=s.split('!=')
			s = [x.strip(' ') for x in s]
		if s[0].isdigit():
			const=s[0]
			col=s[1]
		else:
			const=s[1]
			col=s[0]
		#split col-name arithmetic operation and const
		if '+' in col:
			col =col.split('+')
			col = [x.strip(' ') for x in col]
			for i in range(len(data[col[0]])):
				data[col[0]][i] = data[col[0]][i] + int(col[1])
		if '-' in col:
			col =col.split('-')
			col = [x.strip(' ') for x in col]
			for i in range(len(data[col[0]])):
				data[col[0]][i] = data[col[0]][i] - int(col[1])
		if '/' in col:
			col =col.split('/')
			col = [x.strip(' ') for x in col]
			for i in range(len(data[col[0]])):
				data[col[0]][i] = data[col[0]][i] / float(col[1])
		if '*' in col:
			col =col.split('*')
			col = [x.strip(' ') for x in col]
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
		print(ans)
		return ans
	elif 'or' in s:
		cond=s.split('or')
		cond = [x.strip(' ') for x in cond]
		cond = [x.strip('[,()]') for x in cond]
		v=False
		l=[v]
		# const=[]
		for i in range(len(cond)):
			op=findrelop(cond[i])
			c=cond[i].split(op)
			c = [x.strip(' ') for x in c]
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
			# print(l)
		print(data[l])
		return data[l]

			# if cond[i] in table_name[0][0]:
			# 	cols.append(cond[i])
			# elif cond[i] in ['>','<','=','<=','>=']:
			# 	op.append(cond[i])
			# elif cond[i].isdigit():
			# 	const.append(cond[i])
	elif 'and' in s:
		cond=s.split('and')
		cond = [x.strip(' ') for x in cond]
		cond = [x.strip('[,()]') for x in cond]
		# cols=[]
		v=True
		l=[v]
		# const=[]
		for i in range(len(cond)):
			op=findrelop(cond[i])
			c=cond[i].split(op)
			c = [x.strip(' ') for x in c]
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
		print(data[l])
		return data[l]
	else:
		if '>' in s:
			relop = '>'
			s=s.split('>')
			s = [x.strip(' ') for x in s]
		elif '<' in s:
			relop = '<'
			s=s.split('<')
			s = [x.strip(' ') for x in s]
		elif '=' in s:
			relop = '='
			s=s.split('=')
			s = [x.strip(' ') for x in s]
		elif '>=' in s:
			relop = '>='
			s=s.split('>=')
			s = [x.strip(' ') for x in s]
		elif '<=' in s:
			relop = '<='
			s=s.split('<=')
			s = [x.strip(' ') for x in s]
		elif '!=' in s:
			relop = '!='
			s=s.split('!=')
			s = [x.strip(' ') for x in s]
		
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
			#check if in hashmap
			# if(col in hashmap):
			# 	hashmap.get()
			ans = data[data[col]==int(const)]
		elif relop=='>=':
			ans = data[data[col]<=int(const)]
		elif relop=='<=':
			ans = data[data[col]<=int(const)]
		elif relop=='!=':
			ans = data[data[col]!=int(const)]
		print(ans)
		return ans
	# h = data.dtype.names
	# table = tabulate(ans, h, tablefmt="fancy_grid")
	# return ans
	
#selection, projection, count, sum and avg aggregates
def getAverage(table_name,colname):
	data=table_name
	average=np.mean(data[colname])
	print(average)
	return average
def getCount(table_name):
	num_rows = np.shape(table_name)[0]
	print(num_rows)
	return num_rows

def moving_average(table_name,colname, n):
	data = table_name
	ret = np.cumsum(data[colname[0]], dtype=float)
	n=int(n)
	ret[n:] = ret[n:] - ret[:-n]
	print(ret[n:])
	return ret[n - 1:] / n

def moving_sum(table_name,colname, n):
	data = table_name
	ret = np.cumsum(data[colname[0]], dtype=float)
	n=int(n)
	ret[n:] = ret[n:] - ret[:-n]
	print(ret[n-1:])
	return ret[n - 1:]

def countGroup(table_name, colname):
    data=table_name
    s=colname[0]
    h=colname
    d=[]
    for i in colname:
        d.append(data[i])
    u_ij, inv_ij = np.unique(data[h[1:]], return_inverse=True)
    # Create a totals array. You could do the fancy ijv_dtype thing if you wanted.
    totals=np.zeros(len(u_ij))
    for i in inv_ij:
        totals[i] = totals[i] + 1
    flat_list = [item for sublist in u_ij for item in sublist]
    tab = [totals,flat_list]
    t_matrix = zip(*tab)
    t = [h,t_matrix]
    to_return = [totals,u_ij]
    table = tabulate(t_matrix, h, tablefmt="fancy_grid")
    print(table) 
    return table

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
	print(s)
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
	print(table)
	return totals

def concat(table_name1,table_name2):
    data1=table_name1
    data2=table_name2
    c = np.ma.concatenate((data1, data2), axis=None)
    t_matrix = zip(*c)
    # tabulate data
    table = tabulate(c, tablefmt="fancy_grid")
    print (table)
    return table

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
		params=st.split(":=")
		params = [x.strip(' ') for x in params]
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
			p = params[1]
			filename = p[p.find('(')+1:p.find(')')]+".txt"
			d=importfile(filename)
			table[params[0]]=d
		elif(params[1].startswith("select")):
			p = params[1:]
			res = [sub.replace('select', "") for sub in p] 
			stripped_list = [j.split(',') for j in res]
			final_args = [[x.strip('[,()]') for x in l] for l in stripped_list]
			final_args = [[i for i in l if i] for l in final_args] 
			final_args = [j for sub in final_args for j in sub]
			final_args = [x.strip(' ') for x in final_args]
			table_name = table[final_args[0]]
			d=getSelect(table_name,final_args[1:])
			table[params[0]]=d

		elif(params[1].startswith("project")):
			p = params[1:]
			res = [sub.replace('project', "") for sub in p] 
			stripped_list = [j.split(',') for j in res]
			final_args = [[x.strip('[,()]') for x in l] for l in stripped_list]
			final_args = [[i for i in l if i] for l in final_args] 
			final_args = [j for sub in final_args for j in sub]
			final_args = [x.strip(' ') for x in final_args]
			table_name = table[final_args[0]]
			column_names = final_args[1:]
			d=projection(table_name,column_names)
			table[params[0]]=d

		elif(params[1].startswith("avg")):
			p = params[1:]
			res = [sub.replace('avg', "") for sub in p] 
			stripped_list = [j.split(',') for j in res]
			final_args = [[x.strip('[,()]') for x in l] for l in stripped_list]
			final_args = [[i for i in l if i] for l in final_args] 
			final_args = [j for sub in final_args for j in sub]
			final_args = [x.strip(' ') for x in final_args]
			table_name = table[final_args[0]]
			column_names = final_args[1:]
			d=getAverage(table_name,column_names[0])
			table[params[0]]=d

		elif(params[1].startswith("sumgroup")):
			p = params[1:]
			res = [sub.replace('sumgroup', "") for sub in p] 
			stripped_list = [j.split(',') for j in res]
			final_args = [[x.strip('[,()]') for x in l] for l in stripped_list]
			final_args = [[i for i in l if i] for l in final_args] 
			final_args = [j for sub in final_args for j in sub]
			final_args = [x.strip(' ') for x in final_args]
			table_name = table[final_args[0]]
			column_names = final_args[1:]
			d=sumGroup(table_name,column_names)
			table[params[0]]=d
		elif(params[1].startswith("join")):
			p = params[1:]
			res = [sub.replace('join', "") for sub in p] 
			stripped_list = [j.split(',') for j in res]
			final_args = [[x.strip('[,()]') for x in l] for l in stripped_list]
			final_args = [[i for i in l if i] for l in final_args] 
			final_args = [j for sub in final_args for j in sub]
			final_args = [x.strip(' ') for x in final_args]
			table_name1 = table[final_args[0]]
			table_name2 = table[final_args[1]]
			args = final_args[2:]
			d=getJoin(table_name1,table_name2,args)
			table[params[0]]=d

		# # elif(params[2].startswith("avggroup")):
		# # 	p = params[2:]
		# # 	table_name = table[(p[0].split('('))[1].split(',')[0]]
		# # 	args = params[3:]
		# # 	final_args = [j.strip('[,()]') for j in args]
		# # 	final_args = [i for i in final_args if i] 
		# # 	d=avgGroup(table_name[1],final_args)
		# # 	table[params[0]]=d

		elif(params[1].startswith("movavg")):
			p = params[1:]
			res = [sub.replace('movavg', "") for sub in p] 
			stripped_list = [j.split(',') for j in res]
			final_args = [[x.strip('[,()]') for x in l] for l in stripped_list]
			final_args = [[i for i in l if i] for l in final_args] 
			final_args = [j for sub in final_args for j in sub]
			final_args = [x.strip(' ') for x in final_args]
			length = len(final_args)
			table_name = table[final_args[0]]
			d=moving_average(table_name,final_args[1:length-1],final_args[length-1])
			table[params[0]]=d

		elif(params[1].startswith("movsum")):
			p = params[1:]
			res = [sub.replace('movsum', "") for sub in p] 
			stripped_list = [j.split(',') for j in res]
			final_args = [[x.strip('[,()]') for x in l] for l in stripped_list]
			final_args = [[i for i in l if i] for l in final_args] 
			final_args = [j for sub in final_args for j in sub]
			final_args = [x.strip(' ') for x in final_args]
			length = len(final_args)
			table_name = table[final_args[0]]
			d=moving_sum(table_name,final_args[1:length-1],final_args[length-1])
			table[params[0]]=d

		elif(params[1].startswith("sort")):
			p = params[1:]
			res = [sub.replace('sort', "") for sub in p] 
			stripped_list = [j.split(',') for j in res]
			final_args = [[x.strip('[,()]') for x in l] for l in stripped_list]
			final_args = [[i for i in l if i] for l in final_args] 
			final_args = [j for sub in final_args for j in sub]
			final_args = [x.strip(' ') for x in final_args]
			table_name = table[final_args[0]]
			d=sortColumns(table_name,final_args[1:])

		elif(params[1].startswith("countgroup")):
			p = params[1:]
			res = [sub.replace('countgroup', "") for sub in p]
			stripped_list = [j.split(',') for j in res]
			final_args = [[x.strip('[,()]') for x in l] for l in stripped_list]
			final_args = [[i for i in l if i] for l in final_args]
			final_args = [j for sub in final_args for j in sub]
			final_args = [x.strip(' ') for x in final_args]
			table_name = table[final_args[0]]
			column_names = final_args[1:]
			d=countGroup(table_name,column_names)
			table[params[0]]=d
			
		elif(params[1].startswith("count")):
			p = params[1]
			table_name = table[p[p.find('(')+1:p.find(')')]]
			d = getCount(table_name)
			print(d)
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

