#DataBaseManager
A simple DataBaseManager manager. You can manage DataBaseManager simply without using SQL or any other query language. The Inputs and outputs are in the form of JSON so you can simply share the data across networks. A simple SQL shell was attached to do more with Your Db.
Execute "pip install DataBaseManager"
Then import it By Executing
"import DataBaseManager"

#Supported DataBaseManagers:
1)SQLite

#SQLite
1)import:-
'from DataBaseManager import sqlite'
2)create object:-
'MyObj = sqlite("your file path")
3)If you want to create a new Db
'MyObj = sqlite()'
'MyObj.CreateDb("db name",{"table name":{"column":"type"}})'
4)For inserting data:-
'MyObj.insert("table name",[{"column1":"value1","column2":"value2"},{"column":"next items"}])'
5)for selecting:- 
'MyObj.select(["table1","table2"],select=["table1.column","table2.column"],where={"table1.column":"value","table2.column":"value2"}))'
This will return the data in the form of a list of the result tuples same as the form of fetchall()
Use MyObj.parse_fetch_all() to get the data in the form of dictionary
5)For Getting shell:-
"MyObj.shell('Any commands if you want')"
6)also have execute, executescript, commit, fetchone,fetchall etc. cursor same as the python sqlite3
7) execute MyObj.conn to return the connection
8) execute MyObj.schema to get the schema in the form of a dictionary
9) execute MyObj.tables to get the table names

sqlite shell info at:- https://techabam.000webhostapp.com/DataBaseManager/sqlite/shell.html
More info on the link:
https://techabam.000webhostapp.com/DataBaseManager

#Whats new

V0.0.2--new sqlite.Reload() to re initialize the class. for geting the changes that you change in the schema