package program;

import java.util.ArrayList;

/* Used for entries AND exits !
 * 
 * Input: trdCondDyIndex
 *        strIntradyWindow
 *        
 *          Event(0@Ref->2@1615, 0000->0600)
 *          Event(0@1800->2@1615)
 *            evtBegDyFwd, evtEndDyFwd;
 *            evtBegTimeCol, evtEndTimeCol;
 *            evtBegFrameTimeCol, evtEndFrameTimeCol;          
 *          b > b5 + 5
 *          b > mvg(b,10m)
 *          b > h1
 *          
 * Output: trades obj
 * 
 * ENTRY:
 *   event(b > h1, range:, delay:, repeat:1)   may not happen within range
 *   
 * 
 */

public class Process_Intrady extends Process_Abstract {
  
  Process_Intrady(Session session, Trades trds) {
	super(session);
	this.trds = trds;
  }

  
  @Override
  Trades go_enter() throws Exception{
	if (session.bl_entry_fixed){  
        for (int i=session.InstrDep.maxDysBk; i<=session.endTstDateIndex; i++) {		
            if(trds.conditionDy[i]!=1)
      	      continue;
            //trds.entryDyIdx.add(i + session.entryfixed_dyfwd);
            trds.entry_cond_dyidx.add(i);
            trds.entry_dyidx.add(i+session.entryfixed_dyfwd);
            trds.entry_dyfwd.add(session.entryfixed_dyfwd);
            trds.entry_timecol.add(session.entryfixed_timecol);

        } 	    
	} else if (session.bl_entry_event) {
		/***
		 * add entry_dyidx, etc, only if event enters!
		 */
	} 
	
	//parseAndCalcStrategies();
	//runPostFilters();
	
	return trds;
  }
  
  
  @Override
  Trades go_exit() throws Exception{
	if (session.bl_exit_fixed){  
        for (int i=session.InstrDep.maxDysBk; i<=session.endTstDateIndex; i++) {		
            if(trds.conditionDy[i] != 1)
      	      continue;
            trds.exit_cond_dyidx.add(i);
            trds.exit_dyidx.add(i + session.exitfixed_dyfwd);
            trds.exit_dyfwd.add(session.exitfixed_dyfwd);
            trds.exit_timecol.add(session.exitfixed_timecol);
        } 
	} else if (session.bl_exit_event) {

	}
	
	return trds;
  }	  

    
  /*
  void parseTimeRef(final String cmdLine) throws Exception { 
	//* TimeRef(f0@0930)
	String arg = cmdLine.substring(cmdLine.indexOf("(")+1, cmdLine.indexOf(")"));
	
	String strDysBkAndTimeCol = parseUtils.parseTok(session.InstrDep, arg);
	ArrayList<String> lst = new ArrayList<String>();
	for(String param : strDysBkAndTimeCol.split(",")) 
	  lst.add(param.trim());
	session.timeRefDyFwd = Integer.parseInt(lst.get(1));
	session.timeRefCol = Integer.parseInt(lst.get(2));	  
  }
  */
    
  void parseEvtParam(String cmdLine) {
    /* 
     * TimeRef(f0@0930)
     * 
     * Event(f0@Ref:f0@1520)
     * Event(f0@Ref:f1@1520)
     * 
     * Event(f0@1800:f1@1520, )	  
     * Event(f0@1800:f1@1520, )
     * 
     * Event(f0@Ref:f0@1520, 1st time)
     * Event(f0@Ref:f0@1520, 5 max)
     * Event(f0@Ref:f0@1520, 3rd time)
     * 
     */
	
	/*
	    arg = params.get(3);
	    String[] args = arg.split(":"); 
	    frameBeg_timeCol = InstrX.getTimeCol(args[0]);
	    frameEnd_timeCol = InstrX.getTimeCol(args[0]);
		
		getParams();
		argExpression = params.get(0);
		String strDysBkAndTimeCol = parseUtils.parseTok(InstrX, argExpression);
	    ArrayList<String> lst = new ArrayList<String>();
	    for(String param : strDysBkAndTimeCol.split(",")) 
	      lst.add(param.trim());
	    dyBk = Integer.parseInt(lst.get(1));
	    timeCol_p = Integer.parseInt(lst.get(2));
    */
  }
  
  
  @Override
  void parseAndCalcStrategies() throws Exception {
	/*  
    for (int k=0; k<cmdLine.length; k++) {
      //* MUST reset for EACH new CMD line, NOT just run!
      //prcSucc = new int[InstrDep.prc.length];  
      Strategy_Abstract strategyX=null; 
      	  
      if (cmdLine[k].indexOf("timeref(") == 0) {
          parseTimeRef(cmdLine[k]);  		  
      } else if (cmdLine[k].indexOf("event(") == 0) {
          parseEvtParam(cmdLine[k]);  		  
          
      } else if (cmdLine[k].indexOf("day(") == 0) {
      		  strategyX = parseAndRun_Strategy(new Strategy_Date(InstrDep, cmdLine[k], session.sessionId));

      } else {   //* Really everything: C > C1, P1@1100 > O, etc. min/max, h/l, mvg 
      		  strategyX = parseAndRun_Strategy(new Strategy_Compare(InstrDep, cmdLine[k], session.sessionId));  
      }              

      	  if (k==0) {	
      	      for (int i=InstrDep.maxDysBk; i<=session.endTstDateIndex; i++) {
      	    	 trds.conditionDy[i] = 0; 
      		     if ((strategyX.prcSucc[i] == 1 && cmdLineNot[k] == 0) ||
      			     (strategyX.prcSucc[i] == 0 && cmdLineNot[k] == 1)) {
      	            trds.conditionDy[i] = 1;	
      	         }   	    		     
      	       }       	  
            } else {  //* Default AND
      	      for (int i=InstrDep.maxDysBk; i<=session.endTstDateIndex; i++) {	
      	           if (((strategyX.prcSucc[i] == 1 && cmdLineNot[k] == 0) || (strategyX.prcSucc[i] == 0 && cmdLineNot[k] == 1))  
      	               && trds.conditionDy[i] == 1) {
      	        	   trds.conditionDy[i] = 1;	
      	           } else {
      	        	   trds.conditionDy[i] = 0;  
      	           }
      	      }
            }  //* if AND or OR

          }  //* for k loop of cmd's

	*/	
  }
	

}

