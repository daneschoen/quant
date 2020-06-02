package program;

import program.io.*;


class Strategy_Vix extends Strategy_Abstract{

  static final String CMD = "vix";
  static final String FILE_NAME = "vixdata.txt";
  
  private static final String DATE_FORMAT = "*/*/*";
  private static final int ROW_DATA_START = 2;
  private static final int NUM_DATA_COLS = 1;
  private static final int COL_VIX = 4;
  
  String[] cmdType = new String[2];
  Instr[] cmdInstr = new Instr[2];
  int[] cmdMinMaxDays = new int[2];
  int[] cmdTimeCol = new int[2];
  int[] cmdDaysBk = new int[2];  
  double[] cmdVol = new double[2];
  
  int cmdEql;          	        
	                    
  int cmd_MinMaxDays;
  int cmd_TimeCol;
  int cmd_DaysBk;  
                
  private Instr InstrDep;   
  private Indicators vix;
  private ImportDataFile importVix;	  
  
  
  Strategy_Vix(Instr InstrX, String cmdStatement, Session session) {
	super(InstrX, cmdStatement, session);
  
	InstrDep = InstrX;  
	vix = Indicators.getInstance(CMD);      
	
	//* Check if imported
	if (!vix.blImported) {
	    importVix = new ImportDataFile(CMD);
	    importVix.fileName = FILE_NAME;
	    importVix.strDateFormat = DATE_FORMAT;
	    importVix.numDataCols = NUM_DATA_COLS;
	    importVix.rowStart = ROW_DATA_START;
	    importVix.importFileToObjData();
	    vix.blImported = true;
	}
  }
  
  
  @Override
  public void parseAndSetConditions() throws Exception{
		    
    /* vix(C1) >= 50.4
	 * vix(c1) > vix(c2)
	 * vix(c1) = max(vix(c1),20)
	 */ 
		
	//* Here we go 
	cmdStatement = cmdStatement.trim();
	cmdStatement = cmdStatement.toLowerCase();	
	String[] strSides = new String[2];
    
	ParseUtils parse = new ParseUtils(session);
	parse.splitSides(cmdStatement);
	cmdEql = parse.splitSides_cmdEql;
	strSides = parse.splitSides_strSides;	
	
    for (int s=0; s<2; s++) {
    	String strTok = "";
        if (strSides[s].indexOf(CMD) == 0) {  //* "vix(C1)" >= 50.4
      	    cmdType[s] = "vix"; 
      	    parseAndSetConditions_Side(strSides[s]);
      	    cmdTimeCol[s] = cmd_TimeCol;
      	    cmdDaysBk[s] = cmd_DaysBk; 
      	    
        } else if (strSides[s].indexOf("max") >= 0 || strSides[s].indexOf("min") >= 0) {
        	//* vix(C1) >= "max(vix(c1),20))"
        	if (strSides[s].indexOf("max") >= 0) {
        	    cmdType[s] = "max";
        	} else {
        		cmdType[s] = "min";
        	}
        	int y_Po = strSides[s].indexOf("("); 
        	strTok = strSides[s].substring(y_Po+1).trim();    	  
        	int y_Cm = strTok.indexOf(",");
        	strTok = strTok.substring(0,y_Cm).trim();
        	
      	    parseAndSetConditions_Side(strTok);
      	    cmdTimeCol[s] = cmd_TimeCol;
      	    cmdDaysBk[s] = cmd_DaysBk; 
        	
      	    y_Cm = strSides[s].indexOf(",");
      	    strTok = strSides[s].substring(y_Cm+1).trim();
        	int y_Pc = strTok.indexOf(")");
        	strTok = strTok.substring(0,y_Pc).trim();       	
      		cmdMinMaxDays[s] = Integer.parseInt(strTok);
      		
        } else {   //* vix(C1) >= "50.4"
        	cmdType[s] = "v";
        	strTok = strSides[s].trim();	
        	cmdVol[s] = Double.parseDouble(strTok);
        }
    }
    
  }
  

  public void parseAndSetConditions_Side(String strCmdLine) throws Exception{
	//* 1) vix(c), vix(c2) 
	
	ParseUtils parse = new ParseUtils(session);  
	String strTok;  

	int y_Po = strCmdLine.indexOf("("); 
	strTok = strCmdLine.substring(y_Po+1).trim();    	  
	int y_Pc = strTok.indexOf(")");
	strTok = strTok.substring(0,y_Pc).trim();
	
	parse.OHLC(strTok);   
  	String ohlc = parse.ohlc_Type;
  	if (ohlc.equals("v")) {
  		//* not allowed  
  	} else {
  	    cmd_TimeCol = parse.ohlc_TimeCol;
  	    cmd_DaysBk = parse.ohlc_DaysBk;
  	}	
	
  }	

  @Override
  public void calc() throws Exception{
    /* vix(C1) >= 50.4
     * vix(c1) > vix(c2)
     * vix(c1) = max(vix(c1),20)
     */  
    prcSucc = new int[InstrDep.prc.length];
    
    int maxDaysBk = 0;
    int maxMinMaxDaysBk = 0;
    for (int s=0; s<2; s++) {
      if (cmdDaysBk[s] > maxDaysBk) {
    	  maxDaysBk = cmdDaysBk[s];
      } 
      if (cmdMinMaxDays[s] > maxMinMaxDaysBk) {
    	  maxMinMaxDaysBk = cmdMinMaxDays[s];
      } 
    }
    
    if(InstrDep.maxDysBk < cmd_MinMaxDays) 
       InstrDep.maxDysBk = cmd_MinMaxDays;
    
    double[] lrValue = new double[2];
    for (int i=InstrDep.maxDysBk; i<InstrX.prc.length; i++) {	  
      boolean blVixDateMatch=false;
      for (int lr=0; lr<2; lr++) {	
	    //* First get matching or closest matching date of vix to dep instr for each side!
	    int k=0;
	    blVixDateMatch=false;
	    for (k=0; k<vix.data.length; k++) {	
	      if (vix.date[k].equals(InstrDep.prcDate[i-cmdDaysBk[lr]])) {
	  		  blVixDateMatch = true;
	  		  break;
		  } else if (vix.date[k].after(InstrDep.prcDate[i-cmdDaysBk[lr]])) {
			  if (k-1 >= 0) { 
			      if (vix.date[k-1].before(InstrDep.prcDate[i-cmdDaysBk[lr]])) {
			    	  k--;
			    	  blVixDateMatch = true;
			      }
			  }
			  break;
		  }
	    }
	    if(!blVixDateMatch)
	      break;  //* if either side's date is not found break out TWICE 
	    
		//* Calc each side for current day
		if (cmdType[lr].equals("vix")) {
			lrValue[lr] = vix.data[k][COL_VIX]; 
			
		} else if (cmdType[lr].equals("v")) {  
			lrValue[lr] = cmdVol[lr];
			
		} else if (cmdType[lr].equals("min")) { 	
			//* vix(C1) >= "max(vix(c1),20))"
            double fdMin = Double.MAX_VALUE;
            for (int m=0; m<=cmdMinMaxDays[lr]; m++) {
                 if(fdMin > vix.data[k-m][COL_VIX])
                    fdMin = vix.data[k-m][COL_VIX]; 	  
            }
	        lrValue[lr] = fdMin;
	             				
		} else if (cmdType[lr].equals("max")) {
            double fdMax = Double.MIN_VALUE;
            //for (int m=cmdDaysBk[lr]; m<=cmdDaysBk[lr]+cmdMinMaxDays[lr]; m++) {
            for (int m=0; m<=cmdMinMaxDays[lr]; m++) {
                 if(fdMax < vix.data[k-m][COL_VIX])
                    fdMax = vix.data[k-m][COL_VIX]; 	  
            }
	        lrValue[lr] = fdMax;				
				
		}
      }  //* for s side
	  if(!blVixDateMatch)
		    break;	//* break out of i loop also
      
	  //* Now see for that date if vix is certain value
	  boolean blSignal = false;
	  switch (cmdEql) {   //* > or < etc...
	    case 0:  //* > 
		  if (lrValue[0] > lrValue[1]) {
			  blSignal = true;  
		  } else { 
			  blSignal = false;
		  }
		  break;	      
		case 1:  //* >=
		  if (lrValue[0] >= lrValue[1]) {
		      blSignal = true;  
		  } else { 
			  blSignal = false;
		  }
		  break;	  
		case 2:  //* <
		  if (lrValue[0] < lrValue[1]) {
			  blSignal = true;  
		  } else { 
			  blSignal = false;
		  }
		  break;	  
		case 3:  //* <=
		  if (lrValue[0] <= lrValue[1]) {
		      blSignal = true;  
		  } else { 
			  blSignal = false;
		  }
		  break;	  
	    case 4:  //* =
	       if (lrValue[0] == lrValue[1]) {
			   blSignal = true;  
	  	   } else { 
	  		   blSignal = false;
	  	   }
		   break;	  
	  }  //* switch cmdEql 		  	  	  

      
      if(blSignal)
	    prcSucc[i] = 1;
	  else
	    prcSucc[i] = 0;		  
      
    }  //* for i loop  
	  
  }  //* end method calc()		
	
}

