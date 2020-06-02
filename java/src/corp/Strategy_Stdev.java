package program;


class Strategy_Stdev extends Strategy_Abstract{

  private double cmd_rval_stdev;	
  /* 
   * STDEV(C-C1, 10) > 20.7 
   */
  Strategy_Stdev(Instr InstrX, String cmdStatement, Session session) {
	super(InstrX, cmdStatement, session);
  }
  
  @Override
  void calcExpressionFnSides() throws Exception{	
	//Strat_Abstract stratX = Strat_Factory.getInstance(tokInstr[tk], strSides);
	//* Left side - the fn	
	Strat_Abstract stratX = new Strat_Stdev(InstrX, strCmdSides[0], session);
	stratX.parseAndCalc();
	calcdExprFn[0] = stratX.calcdExprFn;      
		
	//* Right side - limit to numbers!
	cmd_rval_stdev = Double.parseDouble(strCmdSides[1]);
	for(int i=InstrX.maxDysBk; i<InstrX.prc.length; i++)
	  calcdExprFn[1][i] = cmd_rval_stdev;
  }
  
}