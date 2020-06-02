package program;

import java.util.ArrayList;


public class Strategy_Econ extends Strategy_Abstract{

  private ArrayList<String> params = new ArrayList<String>(); 	
  private int cmdParam;
  private int cmdInstrNum;
  private String cmdInstrSuffix;
  private String cmdEconFnName;
  
	 
  Strategy_Econ(final Instr InstrX, final String cmdStatement, final Session session) {
	super(InstrX, cmdStatement, session);
  }
  
  @Override
  public void parseAndSetConditions() throws Exception{  
    String strCmd = cmdStatement;	    		
	if (strCmd.indexOf("hol") >= 0) {
	    cmdParam = 0;	
	} else if (strCmd.indexOf("econ") >= 0) {
		cmdParam = 1;
	}
	
	params = getParams(strCmd);
	
	cmdInstrNum = InstrX.key;    //* first set to default  // 1
    cmdInstrSuffix = InstrSpecs.idNames[cmdInstrNum].toLowerCase();   // da     
	int y_Instr = 0;
	for (int k=0;k<InstrSpecs.idNames.length;k++) {	
      String strOverideDefaultInstr = InstrSpecs.idNames[k] + ".";	
	  strOverideDefaultInstr = strOverideDefaultInstr.toLowerCase();
      if (strCmd.indexOf(strOverideDefaultInstr) >= 0) {
	      cmdInstrNum = k;  // instr
	      cmdInstrSuffix = InstrSpecs.idNames[k];
	      cmdInstrSuffix = cmdInstrSuffix.toLowerCase(); 
	      y_Instr = strCmd.indexOf(".");
	      strCmd = strCmd.substring(y_Instr+1);
	      break;
	  }
	}       		
		
	cmdEconFnName = strCmd.substring(0,strCmd.indexOf("(")).trim();	
			
  }
	  
  @Override
  public void calc() throws Exception{
    if (cmdParam == 1) {  //* econ_fomc
    	      
        Econ EconX = Econ.getInstance(cmdEconFnName);  
        
        int k;
        int cmdDay;
        for (int i=InstrX.maxDysBk; i<InstrX.prc.length; i++) {		
	        prcSucc[i] = 0;  //* just set to default false	
			
		    k=0;
		    boolean blMatchDay=false;
		    //for (int p=0; p<params.size(); p++) {
		    for (int p=0; p<1; p++) {
		        cmdDay = Integer.parseInt(params.get(p));
		      //if(i-cmdDay < session.begTstDateIndex || i-cmdDay > session.endTstDateIndex)
		        if(i-cmdDay <= InstrX.maxDysBk || i-cmdDay >= InstrX.prc.length)
		    	  continue;
			    while (k<EconX.dt.length) {  			  
		            if (EconX.dt[k].equals(InstrX.prcDate[i-cmdDay])) {
		            	blMatchDay = true;
		                break;
		            } 
		            
		    	    k++;
			    }
			    
			    if (blMatchDay) {
			    	prcSucc[i] = 1;	  
			    	break; 	
			    }  
		    }   	  
		    
		}  //* for i loop
	
    } else {  //* HOL: not hol(0), us.hol(1) , hol(-2) , hol(-3,-1)
    	
        Instr InstrCmd = Instr.getInstance(cmdInstrNum);  //* could simply be default dep instr
        String cmdEconNameKey = cmdEconFnName + cmdInstrSuffix;   //* convert: us.hol(1) => holus
        Econ EconX = Econ.getInstance(cmdEconNameKey);  
	  		
		  /* 07/01/2007
		   * 07/02/2007
		   *             07/04/2007
		   * 07/07/2007
		   * 07/08/2007
		   * 07/10/2007
		   */  
	      /* 07/01/2007
		   * 07/02/2007
		   *             07/04/2007
		   *             07/07/2007
		   * 07/08/2007
		   * 07/10/2007
		   */  
	    int k;
	    int cmdDay;			     	
	    for (int i=InstrX.maxDysBk; i<InstrX.prc.length; i++) {			
	        prcSucc[i] = 0;  //* just set to default false	
			
		    k=0;
		    boolean blMatchDay = false;
		    //for (int p=0; p<params.size(); p++) {
		    for (int p=0; p<1; p++) {	
		        cmdDay = Integer.parseInt(params.get(p));
		        if(i-cmdDay <= InstrX.maxDysBk || i-cmdDay >= InstrX.prc.length)
		    	  continue;
			    while (k<EconX.dt.length) {  			
			    	if (cmdDay == 0) {
			    	    if (EconX.dt[k].equals(InstrCmd.prcDate[i-cmdDay])) {
		            	    blMatchDay = true;
		                    break;
		                }
			    	} else if (cmdDay > 0) {
			    	    if (EconX.dt[k].equals(InstrCmd.prcDate[i-cmdDay]) ||
			    	       (EconX.dt[k].after(InstrCmd.prcDate[i-cmdDay]) &&	
			    	        EconX.dt[k].before(InstrCmd.prcDate[i-cmdDay+1]))) {
		            	    blMatchDay = true;
		                    break;
		                }			    		
			    	} else if (cmdDay < 0) {
			    	    if (EconX.dt[k].equals(InstrCmd.prcDate[i-cmdDay]) ||
					       (EconX.dt[k].before(InstrCmd.prcDate[i-cmdDay]) &&	
					    	EconX.dt[k].after(InstrCmd.prcDate[i-cmdDay-1]))) {
				            blMatchDay = true;
				            break;
				        }			    					    		
			    	}
		    	    k++;
			    }
			    
			    if (blMatchDay) {
			    	prcSucc[i] = 1;	  
			    	break; 	
			    }  
		    }   	  
		    
		}  //* for i loop				
    }  //* if econ or hol fn
    
  }  // Method calc  
	
}
