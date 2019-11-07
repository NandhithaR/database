import numpy as np
from tabulate import tabulate

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
	headers=file_array.dtype.names
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
	

#selection, projection, count, sum and avg aggregates
def getAverage(filename,colname):
	head,data=importfile(filename)
	average=np.mean(data[colname])
	return average

def getSum(filename,colname):
	head,data=importfile(filename)
	s=np.sum(data[colname])
	return s

# def fields_view(arr, fields):
#     dtype2 = np.dtype({name:arr.dtype.fields[name] for name in fields})
#     return np.ndarray(arr.shape, dtype2, arr, 0, arr.strides)
def projection(filename,*colname):
	head,data=importfile(filename)
	h=[]
	d=[]
	for i in colname:
		h.append(i)
	#print(d)
	# tabulate data
	table = tabulate(d, h, tablefmt="fancy_grid")
	# output
	#print(table)
# def readQuery(query):

# def select(filename,query):
# 	head,data=importfile(filename)
# 	cond = readQuery(query)
def select(filename,*arg):
	head,data=importfile(filename)
	test_cols = data[['qty', 'time']]
	test_vals = np.array(('a1v1', 'a4v1'), test_cols.dtype)
	print(data[test_cols == test_vals])



#sumgroup, avggroup, moving avg, moving sum, group by, join


if __name__ == "__main__":
   head,data=importfile('sampledata.txt')
   # print(head)
   # print(data)
   sortColumns('sampledata.txt','qty')
   getAverage('sampledata.txt','qty')
   projection('sampledata.txt','qty','saleid')
   getSum('sampledata.txt','qttiy')
   select('sampledata.txt','qty=5')





