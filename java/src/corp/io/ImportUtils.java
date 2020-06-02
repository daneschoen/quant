package program.io;

import java.util.Calendar;


public class ImportUtils {

  public int mt;
  public int dy;
  public int yr;
  public int hr;
  public int min;
  public int sec;

  
  public void parseMtDyYr(String strDate, String format_date) {

	strDate = strDate.toLowerCase().trim();	

    if (format_date.equals("MM/dd/yyyy")) {
	    mt = Integer.valueOf(strDate.substring(0,2)).intValue();
	    dy = Integer.valueOf(strDate.substring(3,5)).intValue();
	    yr = Integer.valueOf(strDate.substring(6,10)).intValue();
	    
    } else if (format_date.equals("MM/dd/yy")) {    
	    mt = Integer.valueOf(strDate.substring(0,2)).intValue();
	    dy = Integer.valueOf(strDate.substring(3,5)).intValue();	    
		yr = Integer.valueOf(strDate.substring(6,8)).intValue();
	    if (yr < 40)   {  // "00, 01, 06"
	        yr += 2000;  
	    } else {
		    yr += 1900;  // 86,96,99  
	    }
    } else if (format_date.equals("MM/dd/yyy")) {    //* !
	    mt = Integer.valueOf(strDate.substring(0,2)).intValue();
	    dy = Integer.valueOf(strDate.substring(3,5)).intValue();
		yr = Integer.valueOf(strDate.substring(6)).intValue();
	    if (yr<40)   {  // "00, 01, 06"
	        yr += 2000;  
	    } else {
		    yr += 1900;  // 86,96,99  
	    }   
    } else if (format_date.equals("*/*/*")) {    //* !
		Calendar calToday = Calendar.getInstance();  
        int iYear = calToday.get(Calendar.YEAR);
    	iYear = iYear - 2000;  //* 8 ie
    	
    	int y_Slash = strDate.indexOf("/"); 
	    mt = Integer.valueOf(strDate.substring(0,y_Slash)).intValue();
	    strDate = strDate.substring(y_Slash+1);
	    y_Slash = strDate.indexOf("/");
	    dy = Integer.valueOf(strDate.substring(0,y_Slash)).intValue();
	    strDate = strDate.substring(y_Slash+1);
		yr = Integer.valueOf(strDate).intValue();
	    if (yr < iYear + 5)   {  // "00, 01, 06"
	        yr += 2000;  
	    } else if (yr < 100){
		    yr += 1900;  // 86,96,99  
	    }  //* else already 1999, 2000, 2001, etc. 	    
	}

  }
  
  public void parseTime(String strTime, String formatTime) {

	strTime = strTime.toLowerCase().trim();	

	if (formatTime.equals("HH:mm:ss")) {
		hr = Integer.valueOf(strTime.substring(0,2)).intValue();
		min = Integer.valueOf(strTime.substring(3,5)).intValue();
		sec = Integer.valueOf(strTime.substring(6,9)).intValue();
	}
  }
  
  
  
  
}
