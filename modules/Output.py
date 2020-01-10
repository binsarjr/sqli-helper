from prettytable import PrettyTable

class Output:
    def success(self, message, title):
        result = f"[\033[92m+\033[97m] {title}\n"
        for message in message:
            result += f"└[\033[92m•\033[97m] {message}\n"
        return "\n{}\n".format(result.strip('\n'))
    
    def failed(self, message, title):
        result = f"[\033[92m+\033[97m] {title}\n"
        for message in message:
            result += f"└[\033[92m•\033[97m] {message}\n"
        return "\n{}\n".format(result.strip('\n'))

    def error(self, message, title):
        result = f"[\033[91m!\033[97m] {title}\n"
        for message in message:
            result += f"└[\033[92m•\033[97m] {message}\n"
        return "\n{}\n".format(result.strip('\n'))

    def info(self, message, status):
        result = f"[\033[94mINFO\033[97m]\n"
        if status == True:
            for message in message:
                result += f"└[\033[92m+\033[97m] {message}\n"
        else:
            for message in message:
                result += f"└[\033[91m-\033[97m] {message}\n"
        return "\n{}\n".format(result.strip('\n'))
    
    def table(self, field_names, rows):
        x = PrettyTable()
        x.field_names = field_names

        for row in rows:
            x.add_row(row)
        x.align = "l"
        return x
        # x.add_row()
        # x.add_row(["Darwin", 112, 120900, 1714.7])
        # x.add_row(["Hobart", 1357, 205556, 619.5])
        # x.add_row(["Sydney", 2058, 4336374, 1214.8])
        # x.add_row(["Melbourne", 1566, 3806092, 646.9])
        # x.add_row(["Perth", 5386, 1554769, 869.4])

 