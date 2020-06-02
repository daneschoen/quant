
import datetime, calendar
# from datetime import timedelta, timezone
# from pytz import utc, timezone
import pytz
import string, ast


def convert_str_epoch(lst_chart_data_str):
    """
    lst_chart_data_str = [chart_data_dtstr_long, ...]
    
    # "[['07/04/2015', 3.14], ['07/05/2015', 6.22], ..., N]"
    # ast => chg '07/04/2015' -> epoch => back to str
    """
    lst_chart_series = []
    for s in range(len(lst_chart_data_str)):
      # str -> lst  
      lst_chart_series.append(ast.literal_eval(lst_chart_data_str[s]))
      # dtstr -> epoch
      #for s in range(len(lst_chart_series)):
      for i_s in range(len(lst_chart_series[s])):
        dtime_i_s = datetime.datetime.strptime(lst_chart_series[s][i_s][0],'%m/%d/%Y')   #('7/4/2015','%d/%m/%Y')
        lst_chart_series[s][i_s][0] = calendar.timegm(dtime_i_s.timetuple())*1000   # int(time.mktime(dtime_i_s.timetuple()))
    return lst_chart_series


def convert_strlst_str(strlst_str):
    lst_dtstr=[]
    if "'" in strlst_str:
      lst_dtstr = ast.literal_eval(strlst_str)
    else:
      # Cant have comma in string element
      lst_dtstr = strlst_str[1:-1].split(",")
    return lst_dtstr


def convert_strlst_dtstr_epoch(strlst_dtstr):
    lst_epoch = []
    lst_dtstr = ast.literal_eval(strlst_dtstr)
    for dtstr in lst_dtstr:
      dtime_i_s = datetime.datetime.strptime(dtstr,'%m/%d/%Y')   
      lst_epoch.append(calendar.timegm(dtime_i_s.timetuple())*1000)   # int(time.mktime(dtime_i_s.timetuple()))
    
    return lst_epoch


def convert_strlst_fd(strlst_fd):
    lst_series = ast.literal_eval(strlst_fd)
    return lst_series
    
    
    
