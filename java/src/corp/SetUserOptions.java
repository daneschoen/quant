package program;


public class SetUserOptions {
  
  private Session session;
  private Instr InstrDep;
  
  public SetUserOptions(Session session){
    this.session = session;  
    InstrDep = session.InstrDep;
  } 
  
  
  public void parseAndSetViewForStatistics() throws Exception{ 
	try {
	  //* run fr Parser right before Strategy.calcStatsAndDisplay() 
	  /* SetNumObs(10)
	   * SetViewTimes(3, 6, 2, 10)  SetViewTimes(120, 6, 2, 10)
	   * SetViewStartTime(0230)
       */			
	  String strUserCmds = session.strViewOptionsWindow;
      if (strUserCmds.length() == 0) {
    	throw new ExceptionSetUserOption("ERROR: Setting View Options - commands are empty");
      }  	
      for (String strCmdLine : strUserCmds.split("\n")) {	
    	strCmdLine = strCmdLine.trim().toLowerCase();    	        	
	    if (strCmdLine.indexOf("setnumobs") == 0) {	      	 	        	 	        	  
	        setNumObs(strCmdLine); 
	    } else if (strCmdLine.indexOf("setviewtimes") == 0) {        	 	        	 
	        setViewTimes(strCmdLine); 
	    } else if (strCmdLine.indexOf("setviewstarttime") == 0) {        	 	        	 
	        setViewStartTime(strCmdLine); 
	    }
         
	  }
    
    } catch(Exception e) {
      throw new ExceptionSetUserOption("ERROR: Setting View Options");
    }	
  }
  
  public void setNumObs(String strUserLine){    
    int t_P0 = strUserLine.indexOf("(");  	  
    int t_P1 = strUserLine.lastIndexOf(")");
    String strCmdLine = strUserLine.substring(t_P0+1,t_P1);
    strCmdLine = strCmdLine.trim().toLowerCase(); 
    session.viewNumObs = Integer.parseInt(strCmdLine);	
  }
		
  public void setViewStartTime(String strUserLine) throws Exception{
    int t_P0 = strUserLine.indexOf("(");  	  
	int t_P1 = strUserLine.lastIndexOf(")");
	String strCmdLine = strUserLine.substring(t_P0+1,t_P1);
	String strTime = strCmdLine.trim().toLowerCase(); 
	//Strategy.cmdUserViewStartTimeCol = Utils.strTimeToCol(strTime, Instr.getInstance(Strategy.iDependentInstr));
	session.viewHideEndTimeCol = InstrDep.getTimeCol(strTime)-1;
	session.viewHideBegTimeCol = InstrDep.lastTimeCol+1;  //* ie 1615->1700
  }
			  
  
  public void setViewTimes(String strUserLine) throws Exception{ 
	  			
  	int y_P0 = strUserLine.indexOf("(");  	  
	int y_P1 = strUserLine.lastIndexOf(")");
  	String strCmdLine = strUserLine.substring(y_P0+1,y_P1);
    strCmdLine = strCmdLine.trim().toLowerCase();  // "3,6,2,10"
    String[] params = strCmdLine.split(",");
    
    int numMins = Integer.parseInt(params[0].trim());
    int numHours = Integer.parseInt(params[1].trim());
    int numDays = Integer.parseInt(params[2].trim());
    int incrMin = Integer.parseInt(params[3].trim());
    
    incrMin = incrMin/InstrDep.minIncr;
        
  	/* This has to work for ALL instr which open and cls at any time!
     * And 24 hr
     * [:][0] = relative fwd day(s) , [:][1] = the time column eg 930, etc...
     */
	int[][] fwdDyTimeCol = new int[numMins + numHours + 2*numDays + 100][2];  
	
	String[] insertTimes = new String[2];
	insertTimes[0] = InstrDep.opnTimeStamp; 
	insertTimes[1] = InstrDep.clsTimeStamp; 
	//String[] insertTimes = {"0245","0300","0400","0930","1615"};
	//String[] insertTimes = {"0000","0230","0300","0400","0930","1615","1700","1800","2000"};
	int[] insertTimeCols = new int[insertTimes.length];
	for(int j=0; j<insertTimes.length; j++)
	  insertTimeCols[j] = InstrDep.getTimeCol(insertTimes[j]);
		
	int iNextDy = 0;  //* day roll incrementor in case overflow the close column
	int jTimeCol = session.entryfixed_timecol;
	int gChgSteps=0;
	
	//* Mins
	int incrSteps=0;
	int cntNumMins=0;
	boolean blAdjOnce = false;
	if(jTimeCol == InstrDep.lastTimeCol && InstrDep.prcTime[jTimeCol].endsWith("5") && InstrDep.minIncr == 5) 
	  blAdjOnce = true;
	  
	while (cntNumMins < numMins) {
	    if (jTimeCol+1 > InstrDep.lastTimeCol) {
	    	iNextDy++;
	    	jTimeCol = InstrDep.firstTimeCol;
	    } else {	
	        jTimeCol++;
	    }
	    incrSteps++;
		if (incrSteps==incrMin || blAdjOnce) {		
		  	fwdDyTimeCol[gChgSteps][0] = iNextDy;
		  	fwdDyTimeCol[gChgSteps][1] = jTimeCol;
			gChgSteps++; 
			cntNumMins++;
		    incrSteps = 0;
		    blAdjOnce = false;
		} else {
	    	for (int j=0; j<insertTimeCols.length; j++) {
	            if (jTimeCol == insertTimeCols[j]) {
	            	fwdDyTimeCol[gChgSteps][0] = iNextDy;
	            	fwdDyTimeCol[gChgSteps][1] = insertTimeCols[j];	    		
	    		    gChgSteps++;
	    		    break;
	            }
	    	}
		} 	
	}

	//* Hours right after last 10 min incr
	for (int g=0; g<numHours; g++) {
	    boolean blFoundNextHour=false; 	
	    while (!blFoundNextHour) {
		    if (jTimeCol+1 > InstrDep.lastTimeCol) {
		    	iNextDy++;
		    	jTimeCol = InstrDep.firstTimeCol;
		    } else {	
		        jTimeCol++;
		    }    
		    
		    if (InstrDep.prcTime[jTimeCol].endsWith("00")) { 
			    blFoundNextHour=true;
		    } else {
		        for (int j=0; j<insertTimeCols.length; j++) {
		          if (jTimeCol == insertTimeCols[j]) {
		        	  fwdDyTimeCol[gChgSteps][0] = iNextDy;
		        	  fwdDyTimeCol[gChgSteps][1] = insertTimeCols[j];	    		
		    	      gChgSteps++;
		    	      break;
		          }
		      }
		    }
		    
	    }
		    
	    fwdDyTimeCol[gChgSteps][0] = iNextDy;
	    fwdDyTimeCol[gChgSteps][1] = jTimeCol;
	    gChgSteps++;
    }   
	
	//* rest of that day
	while (jTimeCol+1 <= InstrDep.lastTimeCol) {
      jTimeCol++;		
      for (int j=0; j<insertTimeCols.length; j++) {
        if (jTimeCol == insertTimeCols[j]) {
        	fwdDyTimeCol[gChgSteps][0] = iNextDy;
        	fwdDyTimeCol[gChgSteps][1] = insertTimeCols[j];	    		
    	    gChgSteps++;
    	    break;
        }
      }
	}
	
	//* Now 2 day's of opn and cls
	jTimeCol = InstrDep.firstTimeCol;
	iNextDy++;
	for (int iDy=0; iDy<numDays; iDy++) {
	    for (int j=0; j<insertTimeCols.length; j++) {
	    	fwdDyTimeCol[gChgSteps][0] = iNextDy;
	    	fwdDyTimeCol[gChgSteps][1] = insertTimeCols[j];	    		
	    	gChgSteps++;
	    }
	    iNextDy++;
    }
	
	session.fwdDyTimeCol = new int[gChgSteps][2];
	for (int f=0; f<gChgSteps; f++) {
	  session.fwdDyTimeCol[f][0] = fwdDyTimeCol[f][0];
      session.fwdDyTimeCol[f][1] = fwdDyTimeCol[f][1];	
	}
	
  }  // end fn setViewTimes
  
}
