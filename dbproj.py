import numpy as np
from tabulate import tabulate
import numpy.lib.recfunctions as rfn
from operator import itemgetter
from itertools import groupby
from collections import defaultdict


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
	return headers,file_array
	

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

def projection(filename,*colname):
	head,data=importfile(filename)
	h=[]
	d=[]
	for i in colname:
		h.append(i)
		d.append(data[i])
	t_matrix = zip(*d)
	table = tabulate(t_matrix, h, tablefmt="fancy_grid")
	return table

def select(filename,*arg):
	head,data=importfile(filename)
	s=data[data['qty']==2]
	for i in range(len(s)):
		s[i][5]=s[i][5]+5
	return data[(data['itemid']>75) | (data['qty']>2)]

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

def geteJoin(filename1,filename2,*cols):
	head1,data1=importfile(filename1)
	head2,data2=importfile(filename2)
	a1=data1[cols[0]]
	a2=data2[cols[1]]
	arrays=np.where(data1['qty']==data2['Q'],a1,a2)
	print(arrays)
	# ans=np.concatenate((a1, a2), axis=0)
	

# def join_struct_arrays(filename1,filename2, *cond):
# 	head1,data1=importfile(filename1)
# 	head2,data2=importfile(filename2)
# 	a1=np.array([data1])
# 	a2=np.array([data2])
# 	arrays=[]
# 	for i in range(len(data1)):
# 		arrays.append(data1[i])
# 	for i in range(len(data2)):
# 		arrays.append(data2[i])
# 	print(arrays['itemid'])
# 	#print(arrays[(data1['itemid']>75) | (data1['qty']>2)])


# def fields_view(arr, fields):
#     dtype2 = np.dtype({name:arr.dtype.fields[name] for name in fields})
#     return np.ndarray(arr.shape, dtype2, arr, 0, arr.strides)

def convertQuery(*arg):
	head,data=importfile(filename)


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
   head,data=importfile('sampledata.txt')
#    print(head)
#    print(head)
#    print(data)
   sortColumns('sampledata.txt','qty')
   getAverage('sampledata.txt','qty')
   projection('sampledata.txt','qty','saleid','itemid')
   getSum('sampledata.txt','qty')
   select('sampledata.txt','qty=5')
   #join('sampledata.txt','datasample.txt', '(R1.qty > S.Q)', '(R1.saleid = S.saleid)')
#    a1 = np.array([(1, 2), (3, 4), (5, 6)], dtype=[('x', int), ('y', int)])
#    a2 = np.array([(7,10), (8,11), (1,2)], dtype=[('z', int), ('w', float)])
#   join_struct_arrays('sampledata.txt','datasample.txt', '(R1.qty > S.Q)', '(R1.saleid = S.saleid)')
   sumGroup('sampledata.txt','qty','pricerange')
#    avgGroup('sampledata.txt','qty','time','pricerange')
   moving_average('sampledata.txt','qty',3)
   moving_sum('sampledata.txt','qty',3)
   geteJoin('sampledata.txt','datasample.txt','qty','Q')
  