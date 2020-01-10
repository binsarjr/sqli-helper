import requests
import re
import os
import json
from .sqli import Sqli
from .Output import Output

class Terminal:
    
    def clear(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def setup(self, url):
        self.sqli = Sqli(url)

        self.url = url
        self.information=self.sqli.information()
        self.user = self.information["user"]
        self.domain = re.search(r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}', self.url)[0]
        self.dbname = "NONE"

        self.informations()
        return  self

    def run(self):
        try:

            cmd         = input("\033[91m┌["+ self.user.replace('@', '\033[93m@\033[96m') +"\033[91m]~[\033[32m"+ self.domain +"\033[91m]\n\033[91m└[\033[94m" + self.dbname + "\033[91m]~\033[93m#\033[97m ")

            if cmd == "clear":
                self.clear()
                self.run()
            elif cmd == 'help':
                self.help()
                self.run()
            elif re.search("dump data (.*)", cmd):
                if (self.dbname == "NONE"):
                    output = Output().info(["Unkown Database"],False)
                    print(output)
                else:
                    table_name  = re.search('dump data (.*)', cmd).group(1)
                    try:
                        message, title, isFound, columns_exist = self.sqli.columns(table_name)
                        if isFound:
                            output = Output().success(message, title)
                            print(output)
                            output = Output().info(["use commas as separators between columns","Examples: username,password,fullname","if you want to display everything, press enter"], True)

                            print(output)
                            columns = input(f"[\033[94m?\033[97m] column name : ")
                            if not columns:
                                columns = columns_exist
                            else:
                                columns = columns.split(',')
                            try:
                                result = self.sqli.dump_data(table_name, columns)
                                self.clear()
                                output = Output().table(result['columns'], result['data'])
                                print(output)
                            except Exception as e:
                                unkown_column=""
                                for column in columns:
                                    column = column.strip(' ')
                                    if column not in columns_exist:
                                        unkown_column += f",'{column}'"
                                unkown_column = unkown_column.strip(',')
                                output = Output().error([f"Unkown columns {unkown_column} doesn't exist in field list"], "Database ERROR")
                                print(output)
                        else:
                            output = Output().info([f"table '{table_name}' doesn't exist"],False)
                            print(output)
                    except Exception as e:
                        output = Output().info([f"table '{table_name}' doesn't exist"],False)
                        print(output)
                self.run()
            elif cmd == "show tables":
                if (self.dbname == "NONE"):
                    output = Output().info(["No Database Selected"],False)
                    print(output)
                else:
                    # table_name  = re.search('dump data (.*)', cmd).group(1)
                    message, title, isFound = self.sqli.tables()
                    if (isFound):
                        output = Output().success(message, title)
                    else:
                        output = Output().failed(message, title)
                    print(output)
                self.run()
            elif re.search('show columns (.*)', cmd):
                table_name = re.search('show columns (.*)', cmd).group(1)
                try:
                    if self.dbname != "NONE":
                        message, title, isFound, columns = self.sqli.columns(table_name)
                        if (isFound):
                            output = Output().success(message, title)
                        else:
                            output = Output().failed(message, title)
                        print(output)
                    else:
                        output = Output().info(["No Database Selected"],False)
                        print(output)
                except Exception:
                    output = Output().info([f"table '{table_name}' doesn't exist"],False)
                    print(output)

                self.run()
            elif cmd == "show dbs":
                self.databases()
                self.run()
            elif cmd == "show information":
                self.informations()
                self.run()
            elif re.search("use (.*)", cmd):
                dbname  = re.search('use (.*)', cmd).group(1)
                self.changeDB(dbname)
                
                self.run()
            else:
                output = Output().error(["Command not found"], "Syntax Error")
                print(output)
                self.run()

        except Exception as e:
            output = Output().error([e], "System ERROR")
            print(output)
            self.run()


    # extract data and print result
    def databases(self, level = 1 ):
        dbs = self.sqli.databases()
        message = list()
        for db in dbs:
            message.append(f"{db}")
        output = Output().success(title="Databases : ", message=message)
        print(output)

    def informations(self, level = 1):
        information = self.sqli.information()
        message = list()

        message.append("Hostname                : {}".format(information['hostname']))
        message.append("Port                    : {}".format(information['port']))
        message.append("SSL                     : {}".format(information['ssl']))
        message.append("OpenSSL                 : {}".format(information['openssl']))
        message.append("Symlink                 : {}".format(information['symlink']))
        message.append("Socket                  : {}".format(information['socket']))
        message.append("User                    : {}".format(information['user']))
        message.append("Database                : {}".format(information['schema']))
        message.append("Database Version        : {}".format(information['version']))
        message.append("Base Dir                : {}".format(information['base_dir']))
        message.append("Data Dir                : {}".format(information['data_dir']))
        message.append("Operating System        : {}".format(information['os_version']))
        message.append("Mechine Version         : {}".format(information['mechine_version']))
        
        print(Output().success(message=message,title="informations :"))

    def changeDB(self,dbname):
        change, status, dbname = self.sqli.changeDB(dbname)
        if(self.dbname == "NONE" or dbname != "NONE"):
            self.dbname = dbname
        output = Output().info(message=change, status=status)
        print(output)

    def showTables(self):
        pass

    def benner(self):
        return '''
\033[0m|| 
\033[0m||\033[92m    _____ ____    __ \033[91m   _ \033[92m      __  __     __     _____      
\033[0m||\033[92m   / ___// __ \  / / \033[91m  (_)\033[92m     / / / /__  / /___ |__  /_____    
\033[0m||\033[92m   \__ \/ / / / / /  \033[91m / /\033[92m_____/ /_/ / _ \/ / __ \ /_ </ ___/ 
\033[0m||\033[92m  ___/ / /_/ / / /___\033[91m/ /\033[92m_____/ __  /  __/ / /_/ /__/ / /    
\033[0m||\033[92m /____/\___\_\/_____\033[91m/_/\033[92m     /_/ /_/\___/_/ .___/____/_/     
\033[0m||\033[92m                                        /_/ \033[91mv1.0 BETA
\033[0m||
\033[0m||   Author  : Binsar Dwi Jasuma
\033[0m||   Github  : github.com/binsarjr
\033[0m||   Team    : IndoSec
\033[0m||   LICENSE : MIT
\033[0m||
\033[0m|| 
        '''

    def help(self):
        print("""
    show information            : shows  information from the target
    show dbs                    : show databases
    use <database_name>         : change the database to be used
    show tables                 : shows all data tables in the database used
    show columns <column_name>  : shows all data columns in the table
    dump data <column_name>     : pulling out data in the column used


        """)