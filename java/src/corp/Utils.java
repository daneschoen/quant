package program;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class Utils {
  
  /*	
  public static void main (String[] args) {
	System.out.println(diff_dtime("2015/7/04 18:00","2015/07/03 06:09"));
  }
  */
	
  public static float diff_dtime(String strDtime0, String strDtime1) {
	//String str = "Jun 13 2003 23:11:52.454 UTC";
	//SimpleDateFormat df = new SimpleDateFormat("MMM dd yyyy HH:mm:ss.SSS zzz");
	SimpleDateFormat sdf = new SimpleDateFormat("yyyy/MM/dd HH:mm");
	try {
	  Date date0 = sdf.parse(strDtime0);
	  Date date1 = sdf.parse(strDtime1);
	  long diff_epoch = date0.getTime() - date1.getTime();
	  return  Math.abs((float)diff_epoch/(1000*60*60*24)); // 1055545912454
	} catch (ParseException e) {
		return -1;
		//e.printStackTrace();
	}
  }
  
  public static int strTimeToCol(String strTime, Instr InstrX) {  
	int timeCol;    
	
	strTime = strTime.trim().toLowerCase();
	
    if (strTime.equals("o")) {
    	timeCol = InstrX.opnDyCol;
    } else if (strTime.equals("c")) {
    	timeCol = InstrX.clsDyCol;
    } else {
        if (strTime.length() < 4) {
            strTime = "0" + strTime;	  
        }
        //* ex: 0900  1130
        strTime = strTime.substring(0,2) + ":" + strTime.substring(2);          
        timeCol = InstrX.firstTimeCol;
        while(timeCol <= InstrX.lastTimeCol && !strTime.equals(InstrX.prcTime[timeCol]))
          timeCol++;
        if (timeCol > InstrX.lastTimeCol) {
          // need to throw error  
        }
    }    
    
	return timeCol;
  }
  
  
  public boolean checkIfAllImported(String cmdStr) {
    //* Go thru every command line and see if instr is imported 
    //* BUT always import every instr if checked Always Import	    
    //for (int k=0; k<cmdStr.length; k++) {
	  
    for (int r=0; r<InstrSpecs.idNames.length; r++) {	
    	  String strInstr = InstrSpecs.idNames[r] + ".";	
  		  strInstr = strInstr.toLowerCase();
  		  if (cmdStr.indexOf(strInstr) >= 0) {
  		      Instr InstrX = Instr.getInstance(r);	
  		      if (!InstrX.blImported) {
  		          return false;	
  		      }
  		  }
  		}
          
      //}
      return true;         
	}  

}  
