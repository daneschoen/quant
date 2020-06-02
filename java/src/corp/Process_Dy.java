package program;

import java.util.ArrayList;


class Process_Dy extends Process_Abstract {
  
  Process_Dy(Session session) {
    super(session);
  }

  @Override
  Trades go_enter() throws Exception{
	session.arrCmd_feature_dy = new ArrayList<String[]>(session.arrCmdEntryDy);
    parseAndCalcStrategies();
	runPostFilters();
	return trds;
  }	  
  	  	    
  @Override
  Trades go_exit() throws Exception{
	session.arrCmd_feature_dy = new ArrayList<String[]>(session.arrCmdExitDy);  
    parseAndCalcStrategies();
	return trds;
  }	  
	    
  private void parseAndRun_RegNonlinear(String cmdStrLine) throws Exception{
    //Svm svm = new Svm();
	//svm.output();
  }    
	    
  private Strategy_Abstract parseAndRun_Strategy(Strategy_Abstract strategy_statement) throws Exception{
    //strategy.nested = 0;
    strategy_statement.parseAndSetConditions(); 
    strategy_statement.calc();
    return strategy_statement;
  }    

	     
  void parseAndCalcStrategies() throws Exception{ 	 
	/* 
	 * Process_Dy: for (int i=InstrDep.maxDysBk; i<=session.endTstDateIndex; i++) {
	 * => Strategy_Compare: InstrDep -> InstrX, cmd_line, session
	 *   => Strat_Expression(InstrX, strCmdSides[s], session)  <=>  Strat_Factory  
	 *   
	 *   
	 */
    /* 2 Fundamental types of "Commands ~ EQN's":
       Expressions and Predicate Statements
       
       - Expressions - consisting of symbols/tokens and other expressions
           c3, p@1115, 7.5, 
           c3 + 32.8
       
       - Fn - Fn Expression/Clause that takes expression as arg
           mvg(c-c1,12) 
           mvg(p@1100,7) + 8.3
           
       - Eqn - Fn Expresion/Clause that takes predicate statement as arg
           STREAK(c>c1)  
           wait(c>c1 OR r>10)
           
       - Fn that take fn's
           min(c-c1,10)
           max(VolHist(30, c), 3)
           
       - Predicate Statements - Equations ~ sentences" - Boolean-valued function P: X -> {true, false} 
         - Two sided, each being an Expression 
	       C + 50 > C4
	       C2 < MIN(C3,5)                
	       P1@1100 > MAX(C1, 10) 
	       C > MAX(P1@1100, 10)	  
	       C-C1 = MIN(C-C1, 15)    
	       ABS(C-C1) = MIN(ABS(C-C1), 15)  all these allow nesting
	   
	       wait(C > C1 OR R > 10) = 3
	       C < C1 OR RANK(C,20)=2
	       c < c5 OR c1 < c8
	   	   	   
	   - Single sided Predicate Statements 
	       dayweek(1,3)                    no nesting
	   
	  ENTRY/EXIT
	    enter(0, 1015) / exit(0, 1015)
 
        event(b > p@1015)        //* default max search this day
        event(b > p@1015 + 5)    //* prev would simply enter a few ticks after 1015 so
        event(b > p@1015, 10m/s/d) 
        event(b > p@1015, search, wait) 
	    
    */   
	  
    /* Now parse and run strategies BUT in specific order:
     * from complex nested:   WAIT(C=MAX(C, 10)) >= 20 
     * medium complex: C >= .9 *(MAX(H,10) - MIN(L,10)) , FIRST(C==MAX(C,20)), COUNT
     * to most simple: C > C1        
     */
	  
    //* MUST Reset to 0 for each whole new RUN (not cmdLine !), also max index
    //Strategy.prcSuccess = new int[InstrDep.maxPrcIndex+1];
    //Strategy.trdCondDyIndex = new ArrayList<Integer>();
	  
    //for (int k=0; k<cmdLine.length; k++) {
	int k=-1;
	for (String[] cmdLineMeta: session.arrCmd_feature_dy) {
	  k+=1;
      //* MUST reset for EACH new CMD line, NOT just run!
	  //prcSucc = new int[InstrDep.prc.length];  
	  Strategy_Abstract strategyX=null;
	
	  if (cmdLineMeta[0].indexOf("tradeday(") == 0) {
		  strategyX = parseAndRun_Strategy(new Strategy_Tradeday(InstrDep, cmdLineMeta[0], session));
	  } else if (cmdLineMeta[0].indexOf("day(") == 0) {
		  strategyX = parseAndRun_Strategy(new Strategy_Date(InstrDep, cmdLineMeta[0], session));	  
	  } else if (cmdLineMeta[0].indexOf("month(") == 0) {
		  strategyX = parseAndRun_Strategy(new Strategy_Date(InstrDep, cmdLineMeta[0], session));
	  } else if (cmdLineMeta[0].indexOf("dayweek(") == 0 && session.USERTYPE == 4) {
		  strategyX = parseAndRun_Strategy(new Strategy_Dayweek(InstrDep, cmdLineMeta[0], session));        	  
	  } else if (cmdLineMeta[0].indexOf("week(") == 0) {
		  //strategyX = parseAndRun_Strategy(new Strategy_Week(InstrDep, cmdLineMeta[0], session));        	  		  
	  } else if (cmdLineMeta[0].indexOf("hol(") == 0) {
		  strategyX = parseAndRun_Strategy(new Strategy_Econ(InstrDep, cmdLineMeta[0], session));
	  } else if (cmdLineMeta[0].indexOf("econ") == 0) {
		  strategyX = parseAndRun_Strategy(new Strategy_Econ(InstrDep, cmdLineMeta[0], session));  
	  } else if (cmdLineMeta[0].indexOf("volhilo(") == 0) {
	      // parseAndRun_VolHiLo(cmdLines[k]);
	  } else if (cmdLineMeta[0].indexOf("vix(") == 0) {
		  strategyX = parseAndRun_Strategy(new Strategy_Vix(InstrDep, cmdLineMeta[0], session));		  

	  } else if (cmdLineMeta[0].indexOf("countpure(") == 0 && session.USERTYPE == 4) {
		  //parseAndRun_Strategy(new Strategy_Countpure(), cmdLineMeta[0]);  
		  strategyX = parseAndRun_Strategy(new Strategy_Countpure(InstrDep, cmdLineMeta[0], session));
	  } else if (cmdLineMeta[0].indexOf("count(") == 0  && session.USERTYPE == 0) {
		  strategyX = parseAndRun_Strategy(new Strategy_Count(InstrDep, cmdLineMeta[0], session));  
	  
	  } else if (cmdLineMeta[0].indexOf("rank(") == 0  && session.USERTYPE == 0) {
		  strategyX = parseAndRun_Strategy(new Strategy_Rank(InstrDep, cmdLineMeta[0], session));  
	  } else if (cmdLineMeta[0].indexOf("sum(") == 0  && session.USERTYPE == 0) {
		  strategyX = parseAndRun_Strategy(new Strategy_Sum(InstrDep, cmdLineMeta[0], session));
	  } else if (cmdLineMeta[0].indexOf("stdev(") == 0 && session.USERTYPE == 0) {
		  strategyX = parseAndRun_Strategy(new Strategy_Stdev(InstrDep, cmdLineMeta[0], session));       
	  } else if (cmdLineMeta[0].indexOf("pivot(") == 0 && session.USERTYPE == 0) {
		  strategyX =  parseAndRun_Strategy(new Strategy_Pivot(InstrDep, cmdLineMeta[0], session));           
      } else if (cmdLineMeta[0].indexOf("regnonlinear1(") == 0 && session.USERTYPE == 4) {
    	  //parseAndRun_RegNonlinear(cmdLine[k]);                	  
      } else if (cmdLineMeta[0].indexOf("candle") == 0 && session.USERTYPE == 4) {
    	  //strategyX = parseAndRun_Strategy(new Strategy_Candle(InstrDep, cmdLineMeta[0], session));	 
	  
	  } else {   //* Lastly the most simple C > C1, P1@1100 > O, etc. min/max, h/l, mvg
	      strategyX = parseAndRun_Strategy(new Strategy_Compare(InstrDep, cmdLineMeta[0], session));
	  }              
	  
	  if (k==0) {  
	      for (int i=InstrDep.maxDysBk; i<=session.endTstDateIndex; i++) {
	    	 trds.conditionDy[i] = 0; 
		     if ((strategyX.prcSucc[i] == 1 && cmdLineMeta[1] == "") ||
			     (strategyX.prcSucc[i] == 0 && cmdLineMeta[1] == "not")) {
	            trds.conditionDy[i] = 1;	
	         }   	    		     
	       }
	  } else {   //* Default AND
	      for (int i=InstrDep.maxDysBk; i<=session.endTstDateIndex; i++) {	  	  
	           if ( ((strategyX.prcSucc[i] == 1 && cmdLineMeta[1] == "") || 
	        	     (strategyX.prcSucc[i] == 0 && cmdLineMeta[1] == "not"))  
	               && trds.conditionDy[i] == 1) {
	        	   trds.conditionDy[i] = 1;	
	           } else {
	        	   trds.conditionDy[i] = 0;  
	           }
	      }
      }  //* if AND or OR

    }  //* for k loop of cmd's

  }  
  
  
  //* Now all Post-Filters 
  public void runPostFilters() throws Exception {
	if (session.bl_postfilter_recprof) {
	    //Strategy_Abstract postFilter = parseAndRun_Strategy(new PostFilter_RecProf(session, trds));        
		trds = new PostFilter_RecProf(session, trds).go();
	}   	  
  }
  
}