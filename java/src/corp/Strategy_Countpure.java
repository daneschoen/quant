package program;


public class Strategy_Countpure  extends Strategy_Abstract{

  public int nested;  //*RIGHT NOW NO NESTING FOR NESTER FN'S!
		
  public int[] prcSucc;   //* each index represents a signal
  public int cntSucc;	
  public String cmdStrNest;
  public int cmdEql;      //* NOTE: This is the 2nd set of eql's! NOT inside ()!
  public int cmdMDys;     //* M=4 days out of N=6 	  
  public int cmdOfNDays;  //* COUNT(C>C1,6)=4
                          //* COUNT(C>C1,7)>=5 
  public int maxDysBk;
	  
  /* 
   *  
   */
  Strategy_Countpure(Instr InstrX, String cmdStatement, Session session) {
	super(InstrX, cmdStatement, session);
  }
	  
  public void parseAndSetConditions(String strCmdLine) throws Exception{
	    
	/*
	 * COUNT(C1>C2,6) = 4
	 * COUNT(O<C1,4) = 4
	 * COUNT(O<C1 OR C1<C2,4) = 4
	 * COUNT(C<P@1300,6)>=2
	 * 
	 * Extract parameters for COUNT(C<P@1300,6)>=2
	 * 1) Set cmdStrNest
	 * 2) Set cmdEql: >,>=,<,<=
	 * 3) Set cmdOfNDays, cmdMDys
	 */ 
	
    //* Here we go 
	strCmdLine = strCmdLine.trim();
	strCmdLine = strCmdLine.toLowerCase();

	//* 1) Set cmdStrNest:  COUNT(C<P@1300,6)>=2
	int y_P0 = strCmdLine.indexOf("(");  	  
	int y_C = strCmdLine.lastIndexOf(",");
	cmdStrNest = strCmdLine.substring(y_P0+1,y_C);
	strCmdLine = strCmdLine.substring(y_C+1);
	strCmdLine = strCmdLine.trim();
    //D System.out.println(cmdStrNest);
    //D System.out.println(strCmdLine);
	  
	//* 2) >,>=,<,<=
	int y_gtls = -1;
	int y_ = -1;
	if (strCmdLine.lastIndexOf(">=") >= 0) {
	  y_gtls = strCmdLine.lastIndexOf(">=");  
	  y_ = 2;	  
	  cmdEql = 1;
	} else if (strCmdLine.lastIndexOf(">") >= 0) {
	  y_gtls = strCmdLine.lastIndexOf(">");
	  y_ = 1;	  
	  cmdEql = 0;
	} else if (strCmdLine.lastIndexOf("<=") >= 0) {
	  y_gtls = strCmdLine.lastIndexOf("<=");
	  y_ = 2;	  
	  cmdEql = 3;
	} else if (strCmdLine.lastIndexOf("<") >= 0) {
	  y_gtls = strCmdLine.lastIndexOf("<");
	  y_ = 1;	  
	  cmdEql = 2;
	} else if (strCmdLine.lastIndexOf("=") >= 0) {
	  y_gtls = strCmdLine.lastIndexOf("=");
	  y_ = 1;	  
	  cmdEql = 4;		
	}
	  
	//* 3) Set cmdOfNDays, cmdMDys
	//* COUNT(C<P@1300,6)>=2  =>  "6)>=2"
	int y_P1 = strCmdLine.indexOf(")");  	  
	cmdOfNDays = Integer.parseInt(strCmdLine.substring(0, y_P1));

	strCmdLine = strCmdLine.substring(y_gtls+y_);
    strCmdLine = strCmdLine.trim();
  	cmdMDys = Integer.parseInt(strCmdLine);
	  
  }	

  public void calc() throws Exception{
	/*
	 * COUNT(C1>C2,6) = 4
	 * COUNT(O<C1,4) = 4
	 * COUNT(C<P@1300,6)>=2
	 * COUNT(C > MAX(C1,10),6)>=2
	 *
	 * 1) Run Strategy_Compare.parseAndSetConditions() AND .calc()
	 * 2) Determine max days back
	 * 3) i loop thru to see if 4 of 6 are true or not
     */	
	
	//* 1) Run Strategy_Compare.parseAndSetConditions() AND .calc()
	Strategy_Compare stratCompare = new Strategy_Compare();
	stratCompare.nested = 1;
	stratCompare.parseAndSetConditions(cmdStrNest); 
	stratCompare.calc();
		
	//* 2) Determine max days back
	maxDysBk = stratCompare.maxDysBk + cmdOfNDays-1;
	
	//* 3) Finally this is the real calc:
	//*    i loop thru to see if 4 of 6 are true or not
	Instr InstrDep = Instr.getInstance(Strategy.iDependentInstr);  
	prcSucc = new int[InstrDep.maxPrcIndex+1];
	int cntM;
	boolean blSignal;		
	boolean blPure = true;
	for (int i=maxDysBk+Strategy.begTstDateIndex; i<=Strategy.endTstDateIndex;i++) {		
	  cntM = 0;	
	  for (int n=0; n<cmdOfNDays; n++) {	
        if ( stratCompare.prcSucc[i-n] == 1 ) {			  
            cntM++;     	
        } 
	  }
	  
	  blSignal = false;
	  switch (cmdEql) {   // > or < etc...
		case 0:  // >
		  if (cntM > cmdMDys) {
			  if (blPure) {
				  blSignal = true;
				  blPure = false;
			  }
		  } else { blSignal = false; blPure = true;}
	      break;
	      
		case 1:  // >=
		  if (cntM >= cmdMDys) {
			  if (blPure) {
				  blSignal = true;
				  blPure = false;
			  }
		  } else { blSignal = false; blPure = true;}
		  break;
		
		case 2:  // <
		  if (cntM < cmdMDys) {
			  if (blPure) {
				  blSignal = true;
				  blPure = false;
			  }
		  } else { blSignal = false; blPure = true;}
		  break;
		
		case 3:  // <=
		  if (cntM <= cmdMDys) {
			  if (blPure) {
				  blSignal = true;
				  blPure = false;
			  }
		  } else { blSignal = false; blPure = true;}
		  break;
		
		case 4:  // =
		  if (cntM == cmdMDys) {
			  if (blPure) {
				  blSignal = true;
				  blPure = false;
			  }
		  } else { blSignal = false; blPure = true;}
		  break;
	  }   		  	  	  
	        	  
      if (nested == 0) {
	      if (blSignal) {   
	          ParserCondition.prcSucc[i] = 1;
	      } else {
	 	      ParserCondition.prcSucc[i] = 0;
	      }			
	  } else if (nested == 1) {
		  if (blSignal) {   
		      prcSucc[i] = 1;
		  } else {
		      prcSucc[i] = 0;
	      }							
	  }
     
	}  //* for i loop  
  
  }  //* calc() method		
}

