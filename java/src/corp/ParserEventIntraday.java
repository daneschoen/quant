package program;

import java.util.ArrayList;


class ParserEventIntraday extends ParserAbstract {
  
  Strategy_Abstract[] cmd;	
	
  //* Used for Entry AND Exit !
  ParserEventIntraday(String strEvtIntradyWindow) {
    super();
    strCmdWindow = strEvtIntradyWindow;
    //Strategy.prcSuccess = new int[InstrDep.maxPrcIndex+1];
    Strategy.trdEntryDyIndex = new ArrayList<Integer>();
    Strategy.trdEntryDyCondIndex = new ArrayList<Integer>();
    Strategy.trdEntryMinIndex = new ArrayList<Integer>();
    Strategy.trdEntryPrc = new ArrayList<Double>();
  }

  
  void go() throws Exception{
	if(!chkIfImported()) 
	  throw new ExceptionCmd("Error - Instrument(s) not imported");
    createArrayCmdStr();
    createArrayCmd();
	parseAndCalcStrategies();
  }	  
  
  private void createArrayCmd() throws Exception{  	      

    cmd = new Strategy_CompIntraday[cmdLine.length]; //* just set array depth;

	for (int k=0; k<cmd.length; k++) {
	  cmd[k] = new Strategy_CompIntraday();	  
	  cmd[k].parseAndSetConditions(cmdLine[k]);
	}  
	
  } 
	  
  private void parseAndRun_Strategy(Strategy_Abstract strategy, String cmdStrLine) throws Exception{
    strategy.nested = 0;
    strategy.parseAndSetConditions(cmdStrLine); 
    strategy.calc();
  }    

	     
  void parseAndCalcStrategies() throws Exception{ 	  
    /* 
        streak(b<b1:30) = 3             no nesting
	    dayweek(1,3)                    no nesting
	   
	  search(0630,1420):
	    E > L1 - 5
	    E > p@1800
        E > mvg(c, 15min)
        E > mvg(b, 15min)
        E > c1 + 3

        E < p@1615 - 1
        E > h1

        E < p@1615 - 0.25z
      
      search(all):  
        E > b0h1m12s  means enter when greater than bar 1 min 12 seconds ago   
    */   
	  
    //* MUST Reset to 0 for each whole new RUN (not cmdLine !), also max index
    Strategy.prcSuccess = new int[InstrDep.maxPrcIndex+1];
	  
    for (int k=0; k<cmdLine.length; k++) {
	          
      //* MUST reset for each new CMD line, not just run!
	  prcSucc = new int[InstrDep.maxPrcIndex+1];  
	          
	  if (cmdLine[k].indexOf("wait(") == 0) {	
	      parseAndRun_Strategy(new Strategy_Wait(), cmdLine[k]);
	  } else if (cmdLine[k].indexOf("first(") == 0) {
		  parseAndRun_Strategy(new Strategy_First(), cmdLine[k]); 	      
	  } else if (cmdLine[k].indexOf("streak(") == 0 && AGlobal.BUILD_VER==0) {
	       parseAndRun_Strategy(new Strategy_Streak() , cmdLine[k]);
	  } else if (cmdLine[k].indexOf("countpure(") == 0 && AGlobal.BUILD_VER==1) {
		 parseAndRun_Strategy(new Strategy_Countpure(), cmdLine[k]);  
	  } else if (cmdLine[k].indexOf("count(") == 0) {
		 parseAndRun_Strategy(new Strategy_Count(), cmdLine[k]);  
	  } else if (cmdLine[k].indexOf("rank(") == 0  && AGlobal.BUILD_VER==0) {
		 parseAndRun_Strategy(new Strategy_Rank(),cmdLine[k]);  
	  } else if (cmdLine[k].indexOf("sum(") == 0  && AGlobal.BUILD_VER==0) {
		 parseAndRun_Strategy(new Strategy_Sum(), cmdLine[k]);
	  } else if (cmdLine[k].indexOf("tradeday(") == 0) {
		 parseAndRun_Strategy(new Strategy_Tradeday(), cmdLine[k]);
	  } else if (cmdLine[k].indexOf("day(") == 0) {
		 parseAndRun_Strategy(new Strategy_Date(), cmdLine[k]);
	  } else if (cmdLine[k].indexOf("month(") == 0) {
		 parseAndRun_Strategy(new Strategy_Date(), cmdLine[k]);
	  } else if (cmdLine[k].indexOf("dayweek(") == 0  && AGlobal.BUILD_VER==1) {
		 parseAndRun_Strategy(new Strategy_Dayweek(), cmdLine[k]);        	  
	  } else if (cmdLine[k].indexOf("hol(") == 0) {
		 parseAndRun_Strategy(new Strategy_Econ(), cmdLine[k]);
	  } else if (cmdLine[k].indexOf("econ") == 0) {
		 parseAndRun_Strategy(new Strategy_Econ(), cmdLine[k]);
	  } else if (cmdLine[k].indexOf("volhist(") == 0 && AGlobal.BUILD_VER == 0) {
	     parseAndRun_Strategy(new Strategy_VolHist(), cmdLine[k]);
	  } else if (cmdLine[k].indexOf("volhilo(") == 0) {
	     // parseAndRun_VolHiLo(cmdLines[k]);
	  } else if (cmdLine[k].indexOf("vix(") == 0) {
		 parseAndRun_Strategy(new Strategy_Vix(), cmdLine[k]);        	  
	  } else if (cmdLine[k].indexOf("stdev(") == 0 && AGlobal.BUILD_VER == 0) {
		 parseAndRun_Strategy(new Strategy_Stdev(), cmdLine[k]);      
	  } else if (cmdLine[k].indexOf("zscore(") == 0 && AGlobal.BUILD_VER == 0) {
	     parseAndRun_Strategy(new Strategy_Zscore(), cmdLine[k]);  
	  } else if (cmdLine[k].indexOf("pivot(") == 0 && AGlobal.BUILD_VER == 0) {
		 parseAndRun_Strategy(new Strategy_Pivot(), cmdLine[k]);           
	  } else if (cmdLine[k].indexOf("candle") == 0 && AGlobal.BUILD_VER == 1) {
		  parseAndRun_Strategy(new Strategy_Candle(), cmdLine[k]);
      } else if (cmdLine[k].indexOf("regnonlinear1(") == 0 && AGlobal.BUILD_VER == 1) {
    	 //parseAndRun_RegNonlinear(cmdLine[k]);                	  
	 
	  } else {   //* Lastly the most simple C > C1, P1@1100 > O, etc. min/max, h/l, mvg
	      parseAndRun_Strategy(new Strategy_Compare(), cmdLine[k]);
	  }
	                    
      //* Here set succ dep on OR, AND, NOT
	  if (k==0) {   //* Automatically OR for very first cmdLines[0]
	      for (int i=Strategy.begTstDateIndex; i<=Strategy.endTstDateIndex;i++) {	
		     if ((prcSucc[i] == 1 && cmdLineNot[k] == 0) ||
			    (prcSucc[i] == 0 && cmdLineNot[k] == 1)) {
	            Strategy.prcSuccess[i] = 1;	
	         } 
	       }
	   /*	
	   } else if (cmdLinesOr[k-1] == 1) {
	        	  for (int i=Strategy.begTstDateIndex; i<=Strategy.endTstDateIndex;i++) {	
	            	if ((prcSucc[i] == 1 && cmdLinesNot[k] == 0) ||
	                  	(prcSucc[i] == 0 && cmdLinesNot[k] == 1)) {
	                    Strategy.prcSuccess[i] = 1;	
	                }   //* else if (prcSucc[i] == 0) { stays same! }
	        	  }
	   */        	  
      } else {  //* Default AND
	      for (int i=Strategy.begTstDateIndex; i<=Strategy.endTstDateIndex;i++) {	
	           if (((prcSucc[i] == 1 && cmdLineNot[k] == 0) || (prcSucc[i] == 0 && cmdLineNot[k] == 1))  
	               && Strategy.prcSuccess[i] == 1) {
	               Strategy.prcSuccess[i] = 1;	
	           } else {
	               Strategy.prcSuccess[i] = 0;  
	           }
	      }
      }  //* if AND or OR

    }  //* for k loop of cmd's

  }
  
  
  
}