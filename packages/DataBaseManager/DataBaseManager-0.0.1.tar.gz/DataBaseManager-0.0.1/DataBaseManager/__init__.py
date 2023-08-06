import traceback
white = '\033[0m'
red = '\033[31m'
green = '\033[32m'
yellow = '\033[93m'
#insert update statement
class Error:
    Errors = {
        1:"Database Not Exists",
        2:"Ertor in creating database",
        3:"Error in the Type of given value",
        4:"Error in the given table name"
    }
import sqlite3 as db
import os
class sqlite:
    conn = None
    cur = None
    schema = None
    tables = None
    def __init__(self,dbname=None):
        self.dbname = dbname
        if dbname==None:return
        try:
            self.conn = db.connect(dbname)
            self.cur = self.conn.cursor()
            cur = self.cur
        except Exception as e:raise ValueError(f'{red}The Database "{dbname}" Not Exists, Error[1]{white+str(e)}')
        self.tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        self.schema = {}
        for x in self.tables:
            table = x[0]
            ll = cur.execute(f"PRAGMA table_info({table})").fetchall()
            gg = {}
            for y in ll:
                name = y[1]
                Type = y[2]
                gg[name] = Type
            self.schema[table] = gg
        self.tables = [x[0] for x in self.tables]
    def insert(self,table,data,Except=None):
        if table not in self.tables:raise ValueError(f"{red}Unknown table{white}")
        for y in data:
            st1 = f"INSERT INTO {table}("
            st2 = ") VALUES("
            gg = ()
            i = 0
            for x in y.items():
                i += 1
                column = x[0]
                val = x[1]
                gg = gg + (val,)
                if i==1:
                    st1 = st1 + str(column)
                    st2 = st2 + "?"
                    continue
                st1 = st1 + "," + str(column)
                st2 = st2 + ",?"
            state = st1+st2+")"
            self.cur.execute(state,gg)
            self.conn.commit()
            #prints trial
    def update(self,table,data,where=None):
        if table not in self.tables:raise Exception(f"{red}The Table '{table}' Not Exists Error[-4]")
        st1 = f"UPDATE {table} SET"
        cc = [x for x in data.items()]
        i = 0
        tt = ()
        for x in cc:
            i += 1
            column = x[0]
            val = x[1]
            ff = f" {column} = ?"
            tt = tt + (val,)
            if i == len(cc):
                st1 += ff
                continue
            st1 += ff+","
        if isinstance(where,dict):
            dd = [x for x in where.items()]
            st1 += " WHERE"
            i = 0
            for x in dd:
                i += 1
                column = x[0]
                value = x[1]
                if value == None:
                    st2 = f' {column}'
                else:
                    st2 = f' {column} = ?'
                    tt += (value,)
                if i == len(dd):
                    st1 = st1 + st2
                else:
                    st1 = st1 +st2 + " AND"
        self.cur.execute(st1,tt)
        self.conn.commit()
    def select(self,table,**args):
        if not table in self.tables and not isinstance(table,list):raise Exception(f"{red}No table named {table}{white}")
        if isinstance(table,list):
            i = 0
            table2 = ""
            for x in table:
                i += 1
                if i == 1:
                    table2 += str(x)
                    continue
                table2 += f" JOIN {x}"
                continue
            table = table2
        if args == {}:
            return self.cur.execute(f"SELECT * FROM {table}").fetchall()
        else:
            st1 = f"SELECT "
            for x in args.items():
                gg = ()
                if x[0] == "select":
                    i = 0
                    for y in x[1]:
                        i += 1
                        if i == len(x[1]):
                            st1 += y + " "
                        else:
                            st1 += y + ","
                    st1 += f"FROM {table} "
                if x[0] == "where":
                    st1 += "WHERE "
                    cc = [x for x in x[1].items()]
                    st2 = ""
                    g = 0
                    for y in cc:
                        g+= 1
                        column = y[0]
                        val = y[1]
                        if val == None:
                            st2 += " " + str(column)
                            continue
                        ss = f"{column} = ?"
                        gg += (val,)
                        if g == len(cc):
                            st2 += ss + " "
                            continue
                        st2 += ss + ","
                    st1 += st2
            self.cur.execute(st1,gg)
           
            return self.cur.fetchall()
                            
                
    def execute(self,sql):
        self.objected = self.cur.execute(sql)
        return self.objected
    def commit(self):self.conn.commit()
    def executescript(sql):
        self.objected = self.cur.executescript(sql)
        return self.objected
    def fetchone(self):return self.objected.fetchone()
    def fetchall(self):return self.objected.fetchall()
    def cursor(self):return self.conn.cursor()
    def drop(self,table=None):
        if table is None:
            os.remove(self.dbname)
            return "Removed DB"
        else:
            if table in self.tables:
                self.conn.execute(f"DROP TABLE {table}")
                self.conn.commit()
                return 'removed table'
        
    def CreateDb(self,Dbname,data):
        self.dbname = Dbname
        try:
            self.conn = db.connect(Dbname)
            self.cur = self.conn.cursor()
            cur = self.cur
        except Exception as e:
            raise Exception(red+"Error In Creating Database Try Sqlite3 Directly to create database Error[2]"+white)
        if not isinstance(data,dict):raise Exception(f"{red}Excepted Argumet 2 Data in the form of a dictionary with key(table name) => value(dict(column:type)) Error[3]{white}")
        for x in data.items():
            table_name = x[0]
            content = x[1]
            cur.execute(f"DROP TABLE IF EXISTS {table_name}")
            st1 = f"CREATE TABLE {table_name}("
            #st2 = ") VALUES("
            i = 0
            cc = [y for y in content.items()]
            for y in cc:
                i += 1
                column = y[0]
                val = y[1]
                if i == 1:
                    st1 = st1 + str(column)
                else:
                    st1 = st1 +","+ str(column)
                gm = ""
                for h in val:
                    if not isinstance(val,list):
                        gm = val
                        break
                    gm = gm +" "+ str(h)
                if i == len(cc):
                    st1 = st1 +" " + str(gm)
                    continue
                
                st1 = st1 +" "+ str(gm)
                
            state = st1 +")"
            cur.execute(state)
            #print(state)
        self.conn.commit()
    def Reload(self):
        return sqlite(self.dbname)
    def shell(self):
        conn = self.conn
        cur = self.cur
        print("Type quit() to exit | Type show to fetchall | Type 'commit' to commit changes | Please assure to use ';'\n"+yellow+"SQLite Console"+white)
        command = ""
        while True:
            d = input(">>> ")
            hh = d
            if hh == "quit()":
                print("Bye")
                break
            if hh == "commit":
                print(conn.commit())
                continue
            if hh == "show":
                print(yellow+"Contents:-\n",white)
                try:gg = re
                except:
                    print("Nothing to show")
                    continue
                for x in re.fetchall():
                    try:
                        ss = ""
                        for k in x:
                            ss = ss + " | " + str(k)
                        print(ss)
                    except Exception as e:
                        print(e)
                continue
            if ";" not in d:
                command = command + hh
                continue
            if ";" in d:
                command = command +hh
            print(command)
            try:
                re = cur.execute(command.replace("\n",""))
                command = ""
                print(re)
            except Exception as e:print(traceback.format_exc())
        return "Console Exit!"
#h = sqlite("db.db")
#print(h.dbname)
#h.CreateDb("db.db",{"name":{"time":["INTEGER"],"type":["text"]}})
#h.shell(h)
#print(h.conn.description)
#h.insert("name",[{"time":67,"type":"hello"},{"time":890,"type":"poda"},{"time":67,"type":"i am changed"}])
#h.update("name",{"time":89,"type":"67 changed to 89"},{"time":67,"type is not null":None})
#print(h.select(["name"],select=["name.type"],where={"time":89}))
#while True:
#    g = input("->")
 #   if g == "quit":
      #  print("Bye")
   #     break
 #   try:print(exec(g))
#    except:print(traceback.format_exc())
#h.Reload()
#print(h.dbname)

#print(Error.Errors[1])