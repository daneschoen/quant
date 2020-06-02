package program;

class Strategy_Count extends Strategy_Abstract{

  protected int cmd_rval;    	  
	                         
  /* COUNT(C>C1, 6) = 4 and RANK
   * cf: STREAK( C<P@1300 + 5.8 ) >= 2 	
   * 
   * COUNT(C < P@1300, 6) >= 2
   *
   * COUNT(C > MAX(C1,10), 6) >= 2
   */
    
  Strategy_Count(Instr InstrX, String cmdStatement, Session session) {
	super(InstrX, cmdStatement, session);
	// TODO Auto-generated constructor stub
  }
  
  @Override
  void calcExpressionFnSides() throws Exception{	
    //* Left side - the fn	
	    //* Left side - the fn		
	Strat_Abstract stratX = new Strat_Eqn_Count(InstrX, strCmdSides[0], session);
	stratX.parseAndCalc();
	calcdExprFn[0] = stratX.calcdExprFn;      
			
	//* Right side - limit to numbers!
	cmd_rval = Integer.parseInt(strCmdSides[1]);  
	for(int i=InstrX.maxDysBk; i<InstrX.prc.length; i++)
	  calcdExprFn[1][i] = cmd_rval;
	
  }

}

