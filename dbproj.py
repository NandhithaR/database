import numpy as np
from tabulate import tabulate
import numpy.lib.recfunctions as rfn
from operator import itemgetter
from itertools import groupby
from collections import defaultdict
from BTrees.OOBTree import OOBTree
import re
import copy
import time

hashmap={}
btree = OOBTree()
collection_hash=[]
collection_btree=[]
hash_keys = {}
btree_keys = {}

def HashTable(tname,table_name,col_name):
	hashmap = defaultdict(lambda:[])
	collection_hash = table_name
	for row in range(len(collection_hash)):
		hashmap[collection_hash[row][col_name]].append(row)
	hash_keys[tname+ '.' + col_name] = hashmap

def Hash(tname, col_name, val):
	hashmap = hash_keys[tname + '.' + col_name]
	matched_rows = hashmap[float(val)]
	print(matched_rows)
	return matched_rows

def BtreesStruc(tname,table_name,col_name):
	hashmap = defaultdict(lambda:[])
	collection_btree = table_name
	for row in range(len(collection_btree)):
		hashmap[collection_btree[row][col_name]].append(row)
	btree_keys[tname+ '.' + col_name] = hashmap
	btree.update(hashmap)

def Btrees(tname, col_name, val):
	hashmap = btree_keys[tname + '.' + col_name]
	matched_rows = hashmap[float(val)]
	print(matched_rows)
	return matched_rows

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
		ll=[]
		relop_list =[]
		for i in range(len(cond)):
			relop=findrelop(cond[i])
			c=cond[i].split(relop)
			c=[x.strip(' ') for x in c]
			(left_file,left_col) = c[0].split(".")
			(left_file,left_col) = [x.strip(' ') for x in (left_file,left_col)]
			(right_file,right_col) = c[1].split(".")
			(right_file,right_col) = [x.strip(' ') for x in (right_file,right_col)]
			temp1 = []
			temp2 = []
			l=[]
			if('+' in s or '-' in s or '*' in s or '/' in s):
				if '+' in left_col:
					col =left_col.split('+')
					col=[x.strip(' ') for x in col]
					left_col=col[0]
					temp1 = data1[left_col]
					for k in range(len(data1[col[0]])):
						temp1[k] = data1[col[0]][k] + int(col[1])
					for j in range(len(data1[col[0]])):
						temp1[j] = data1[col[0]][j] + int(col[1])
				if '-' in left_col:
					col =left_col.split('-')
					col=[x.strip(' ') for x in col]
					left_col=col[0]
					temp1 = data1[left_col]
					for k in range(len(data1[col[0]])):
						temp1[k] = data1[col[0]][k] + int(col[1])
					for j in range(len(data1[col[0]])):
						temp1[j] = data1[col[0]][j] - int(col[1])
				if '/' in left_col:
					col =left_col.split('/')
					col=[x.strip(' ') for x in col]
					left_col=col[0]
					temp1 = data1[left_col]
					for k in range(len(data1[col[0]])):
						temp1[k] = data1[col[0]][k] + int(col[1])
					for j in range(len(data1[col[0]])):
						temp1[j] = data1[col[0]][j] / float(col[1])
				if '*' in left_col:
					col =left_col.split('*')
					col=[x.strip(' ') for x in col]
					left_col=col[0]
					temp1 = data1[left_col]
					for k in range(len(data1[col[0]])):
						temp1[k] = data1[col[0]][k] + int(col[1])
					for j in range(len(data1[col[0]])):
						temp1[j] = data1[col[0]][j] * float(col[1])

				if '+' in right_col:
					col =right_col.split('+')
					col=[x.strip(' ') for x in col]
					right_col=col[0]
					temp2 = data2[right_col]
					for k in range(len(data2[col[0]])):
						temp2[k] = data2[col[0]][k] + int(col[1])
					for j in range(len(data2[col[0]])):
						temp2[j] = data2[col[0]][j] + int(col[1])
				if '-' in right_col:
					col =right_col.split('-')
					col=[x.strip(' ') for x in col]
					right_col=col[0]
					temp2 = data2[right_col]
					for k in range(len(data2[col[0]])):
						temp2[k] = data2[col[0]][k] + int(col[1])
					for j in range(len(data2[col[0]])):
						temp2[j] = data2[col[0]][j] - int(col[1])
				if '/' in right_col:
					col =right_col.split('/')
					col=[x.strip(' ') for x in col]
					right_col=col[0]
					temp2 = data2[right_col]
					for k in range(len(data2[col[0]])):
						temp2[k] = data2[col[0]][k] + int(col[1])
					for j in range(len(data2[col[0]])):
						temp2[j] = data2[col[0]][j] / float(col[1])
				if '*' in right_col:
					col =right_col.split('*')
					col=[x.strip(' ') for x in col]
					right_col=col[0]
					temp2 = data2[right_col]
					for k in range(len(data2[col[0]])):
						temp2[k] = data2[col[0]][k] + int(col[1])
					for j in range(len(data2[col[0]])):
						temp2[j] = data2[col[0]][j] * float(col[1])
				if ('+' not in left_col) or ('-' not in left_col) or ('/' not in left_col) or ('*' not in left_col):
					temp1 = data1[left_col]
				if ('+' not in right_col) or ('-' not in right_col) or ('/' not in right_col) or ('*' not in right_col):
					temp2 = data2[right_col]
			l=[]
			for index_left in range(len(data1[left_col])):
				row_join = []
				b_rows=[]
				count = 0
				for index_right in range(len(data2[right_col])):
					if relop == '<':
						b=(temp1[index_left]<temp2[index_right])
					elif relop == '<=':
						b=(temp1[index_left]<=temp2[index_right])
					elif relop == '>':
						b=(temp1[index_left]>temp2[index_right])
					elif relop == '>=':
						b=(temp1[index_left]>=temp2[index_right])
					elif relop == '=':
						b=(temp1[index_left]==temp2[index_right])
					elif relop == '!=':
						b=(temp1[index_left]!=temp2[index_right])
					b_rows.append(b)
				l.append(b_rows)
			if len(ll)==0:
				ll = np.array(l)
			else:
				ll=ll&l

			# print(relop)
			# print(ll)
			final_Count = 0
			for index_l in range(len(data1[left_col])):
				row_join = []
				count = 0
				for index_r in range(len(data2[right_col])):
					if(ll[index_l][index_r]):
						#TBD: Change column names
						first_dtype = {}
						second_dtype = {}
						for col in data1.dtype.names:
							first_dtype[col] = str(left_file)+'_'+str(col)
						for col in data2.dtype.names:
							second_dtype[col] = str(right_file)+'_'+str(col)
						new_data1 = rfn.rename_fields(data1[index_l], first_dtype)
						new_data2 = rfn.rename_fields(data2[index_r], second_dtype)
						if count:
							row_join = np.concatenate((row_join, rfn.merge_arrays((new_data1,new_data2), flatten=True)))
						else:
							row_join = rfn.merge_arrays((new_data1,new_data2), flatten=True)
							count=count+1
				if len(row_join):
					if final_Count:
						join_ans = np.concatenate((join_ans, row_join))
					else:
						join_ans = rfn.merge_arrays((new_data1,new_data2), flatten=True)
						final_Count=final_Count+1
	#single join with arithmetic
	elif ('+' in s or '-' in s or '*' in s or '/' in s):
		relop = findrelop(s)
		(left,right) = s.split(relop)
		(left,right) = [x.strip(' ') for x in (left,right)]
		(left_file,left_col) = left.split(".")
		(right_file,right_col) = right.split(".")
		temp1 = []
		temp2 = []
		if('+' in s or '-' in s or '*' in s or '/' in s):
			if '+' in left_col:
				col =left_col.split('+')
				left_col=col[0]
				temp1 = copy.deepcopy(data1[left_col])
				for i in range(len(data1[col[0]])):
					temp1[i] = data1[col[0]][i] + float(col[1])
			elif '-' in left_col:
				col =left_col.split('-')
				left_col=col[0]
				# for i in range(len(data1[col[0]])):
				# 	temp1[i] = data1[col[0]][i]
				temp1 = copy.deepcopy(data1[left_col])
				for i in range(len(data1[col[0]])):
					temp1[i] = data1[col[0]][i] - float(col[1])
			elif '/' in left_col:
				col =left_col.split('/')
				left_col=col[0]
				temp1 = copy.deepcopy(data1[left_col])
				for i in range(len(data1[col[0]])):
					temp1[i] = data1[col[0]][i] / float(col[1])
			elif '*' in left_col:
				col =left_col.split('*')
				left_col=col[0]
				temp1 = copy.deepcopy(data1[left_col])
				for i in range(len(data1[col[0]])):
					temp1[i] = data1[col[0]][i] * float(col[1])
			else:
				temp1 = copy.deepcopy(data1[left_col])

		if('+' in s or '-' in s or '*' in s or '/' in s):
			if '+' in right_col:
				col =right_col.split('+')
				right_col=col[0]
				temp2 = data2[right_col]
				for i in range(len(data2[col[0]])):
					temp2[i] = data2[col[0]][i] + float(col[1])
			elif '-' in right_col:
				col =right_col.split('-')
				right_col=col[0]
				temp2 = data2[right_col]
				for i in range(len(data2[col[0]])):
					temp2[i] = data2[col[0]][i] - float(col[1])
			elif '/' in right_col:
				col =right_col.split('/')
				right_col=col[0]
				temp2 = data2[right_col]
				for i in range(len(data2[col[0]])):
					temp2[i] = data2[col[0]][i] / float(col[1])
			elif '*' in right_col:
				col =right_col.split('*')
				right_col=col[0]
				temp2 = data2[right_col]
				for i in range(len(data2[col[0]])):
					temp2[i] = data2[col[0]][i] * float(col[1])
			else:
				temp2 = data2[right_col]

		l=[]
		arrays_left=[]
		arrays_right=[]
		join_ans =[]
		final_Count = 0
		for i in range(len(data1[left_col])):
			b_rows=[]
			row_join = []
			count = 0
			for j in range(len(data2[right_col])):
				if relop == '<':
					b=(temp1[i]<temp2[j])
				elif relop == '<=':
					b=(temp1[i]<=temp2[j])
				elif relop == '>':
					b=(temp1[i]>temp2[j])
				elif relop == '>=':
					b=(temp1[i]>=temp2[j])
				elif relop == '=':
					b=(temp1[i]==temp2[j])
				elif relop == '!=':
					b=(temp1[i]!=temp2[j])
				
				if b:
					#TBD: Change column names
					first_dtype = {}
					second_dtype = {}
					for col in data1.dtype.names:
						first_dtype[col] = str(left_file)+'_'+str(col)
					for col in data2.dtype.names:
						second_dtype[col] = str(right_file)+'_'+str(col)
					new_data1 = rfn.rename_fields(data1[i], first_dtype)
					new_data2 = rfn.rename_fields(data2[j], second_dtype)
					if count:
						row_join = np.concatenate((row_join, rfn.merge_arrays((new_data1,new_data2), flatten=True)))
					else:
						row_join = rfn.merge_arrays((new_data1,new_data2), flatten=True)
						count=count+1
			if len(row_join):
				if final_Count:
					join_ans = np.concatenate((join_ans, row_join))
				else:
					join_ans = rfn.merge_arrays((new_data1,new_data2), flatten=True)
					final_Count=final_Count+1
		
	#multiple join
	elif 'and' in s:
		cond=s.split('and')
		cond = [x.strip(' ') for x in cond]
		cond = [x.strip('[,()]') for x in cond]
		cols=[]
		v=True
		
		ll=[]
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
			for i in range(len(data1[left_col])):
				row_join = []
				b_rows=[]
				count = 0
				for j in range(len(data2[right_col])):
					if relop == '<':
						b=(data1[i][left_col]<data2[j][right_col])
					elif relop == '<=':
						b=(data1[i][left_col]<=data2[j][right_col])
					elif relop == '>':
						b=(data1[i][left_col]>data2[j][right_col])
					elif relop == '>=':
						b=(data1[i][left_col]>=data2[j][right_col])
					elif relop == '=':
						b=(data1[i][left_col]==data2[j][right_col])
					elif relop == '!=':
						b=(data1[i][left_col]!=data2[j][right_col])
					b_rows.append(b)
				l.append(b_rows)
			if len(ll)==0:
				ll = np.array(l)
			else:
				ll=ll&l
			final_Count = 0
			for k in range(len(data1[left_col])):
				row_join = []
				count = 0
				for li in range(len(data2[right_col])):
					if(ll[k][li]):
						#TBD: Change column names
						first_dtype = {}
						second_dtype = {}
						for col in data1.dtype.names:
							first_dtype[col] = str(left_file)+'_'+str(col)
						for col in data2.dtype.names:
							second_dtype[col] = str(right_file)+'_'+str(col)
						new_data1 = rfn.rename_fields(data1[k], first_dtype)
						new_data2 = rfn.rename_fields(data2[li], second_dtype)
						if count:
							row_join = np.concatenate((row_join, rfn.merge_arrays((new_data1,new_data2), flatten=True)))
						else:
							row_join = rfn.merge_arrays((new_data1,new_data2), flatten=True)
							count=count+1
				if len(row_join):
					if final_Count:
						join_ans = np.concatenate((join_ans, row_join))
					else:
						join_ans = rfn.merge_arrays((new_data1,new_data2), flatten=True)
						final_Count=final_Count+1

		# join_ans=[]
		# print(ll)

	#single join
	else:
		relop = findrelop(s)
		(left,right) = s.split(relop)
		(left,right) = [x.strip(' ') for x in (left,right)]
		(left_file,left_col) = left.split(".")
		(right_file,right_col) = right.split(".")
		b=True
		l=[]
		f=[]
		value=[]
		arrays_left=[]
		arrays_right=[]
		join_ans =[]
		final_Count = 0
		for i in range(len(data1[left_col])):
			b_rows=[]
			row_join = []
			count = 0
			for j in range(len(data2[right_col])):
				if relop == '<':
					b=(data1[i][left_col]<data2[j][right_col])
				elif relop == '<=':
					b=(data1[i][left_col]<=data2[j][right_col])
				elif relop == '>':
					b=(data1[i][left_col]>data2[j][right_col])
				elif relop == '>=':
					b=(data1[i][left_col]>=data2[j][right_col])
				elif relop == '=':
					b=(data1[i][left_col]==data2[j][right_col])
				elif relop == '!=':
					b=(data1[i][left_col]!=data2[j][right_col])
				
				if b:
					#TBD: Change column names
					first_dtype = {}
					second_dtype = {}
					for col in data1.dtype.names:
						first_dtype[col] = str(left_file)+'_'+str(col)
					for col in data2.dtype.names:
						second_dtype[col] = str(right_file)+'_'+str(col)
					new_data1 = rfn.rename_fields(data1[i], first_dtype)
					new_data2 = rfn.rename_fields(data2[j], second_dtype)
					if count:
						row_join = np.concatenate((row_join, rfn.merge_arrays((new_data1,new_data2), flatten=True)))
					else:
						row_join = rfn.merge_arrays((new_data1,new_data2), flatten=True)
						count=count+1
			if len(row_join):
				if final_Count:
					join_ans = np.concatenate((join_ans, row_join))
				else:
					join_ans = rfn.merge_arrays((new_data1,new_data2), flatten=True)
					final_Count=final_Count+1
	join_ans_headers= join_ans.dtype.names
	headers = []
	for i in join_ans_headers:
		headers.append(i)
	# t_matrix = zip(*data)
	table = tabulate(join_ans, headers, tablefmt="fancy_grid")
	print(table)
	d=join_ans
	return d
		
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
	dtypes=[file_array.dtype]
	headers=[file_array.dtype.names]
	return file_array
	

def exportfile(table_name,filename):
	# x = np.arange(0, 10, 1)
	c = np.savetxt(filename, table_name, delimiter ='|') 
	# a = open(filename, 'r')# open file in read mode 
	# print("the file contains:") 
	# print(a.read()) 
	# return a

#sort by columns
def sortColumns(table_name,colname):
	data = table_name
	data.sort(order=colname)
	print(data)
	h = data.dtype.names
	headers = []
	for i in h:
		headers.append(i)
	table = tabulate(data, headers, tablefmt="fancy_grid")
	print(table)
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

def getSelect(tname,table_name,args):
	s = ""
	data=table_name
	for i in args:
		s+=i
	if ('or' in s) and ('+' in s or '-' in s or '*' in s or '/' in s):
		cond=s.split('or')
		cond = [x.strip(' ') for x in cond]
		cond = [x.strip('[,()]') for x in cond]
		l=[]
		temp = []
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
				temp = copy.deepcopy(data[col[0]])
				for i in range(len(data[col[0]])):
					temp[i] = data[col[0]][i] + int(col[1])
			elif '-' in cols:
				col =cols.split('-')
				col = [x.strip(' ') for x in col]
				cols=col[0]
				temp = copy.deepcopy(data[col[0]])
				for i in range(len(data[col[0]])):
					temp[i] = data[col[0]][i] - int(col[1])
			elif '/' in cols:
				col =cols.split('/')
				col = [x.strip(' ') for x in col]
				cols=col[0]
				temp = copy.deepcopy(data[col[0]])
				for i in range(len(data[col[0]])):
					temp[i] = data[col[0]][i] / float(col[1])
			elif '*' in cols:
				col =cols.split('*')
				col = [x.strip(' ') for x in col]
				cols=col[0]
				temp = copy.deepcopy(data[col[0]])
				for i in range(len(data[col[0]])):
					temp[i] = data[col[0]][i] * float(col[1])
			else:
				temp = copy.deepcopy(data[cols])

			if op == '>':
				b = (temp>int(const))
				print(b)
			elif op == '<':
				b = temp<int(const)
			elif op == '=':
				b = temp==int(const)
			elif op == '<=':
				b = temp<=int(const)
			elif op == '>=':
				b = temp>=int(const)
			elif op == '!=':
				b = temp!=int(const)
			if len(l)==0:
				l=b
			else:
				l=l|b
		h = data.dtype.names
		headers = []
		for i in h:
			headers.append(i)
		# t_matrix = zip(*data)
		table = tabulate(data[l], headers, tablefmt="fancy_grid")
		print(table)
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
			temp =[]
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
				temp=copy.deepcopy(data[col[0]])
				for i in range(len(data[col[0]])):
					temp[i] = data[col[0]][i] + int(col[1])
			elif '-' in cols:
				col =cols.split('-')
				col = [x.strip(' ') for x in col]
				cols=col[0]
				temp=copy.deepcopy(data[col[0]])
				for i in range(len(data[col[0]])):
					temp[i] = data[col[0]][i] - int(col[1])
			elif '/' in cols:
				col =cols.split('/')
				col = [x.strip(' ') for x in col]
				cols=col[0]
				temp=copy.deepcopy(data[col[0]])
				for i in range(len(data[col[0]])):
					temp[i] = data[col[0]][i] / float(col[1])
			elif '*' in cols:
				col =cols.split('*')
				col = [x.strip(' ') for x in col]
				cols=col[0]
				temp=copy.deepcopy(data[col[0]])
				for i in range(len(data[col[0]])):
					temp[i] = data[col[0]][i] * float(col[1])
			else:
				temp = copy.deepcopy(data[cols])
			if op == '>':
				b = (temp>int(const))
			elif op == '<':
				b = temp<int(const)
			elif op == '=':
				b = temp==int(const)
			elif op == '<=':
				b = temp<=int(const)
			elif op == '>=':
				b = temp>=int(const)
			elif op == '!=':
				b = temp!=int(const)
			l=l&b
		h = data.dtype.names
		headers = []
		for i in h:
			headers.append(i)
		table = tabulate(data[l], headers, tablefmt="fancy_grid")
		print(table)
		return data[l]

	elif '+' in s or '-' in s or '*' in s or '/' in s:
		temp = []
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
			temp=copy.deepcopy(data[col[0]])
			for i in range(len(data[col[0]])):
				temp[i] = data[col[0]][i] + int(col[1])
		if '-' in col:
			col =col.split('-')
			col = [x.strip(' ') for x in col]
			temp=copy.deepcopy(data[col[0]])
			for i in range(len(data[col[0]])):
				temp[i] = data[col[0]][i] - int(col[1])
		if '/' in col:
			col =col.split('/')
			col = [x.strip(' ') for x in col]
			temp=copy.deepcopy(data[col[0]])
			for i in range(len(data[col[0]])):
				temp[i] = data[col[0]][i] / float(col[1])
		if '*' in col:
			col =col.split('*')
			col = [x.strip(' ') for x in col]
			temp=copy.deepcopy(data[col[0]])
			for i in range(len(data[col[0]])):
				temp[i] = data[col[0]][i] * float(col[1])
		
		if relop=='>':
			ans = data[temp>int(const)]
		elif relop=='<':
			ans = data[temp<int(const)]
		elif relop=='=':
			ans = data[temp==int(const)]
		elif relop=='>=':
			ans = data[temp<=int(const)]
		elif relop=='<=':
			ans = data[temp<=int(const)]
		elif relop=='!=':
			ans = data[temp!=int(const)]
		h = ans.dtype.names
		headers = []
		for i in h:
			headers.append(i)
		# t_matrix = zip(*data)
		table = tabulate(ans, headers, tablefmt="fancy_grid")
		print(table)
		return ans
	elif 'or' in s:
		print(s)
		cond=s.split('or')
		print(cond)
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
				cols=c[0]
				const=c[1]
			else:
				cols=c[1]
				const=c[0]
			if op == '>':
				b = (data[cols]>float(const))
			elif op == '<':
				b = data[cols]<float(const)
			elif op == '=':
				if(str(tname)+'.'+str(cols) in hash_keys):
					rows = Hash(tname,cols,const)
					n=len(cols)
					b = [False]*(n+1)
					for i in rows:
						b[i]=True
					b = np.asarray(b)
				elif(str(tname)+'.'+str(cols) in btree_keys):
					rows = Btrees(tname,cols,const)
					n=len(cols)
					b = [False]*(n+1)
					for i in rows:
						b[i]=True
					b = np.asarray(b)
				else:
					b = data[cols]==float(const)
			elif op == '<=':
				b = data[cols]<=float(const)
			elif op == '>=':
				b = data[cols]>=float(const)
			elif op == '!=':
				b = data[cols]!=float(const)
			l=l|b
		h = data.dtype.names
		headers = []
		for i in h:
			headers.append(i)
		# t_matrix = zip(*data)
		table = tabulate(data[l], headers, tablefmt="fancy_grid")
		print(table)
		return data[l]

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
				cols=c[0]
				const=c[1]
			else:
				cols=c[1]
				const=c[0]
			if op == '>':
				b = (data[cols]>float(const))
			elif op == '<':
				b = data[cols]<float(const)
			elif op == '=':
				# b = data[cols]==float(const)
				if(str(tname)+'.'+str(cols) in hash_keys):
					rows = Hash(tname,cols,const)
					n=len(cols)
					b = [False]*(n+1)
					for i in rows:
						b[i]=True
					b = np.asarray(b)
				elif(str(tname)+'.'+str(cols) in btree_keys):
					rows = Btrees(tname,cols,const)
					n=len(cols)
					b = [False]*(n+1)
					for i in rows:
						b[i]=True
					b = np.asarray(b)
				else:
					b = data[cols]==float(const)
			elif op == '<=':
				b = data[cols]<=float(const)
			elif op == '>=':
				b = data[cols]>=float(const)
			elif op == '!=':
				b = data[cols]!=float(const)
			l=l&b
		h = data.dtype.names
		headers = []
		for i in h:
			headers.append(i)
		# t_matrix = zip(*data)
		table = tabulate(data[l], headers, tablefmt="fancy_grid")
		print(table)
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
			ans = data[data[col]>float(const)]
		elif relop=='<':
			ans = data[data[col]<float(const)]
		elif relop=='=':
			if(str(tname)+'.'+str(col) in hash_keys):
				rows = Hash(tname,col,const)
				ans = data[rows]
			elif(str(tname)+'.'+str(col) in btree_keys):
				rows = Btrees(tname,col,const)
				ans = data[rows]
			else:
				ans = data[data[col]==float(const)]
		elif relop=='>=':
			ans = data[data[col]<=float(const)]
		elif relop=='<=':
			ans = data[data[col]<=float(const)]
		elif relop=='!=':
			ans = data[data[col]!=float(const)]
		h = ans.dtype.names
		headers = []
		for i in h:
			headers.append(i)
		# t_matrix = zip(*data)
		table = tabulate(ans, headers, tablefmt="fancy_grid")
		print(table)
		return ans
	

def getAverage(table_name,colname):
	data=table_name
	average=np.mean(data[colname])
	headers = [colname]
	d = np.array([average])
	return average

def getCount(table_name):
	num_rows = np.shape(table_name)[0]
	print(num_rows)
	return num_rows

def moving_average(table_name,colname, n):
	data = table_name
	ret = np.cumsum(data[colname[0]], dtype=float)
	n=float(n)
	ret[n:] = ret[n:] - ret[:-n]
	print(ret[n - 1:] / n)
	return ret[n - 1:] / n

def moving_sum(table_name,colname, n):
	data = table_name
	ret = np.cumsum(data[colname[0]], dtype=float)
	n=float(n)
	ret[n:] = ret[n:] - ret[:-n]
	print(ret[n-1:])
	return ret[n - 1:]

def avgGroup(table_name, colname):
	data=table_name
	s=colname[0]
	h=colname
	d=[]
	for i in colname:
		d.append(data[i])
	u_ij, inv_ij = np.unique(data[h[1:]], return_inverse=True)
	totals=np.zeros(len(u_ij))
	arr=np.zeros(len(u_ij))
	for i in inv_ij:
		arr[i] = arr[i] + 1
	np.add.at(totals, inv_ij, data[h[0]])
	for i in range(len(totals)):
		totals[i] = totals[i]/arr[i]
	flat_list = [item for sublist in u_ij for item in sublist]
	flat_list=np.array(flat_list)
	tab = rfn.merge_arrays((totals,u_ij),flatten=True)
	table = tabulate(tab, h, tablefmt="fancy_grid")
	print(table)
	return tab

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
	flat_list=np.array(flat_list)
    tab = rfn.merge_arrays((totals,u_ij),flatten=True)
    table = tabulate(tab, h, tablefmt="fancy_grid")
    print(table) 
    return tab

def getSum(tablename,colname):
	data=tablename
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
	flat_list=np.array(flat_list)
	tab = rfn.merge_arrays((totals,u_ij),flatten=True)
	table = tabulate(tab, h, tablefmt="fancy_grid")
	print(table)
	return tab

def concat(table_name1,table_name2):
	data1=table_name1
	data2=table_name2
	c = np.ma.concatenate((data1, data2), axis=None)
	t_matrix = zip(*c)
	h = data1.dtype.names
	headers = []
	for i in h:
		headers.append(i)
	table = tabulate(c, headers,tablefmt="fancy_grid")
	print(table)
	print(c)
	return c


if __name__ == "__main__":
	table={}
	st = ""
	print("DATABASE PROJECT:\nThis program supports the following functionalities\n \n1.inputfromfile\n2.outputtofile")
	print("Enter quit to exit")
	while(st!="quit"):
		st = raw_input()
		params=st.split(":=")
		params = [x.strip(' ') for x in params]
		#call function
		if(st.startswith("Hash")):
			start_time = time.time()
			res = st.replace("Hash","")
			res=res.strip('[,()]').split(',')
			table_name=res[0]
			table_name = table[table_name]
			col_name=res[1]
			tname=res[0]
			d=HashTable(tname,table_name,col_name)
			table[params[0]]=d
			total_time = time.time() - start_time
			print("time:")
			print(total_time)

		elif(st.startswith("Btree")):
			start_time = time.time()
			res = st.replace("Btree","")
			res=res.strip('[,()]').split(',')
			table_name=res[0]
			table_name = table[table_name]
			col_name=res[1]
			tname=res[0]
			d=BtreesStruc(tname,table_name,col_name)
			table[params[0]]=d
			total_time = time.time() - start_time
			print("time:")
			print(total_time)

		elif(st.find("inputfromfile")!=-1):
			start_time = time.time()
			p = params[1]
			filename = p[p.find('(')+1:p.find(')')]
			d=importfile(filename)
			table[params[0]]=d
			total_time = time.time() - start_time
			print("time:")
			print(total_time)
		
		elif(st.find("outputtofile")!=-1):
			start_time = time.time()
			p = params[0]
			args = p[p.find('(')+1:p.find(')')]
			args=args.split(",")
			table_name=table[args[0]]
			filename=args[1]
			exportfile(table_name,filename)
			total_time = time.time() - start_time
			print("time:")
			print(total_time)

		elif(params[1].startswith("select")):
			start_time = time.time()
			p = params[1:]
			res = [sub.replace('select', "") for sub in p] 
			stripped_list = [j.split(',') for j in res]
			final_args = [[x.strip('[,()]') for x in l] for l in stripped_list]
			final_args = [[i for i in l if i] for l in final_args] 
			final_args = [j for sub in final_args for j in sub]
			final_args = [x.strip(' ') for x in final_args]
			table_name = table[final_args[0]]
			tname = final_args[0]
			d=getSelect(tname,table_name,final_args[1:])
			table[params[0]]=d
			total_time = time.time() - start_time
			print("time:")
			print(total_time)

		elif(params[1].startswith("project")):
			start_time = time.time()
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
			total_time = time.time() - start_time
			print("time:")
			print(total_time)

		elif(params[1].startswith("avggroup")):
			start_time = time.time()
			p = params[1:]
			res = [sub.replace('avggroup', "") for sub in p] 
			stripped_list = [j.split(',') for j in res]
			final_args = [[x.strip('[,()]') for x in l] for l in stripped_list]
			final_args = [[i for i in l if i] for l in final_args] 
			final_args = [j for sub in final_args for j in sub]
			final_args = [x.strip(' ') for x in final_args]
			table_name = table[final_args[0]]
			column_names = final_args[1:]
			d=avgGroup(table_name,column_names)
			table[params[0]]=d
			total_time = time.time() - start_time
			print("time:")
			print(total_time)
		
		elif(params[1].startswith("avg")):
			start_time = time.time()
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
			total_time = time.time() - start_time
			print("time:")
			print(total_time)

		elif(params[1].startswith("sumgroup")):
			start_time = time.time()
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
			total_time = time.time() - start_time
			print("time:")
			print(total_time)

		elif(params[1].startswith("join")):
			start_time = time.time()
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
			total_time = time.time() - start_time
			print("time:")
			print(total_time)

		elif(params[1].startswith("movavg")):
			start_time = time.time()
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
			total_time = time.time() - start_time
			print("time:")
			print(total_time)

		elif(params[1].startswith("movsum")):
			start_time = time.time()
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
			total_time = time.time() - start_time
			print("time:")
			print(total_time)

		elif(params[1].startswith("sort")):
			start_time = time.time()
			p = params[1:]
			res = [sub.replace('sort', "") for sub in p] 
			stripped_list = [j.split(',') for j in res]
			final_args = [[x.strip('[,()]') for x in l] for l in stripped_list]
			final_args = [[i for i in l if i] for l in final_args] 
			final_args = [j for sub in final_args for j in sub]
			final_args = [x.strip(' ') for x in final_args]
			table_name = table[final_args[0]]
			d=sortColumns(table_name,final_args[1:])
			table[params[0]]=d
			total_time = time.time() - start_time
			print("time:")
			print(total_time)

		elif(params[1].startswith("countgroup")):
			start_time = time.time()
			p = params[1:]
			res = [sub.replace('countgroup', "") for sub in p]
			stripped_list = [j.split(',') for j in res]
			final_args = [[x.strip('[,()]') for x in l] for l in stripped_list]
			final_args = [[i for i in l if i] for l in final_args]
			final_args = [j for sub in final_args for j in sub]
			final_args = [x.strip(' ') for x in final_args]
			table_name = table[final_args[0]]
			column_names = final_args[1:]
			d=countGroup(table_name,final_args[1:])
			table[params[0]]=d
			total_time = time.time() - start_time
			print("time:")
			print(total_time)
			
		elif(params[1].startswith("count(")):
			start_time = time.time()
			p = params[1:]
			res = [sub.replace('count', "") for sub in p] 
			stripped_list = [j.split(',') for j in res]
			final_args = [[x.strip('[,()]') for x in l] for l in stripped_list]
			final_args = [[i for i in l if i] for l in final_args] 
			final_args = [j for sub in final_args for j in sub]
			final_args = [x.strip(' ') for x in final_args]
			table_name = table[final_args[0]]
			column_names = final_args[1:]
			d=getCount(table_name)
			table[params[0]]=d
			total_time = time.time() - start_time
			print("time:")
			print(total_time)

		elif(params[1].startswith("concat")):
			start_time = time.time()
			p = params[1:]
			res = [sub.replace('concat', "") for sub in p] 
			stripped_list = [j.split(',') for j in res]
			final_args = [[x.strip('[,()]') for x in l] for l in stripped_list]
			final_args = [[i for i in l if i] for l in final_args] 
			final_args = [j for sub in final_args for j in sub]
			final_args = [x.strip(' ') for x in final_args]
			table_name1 = table[final_args[0]]
			table_name2 = table[final_args[1]]
			d=concat(table_name1,table_name2)
			table[params[0]]=d
			total_time = time.time() - start_time
			print("time:")
			print(total_time)