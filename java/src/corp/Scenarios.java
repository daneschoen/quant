package program;

import java.util.StringTokenizer;

public class Scenarios {

  public static boolean bl_HiLo;
  public static boolean bl_RecProf;

  public static String strCmdWindow;
    
  
  public static void displayDefault(){
	Scenario_HiLo.displayDefault();
	PostFilter_RecProf.displayDefault();
  }
		
  
  public static void parseAndSetAll() throws Exception{  		  
    strCmdWindow = strCmdWindow.trim().toLowerCase();	        
	if (strCmdWindow.length() != 0) {
        //* Just parse line - send real parsing to each method
	    StringTokenizer stLine = new StringTokenizer(strCmdWindow,"\n");
	    int iNumLines = stLine.countTokens();
	    String[] cmdScenarios = new String[iNumLines];        
	    int k=0;
	    while (stLine.hasMoreTokens()) {
	      cmdScenarios[k] = stLine.nextToken();
	      cmdScenarios[k] = cmdScenarios[k].trim();
	      cmdScenarios[k] = cmdScenarios[k].toLowerCase();
	      k++;
	    }
       
	    for (k=0; k<iNumLines; k++) {    	        	
	      if (cmdScenarios[k].indexOf("recprof") == 0) {	      	 	        	 	        	  
	    	  if (bl_RecProf) {
	    		  PostFilter_RecProf.setCmd(cmdScenarios[k]);
	    	  } else {
	    		  PostFilter_RecProf.setCmd("");
	    	  }       	
	      } else if (cmdScenarios[k].indexOf("hilo") == 0) {
	    	  if (bl_HiLo) {
	    		  Scenario_HiLo.setCmd(cmdScenarios[k]);
	    	  } else {
	    		  Scenario_HiLo.setCmd("");
	    	  }
	      }
	    }        
	}  // if strCommandUser is not empty
  
  }
}
