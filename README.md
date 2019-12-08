# database project
This project supports the following functionalities:
1.inputfromfile
2.average
3.sum
4.count
5.averageGroup
6.sumGroup
7.countGroup
8.movingAvg
9.movingSum
10.select
11.project
12.join

The user can enter the the name of the functions to get the required queries.
Once executed the time taken for the query to be executed will be displayed.

All intermediate results are stored in a hashmap, table{ }

Following is a description of each function

inputfromfile: Takes the filename and stores the information in a tabular format.

average: Takes a table and column name and returns the average of that column.

sum: Takes a table and column name and returns the sum of that column.

count: Takes a table and column name and returns the count of that column.

averageGroup: Takes the table name as the first parameter, performs the aggregate
functionality on the next single attribute passed to the function grouped by all the rest
attributes.

sumGroup:  Takes the table name as the first parameter, performs the aggregate
functionality on the next single attribute passed to the function grouped by all the rest
attributes.

countGroup: Takes the table name as the first parameter, performs the aggregate
functionality on the next single attribute passed to the function grouped by all the rest
attributes.

movingAvg: Takes a table, an attribute and a constant k as it parameters. K-way moving aggregate of the attribute is returned.

movingSum: Takes a table, an attribute and a constant k as it parameters. K-way moving aggregate of the attribute is returned.

select: Takes the table name and column names along with some condition and displays the result based on the condition given.
This method supports select with multiple ands (with and without arithmetic operation on columns), 
select with multiple or (with and without arithmetic operation on columns)  select with just one codition

project: Takes the table name and columns as parameters and returns a table with the column

join: Takes two tables and joins them based on a contions.  This method supports join with multiple ands 
(with and without arithmetic operation on columns), join with multiple or (with and without arithmetic operation on columns) 
join with just one codition

Example Usage: 
Enter the query: R := inputfromfile(sales1)
Enter the query: R1 := select(R, (time > 50) or (qty < 30))

In the above example, the first line takes a file sales1, and stores the contents of sales1 in an array table which can later 
be referenced using R
Similarly, the output of R1 := select(R, (time > 50) or (qty < 30)), stores the result from select(R, (time > 50) or (qty < 30)) 
in R1.
