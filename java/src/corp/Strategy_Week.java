package program;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.GregorianCalendar;

public class Strategy_Week extends Strategy_Abstract{

  private ArrayList<String> params = new ArrayList<String>(); 
  private int cmdParam;

  @Override
  void parseAndSetConditions(final String strCmdLine) throws Exception{

	//* WEEK(1,..,5)	
	params = getParams(strCmdLine);
  }
  

  public void calc() throws Exception{

    boolean signal=false;		      
	for (int i=Strategy.begTstDateIndex; i<=Strategy.endTstDateIndex; i++) {		
  
      signal=false;
	  for (int p=0; p<params.size(); p++) { 
	    if (InstrDep.getWeek(i) == Integer.parseInt(params.get(p))) {
	        signal = true;  		  
		    break;
		}    			      
      }
      
      if (signal) {   
	      ParserCondition.prcSucc[i] = 1;
	  } else {
	      ParserCondition.prcSucc[i] = 0;
	  }			  
      
	}  //* for i loop
		
  }  // Method calc
}
