package program;

import java.util.ArrayList;

public class Strategy_Date extends Strategy_Abstract{

  private ArrayList<String> params = new ArrayList<String>(); 
  private int cmd_type;
  /* 
   * DAY(1,..,5), MONTH(1,..,12) 
   */	

  Strategy_Date(Instr InstrX, String cmdStatement, Session session) {
	super(InstrX, cmdStatement, session);
  }
  
  @Override
  void parseAndSetConditions() throws Exception{

	if (cmdStatement.indexOf("day(") >= 0) {	
		cmd_type = 0;
    } else if (cmdStatement.indexOf("month(") >= 0) {
    	cmd_type = 1;	          	  
    }
	
	params = getParams(cmdStatement);
  }


  public void calc() throws Exception{

    boolean signal=false;		      
	for(int i=InstrX.maxDysBk; i<InstrX.prc.length; i++) {	
  
      switch (cmd_type) {   
		case 0:
		  signal=false;
		  if (session.USERTYPE == 4) {
			 for (int p=0; p<params.size(); p++) { 
			    if (InstrX.getWeekday(i) == Integer.parseInt(params.get(p))) {
			        signal = true;  		  
		            break;
			    }    
			 }     
		  } else {
			  if(InstrX.getWeekday(i) == Integer.parseInt(params.get(0)))
			    signal = true;						  
		  }
		  break;
		case 1:  
		  signal=false;			  
		  for (int p=0; p<params.size(); p++) { 
		    if (Integer.parseInt(InstrX.getMonth(i)) == Integer.parseInt(params.get(p))) {
			    signal = true;  		 
	            break;
		    }
		  } 
		  break;
      }
      
      if(signal)
	    prcSucc[i] = 1;
	  else
	    prcSucc[i] = 0;		  
      
	}  //* for i loop
		
  }  // Method calc
}
