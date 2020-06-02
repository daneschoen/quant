package program;

public class Mod_Event {

  /*
   * b > mvg(p@1430, 15, min) 
   * b > mvg(b, 15, min)
   * 
   */
  private Instr InstrDep; 
	
  public Mod_Event() {
    InstrDep = Instr.getInstance(Strategy.iDependentInstr);
  }
	  
  public void run() throws Exception{
	  
  }
  
  public void calcTradesIntrady(String strEvt) throws Exception{  //* enter at intrady evt, not fixed time | given day evt occurred
    /* 
	 * E(0d@Ref)					enter at Ref time
	 * E(0d@Ref->) > p@Ref + 5      to inf, 24hr
	 * E(0p@Ref->30m) > h1
	 * E(0d@Ref->30m) < l(p1@0600,p1@1615)
	 * E(0p@1800->2d@1615, 0000->0600) > h1
	 * E > p@ref + 2.0z
	 * 
	 * E <= mvg(b,10m)
	 * E <= mvg(b5,1h)
	 * b(0p@Ref->1p@1615, 1800->0600) > b + 5
     */
	  
        /* if (blEventIntradyEnter):
         *   parse: strEnterIntradyWindow;           
    	 *   if (prcEnter[i]==1):
    	 *     search intraday for entry, uptill the search end day&time
    	 *     
    	 * else
    	 *   calc dy enter normally
    	 * 
    	 * if (blEventIntradyExit):
         *   parse: strExitIntradyWindow;           
    	 *   if (prcExit[i]==1):
    	 *     search intraday for exit uptill the search end day&time
    	 * else    
    	 *   calc dy exit normally
    	 *
    	 *     int evtIntradyEnterSearchDyFwd=0;	  
        String evtIntradyEnterSearchstrTime="";  
        int evtIntradyEnterSearchTimeCol=InstrDep.lastTimeCol;  
        int evtIntradyExitSearchDyFwd=0;	  
        String evtIntradyExitSearchstrTime="";  
        int evtIntradyExitSearchTimeCol=InstrDep.lastTimeCol; 
    	 */ 
	  /* Must return:
	   *  Strategy.trdEntryDyIndex
	   *  Strategy.trdEntryMinIndex
	   *  Strategy.trdEntryDyCondIndex
	   *  
	   *  All these must have been set BEFORE:
	   *  evtBegFrameTimeCol, evtEndFrameTimeCol
	   *  evtBegTimeCol, evtEndTimeCol
	   *  evtBegDyFwd, evtEndDyFwd
	   */
		
		double ptsEnter;
	    double prc_ij;	  
	    double prcThresh_i;
	    int i;	  
		
	    Parser parser = new Parser();
	    parser.runConditionEntryOnly();  //* gets back Strategy.trdCondDyIndex  
	    //* now need to calc: Strategy.trdEntryDyIndex, Strategy.trdEntryMinIndex
	    //* cuz not every trdCondDyIndex will turn into actual trade    

	    Strat_HighLow strat_HighLow = null;
	    if (strLvlEvent.equals("h1")) {
	    	ptsEnter = 1;
	    } else if (strLvlEvent.equals("l1")) {
	    	ptsEnter = -1;
	    } else if (strLvlEvent.indexOf("h(") >= 0) {
	    	strat_HighLow = new Strat_HighLow("h(p1@0600,p1@1615)");
	    	strat_HighLow.InstrX = InstrDep;
	    	strat_HighLow.parseAndSetConditions();
	    	ptsEnter = 1;
	    } else if (strLvlEvent.indexOf("l(") >= 0) {
	    	strat_HighLow = new Strat_HighLow("l(p1@0600,p1@1615)");
	    	strat_HighLow.InstrX = InstrDep;
	    	strat_HighLow.parseAndSetConditions();
	    	ptsEnter = -1;
	    } else {
	    	ptsEnter = Double.parseDouble(strLvlEvent);
	    }
	    
	    for (int tCondIdx=0; tCondIdx < Strategy.trdCondDyIndex.size(); tCondIdx++) {
	       i = Strategy.trdCondDyIndex.get(tCondIdx); 	
	       if(i+cmdExitTimeTarget_DysFwd > Strategy.endTstDateIndex)
	    	 break;
	       //System.out.println(InstrDep.getYear(i)+"/"+InstrDep.getMonth(i)+"/"+InstrDep.getDay(i));      
	       if (strLvlEvent.equals("h1")) {
	    	   prcThresh_i = InstrDep.prc[i-1][InstrDep.hi24Col];
	           //System.out.println(" " + prcThresh_i + " " + Strategy.timeRefCol);  
	           //System.out.println(" " + InstrDep.prc[i + evtBegDyFwd][evtBegTimeCol]);  
	       } else if (strLvlEvent.equals("l1")) {    	   
	    	   prcThresh_i = InstrDep.prc[i-1][InstrDep.lo24Col];
	       } else if (strLvlEvent.indexOf("h(") >= 0) {
	    	   prcThresh_i = strat_HighLow.calcHigh(i);   
	       } else if (strLvlEvent.indexOf("l(") >= 0) {
	    	   prcThresh_i = strat_HighLow.calcLow(i);
	       } else { 	
	    	   prcThresh_i = InstrDep.prc[i][Strategy.timeRefCol] + ptsEnter; 	
	       }
	       //System.out.println(" " + evtBegDyFwd + ","+ evtBegTimeCol + " to " + evtEndDyFwd+ "," + evtEndTimeCol);       
	       boolean blFoundEvent = false;
	       int startCol;
	       int endCol;
	       for (int iDysFwd=evtBegDyFwd; iDysFwd<=evtEndDyFwd; iDysFwd++) {	
	      	  
	    	  startCol = evtBegFrameTimeCol; 
	          if(iDysFwd == evtBegDyFwd) 
	      	    startCol = evtBegTimeCol; 
	          endCol = evtEndFrameTimeCol;  
	      	  if(iDysFwd == evtEndDyFwd) 
	      	    endCol = evtEndTimeCol;
	      		      
	          for (int j=startCol; j<=endCol; j++) {  //* go across time
	             prc_ij = InstrDep.prc[i + iDysFwd][j];
	      	     if ((ptsEnter <  0 && prc_ij <= prcThresh_i) || 
	      		     (ptsEnter >= 0 && prc_ij >= prcThresh_i)) { 
	      	    	 
	      	    	 Strategy.trdEntryDyIndex.add(i + iDysFwd);   	
	      	    	 Strategy.trdEntryDyCondIndex.add(i);
	      	    	 Strategy.trdEntryMinIndex.add(j);	 
	      	    	 Strategy.trdEntryPrc.add(prc_ij);  //prcThresh_i
	      	    	 
	      	    	 blFoundEvent = true;
			         break;
	      	     }        
	      	  }  //*  for look across in time 
	      	  if(blFoundEvent) break;
	      }  //* for look fwd in days
	      //* quite possible no event entry given cond dy
	   }  //* i next cond dy
	   
	   calcTrades_Exit();
	   
	  }
	  
	  /* Must return:
	   *  Strategy.trdEntryDyIndex
	   *  Strategy.trdEntryMinIndex
	   *  Strategy.trdEntryPrc
	   */
	  public void calcTradesEventIntradyEntryZ(String strZThresh) throws Exception{  //* given day evt occurred | enter at intrady evt, NOT time
	    /* For now - this is for hilo only: 
	     *  b > Ref + "5", 0, 1615, day/all
		 *  b > Ref + "2.0z"
	     *  b < Ref - "1.5z"
		 */  
		int cmdStdPeriod = 40;  
	    double zThresh = Double.parseDouble(strZThresh.substring(0,strZThresh.lastIndexOf("z")).trim());
	    int i;	 
	    double prcRef_i;
	    
	    Parser parser = new Parser();
	    parser.runConditionEntryOnly();  //* gets back Strategy.trdCondDyIndex
	    if(Strategy.maxDysBk < cmdStdPeriod+1) 
	      Strategy.maxDysBk = cmdStdPeriod+1;
	    //* now need to calc: Strategy.trdEntryDyIndex, Strategy.trdEntryMinIndex
	    //* cuz not every trdCondDyIndex will turn into actual trade  
	    
	    for (int idx=0; idx<Strategy.trdCondDyIndex.size(); idx++) {
	       i = Strategy.trdCondDyIndex.get(idx); 	
		   prcRef_i = InstrDep.prc[i][Strategy.timeRefCol];
		
	  	   String ret = searchEvtZ(evtBegFrameTimeCol, evtEndFrameTimeCol, 
	                               evtBegTimeCol, evtEndTimeCol,
	                               evtBegDyFwd, evtEndDyFwd, 
	                               i, prcRef_i, zThresh, cmdStdPeriod);
		   if (ret.length()>0) {
		       String params[] = ret.split(",");
	           int evtDy = Integer.parseInt(params[0]);	   
	           int evtTimeCol = Integer.parseInt(params[1]);
	           double evtPrc = Double.valueOf(params[2]);  //InstrDep.prc[exitFirstDayIndex][exitFirstTimeCol];  //enterPrc_t + cmdfdProfitTarget;
	           
		       Strategy.trdEntryDyIndex.add(evtDy);   	
		       Strategy.trdEntryDyCondIndex.add(i);
		       Strategy.trdEntryMinIndex.add(evtTimeCol);	 
		       Strategy.trdEntryPrc.add(evtPrc);  
		   }
	       //* quite possible no event entry given cond dy
	    }  //* i next cond dy
	   
	    calcTrades_Exit();
	  }

	
}
