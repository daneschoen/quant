

from jinja2 import evalcontextfilter, Markup, escape


# def plural(str, end_ptr = None, rep_ptr = ""):
#     if end_ptr and str.endswith(end_ptr):
#         return str[:-1*len(end_ptr)] + rep_ptr
#     else:
#       return str+'s'

def plural(num):
    if num > 1:
      return "s"
    else:
      return ""

