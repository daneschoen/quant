package program;


class Strategy_Pivot extends Strategy_Abstract{
  
  private int cmd_rval_pivotMove; 

  /* 
   * pivot(c, 10.5, p) = -3 
   */
  Strategy_Pivot(Instr InstrX, String cmdStatement, Session session) {
	super(InstrX, cmdStatement, session);
  }
  
  @Override
  void calcExpressionFnSides() throws Exception{	
	//Strat_Abstract stratX = Strat_Factory.getInstance(tokInstr[tk], strSides);
	//* Left side - the fn	
	Strat_Abstract stratX = new Strat_Pivot(InstrX, strCmdSides[0], session);
	stratX.parseAndCalc();
	calcdExprFn[0] = stratX.calcdExprFn;      
		
	//* Right side - limit to numbers!
	cmd_rval_pivotMove = Integer.parseInt(strCmdSides[1]);
	for(int i=InstrX.maxDysBk; i<InstrX.prc.length; i++)
	  calcdExprFn[1][i] = cmd_rval_pivotMove;
  }
  
}