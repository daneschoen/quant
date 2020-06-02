package program;

public class PostFilter_RecProf { //extends Strategy_Abstract{
   
  static String strCmdLine;	
  
  private int cmdEql;
  private double cmdAvgPts;
  private int cmdNbrTrades;
  private int cmdDysHold;
  private int cmdHoldTimeCol;
  
  private Utils utils;
  private ParseUtils2 parseUtils;
  
  Session session;
  Instr InstrDep;
  Trades trds;
  
  public int[] prcSucc;
  
  
  public PostFilter_RecProf(Session session, Trades trds) {
  	//super(InstrX, cmdStatement, session);
	this.session = session;
	this.InstrDep = session.InstrDep;
	this.trds = trds;
	  
  	utils = new Utils();
  	parseUtils = new ParseUtils2(session);
  	
  	prcSucc = new int[InstrDep.prc.length];
  }
    
  
  public Trades go() throws Exception{
    parseAndSetConditions();
	calc();
	filter();
	return trds;
  }
  
  public void filter() throws Exception{
    for (int i=InstrDep.maxDysBk; i<=session.endTstDateIndex; i++) {	
	    if(prcSucc[i] == 1)	
	      trds.conditionDy[i] = 1;	
        else 
    	  trds.conditionDy[i] = 0;  
    }	  
  }
  
  /*** 
   * RECPROF(+/- days, hold days, hold time) 
   * recprof(2, 1, 1620) > 2.5
   */ 	  	  
  public void parseAndSetConditions() throws Exception{    
	String[] strCmdLines = parseUtils.getArrCmd(session.str_postscenario);
	String cmdLine="";
    for(String strCmd: strCmdLines) {
       if (strCmd.indexOf("recprof") == 0) {
    	   cmdLine = strCmd;
    	   break;
       }
    }
    strCmdLine = cmdLine;    
    session.str_postfilter_recprof = strCmdLine;
    //* >,>=,<,<=     prevtrade(2,  1, 1620) > 2.5
    int y_gtls = -1;
    int y_ = -1;
    if (cmdLine.lastIndexOf(">=") >= 0) {
    	y_gtls = cmdLine.lastIndexOf(">=");  
    	y_ = 2;	  
    	cmdEql = 1;
    } else if (cmdLine.lastIndexOf(">") >= 0) {
    	y_gtls = cmdLine.lastIndexOf(">");
    	y_ = 1;	  
    	cmdEql = 0;
    } else if (cmdLine.lastIndexOf("<=") >= 0) {
    	y_gtls = cmdLine.lastIndexOf("<=");
    	y_ = 2;	  
    	cmdEql = 3;
    } else if (cmdLine.lastIndexOf("<") >= 0) {
    	y_gtls = cmdLine.lastIndexOf("<");
    	y_ = 1;	  
    	cmdEql = 2;
    } else if (cmdLine.lastIndexOf("=") >= 0) {
    	y_gtls = cmdLine.lastIndexOf("=");
    	y_ = 1;	  
    	cmdEql = 4;		
    }
      	  
    //* Parse cmdAvgPts   prevtrade(2,  1, 1620) > 2.5
    String strAvgPts = cmdLine.substring(y_gtls+y_);
    strAvgPts = strAvgPts.trim();
    cmdAvgPts = Double.parseDouble(strAvgPts);	  
    cmdLine = cmdLine.substring(0,y_gtls);
    cmdLine = cmdLine.trim();

    //* Parse cmdNbrTrades   prevtrade(2,  1, 1620) > 2.5
	int t_P0 = cmdLine.indexOf("(");  	  
	int t_P1 = cmdLine.lastIndexOf(")");
  	cmdLine = cmdLine.substring(t_P0+1,t_P1);
    cmdLine = cmdLine.trim();         //* "2, 0,1620"
    int y_C = cmdLine.indexOf(",");      //* first comma
    cmdNbrTrades = Integer.parseInt(cmdLine.substring(0,y_C));
    cmdLine = cmdLine.substring(y_C+1);
    cmdLine = cmdLine.trim();

    //* Parse holding period    prevtrade(2,  1, 1620) > 2.5
    //* first holding days
    y_C = cmdLine.indexOf(",");      //* 2nd comma
    cmdDysHold = Integer.parseInt(cmdLine.substring(0,y_C));
    cmdLine = cmdLine.substring(y_C+1);
    cmdLine = cmdLine.trim();

    //cmdHoldTimeCol = utils.strTimeToCol(cmdLine, InstrX);
    cmdHoldTimeCol = InstrDep.getTimeCol(cmdLine);
  
  }
  
  
  public void calc() throws Exception{
	
    double prcRefSignal;
    double avgPl;
    int cntTrades;
    int k;
    boolean blInsideBounds;
    boolean blSignal;   
    
	int timeRefCol = session.entryfixed_timecol;
	//Strategy strategy = new Strategy();
	
	//* cmdEql  cmdAvgPts  cmdNbrTrades  cmdDysHold  cmdHoldTimeCol
	
    for (int i=InstrDep.prc.length-1; i>=InstrDep.maxDysBk; i--) {		
      if (trds.conditionDy[i]==1) {    //* now decide to include this or not
          avgPl = 0.0;		
          cntTrades = 0;
    	  k = 1;
      	  blInsideBounds = true;
      	  //* Now go back cmdNbrTrades to see if < or > cmdAvgPts
          while (cntTrades < cmdNbrTrades && blInsideBounds) {
            if (i-k >= 0) {  //* not enuf back trades, dont test prcSuccess[I]  
            	if (trds.conditionDy[i-k] == 1) { 
             	    if (i-k+cmdDysHold < InstrDep.prc.length) {	
            	        cntTrades++; 	
      		            prcRefSignal = InstrDep.prc[i-k][timeRefCol];  //* "PLAST" - the reference price
                        avgPl += InstrDep.prc[i-k+cmdDysHold][cmdHoldTimeCol] - prcRefSignal;              
            	    } else {
            		    blInsideBounds = false;
            	    }         //* if upperbound
                }         //* if prcSuccess
            } else {  //* if lowerbound
            	blInsideBounds = false;
            }	
            k++;
          }  //* while loop
          
          if (blInsideBounds && cntTrades == cmdNbrTrades) {  //* recprof(2, 1, 1620) > 2.5   	  
         	  avgPl /= cmdNbrTrades;  
              blSignal = false; 	    
           	  switch (cmdEql) {   // > or < etc...
            	case 0:  // >
           	      if (avgPl > cmdAvgPts) {  
           		      blSignal = true;  
           	   	  } else { 
           	   		  blSignal = false;
           	   	  }
           	      break;
           		case 1:  // >=
           	  	  if (avgPl >= cmdAvgPts) {
           		   	  blSignal = true;  
           		   } else { 
           			   blSignal = false;
           		   }
           		   break;		
            	case 2:  // < 
            	  if (avgPl < cmdAvgPts) {  
            	      blSignal = true;  
            	  } else { 
            		  blSignal = false;
            	  }                 	  
           		  break;	
            	case 3:  // <=
            	  if (avgPl <= cmdAvgPts) {  
            	      blSignal = true;  
        		  } else { 
        			  blSignal = false;
        		  }
            	  break;		
                case 4:  // =
            	  if (avgPl == cmdAvgPts) {
            		  blSignal = true;  
            	  } else { 
            		  blSignal = false;
            	  }
            	  break;
           	  }   		  	  	  
        			        
              if (blSignal) {   
               	  prcSucc[i] = 1;
              } else {
                  prcSucc[i] = 0;
              }
              
          }  //* if blInsideBounds			            		

      }  //* if prcSuccess
    }  //* for loop
      
  }  //* calc method
	
}	
