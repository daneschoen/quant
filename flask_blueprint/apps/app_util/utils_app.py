
#from constants import *

def arrCode_arrCodeName(arrCode):
    """
    ['client_home', 'phone'] ==> ['client_home___Client Home', 'phone___Phone']
    """
    arrCodeName = []
    for code in arrCode:
        code_split_i = code.split("_")
        name_i = ""
        for c in code_split_i:
            name_i += c.capitalize() + " "
        arrCodeName.append(code + "___" + name_i.strip())

    return arrCodeName

