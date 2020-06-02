package program;


class Strategy_VolHist extends Strategy_Abstract{

  //* volhist(days, H/L/C/O/P@1100) >= 50.4
  private double cmdVolhist; 
	
  
  Strategy_VolHist(Instr InstrX, String cmdStatement, Session session) {
	super(InstrX, cmdStatement, session);
  }
  
  
  @Override
  void calcExpressionFnSides() throws Exception{	
	
	//* Left side - the fn	
	Strat_Abstract stratX = new Strat_VolHist(InstrX, strCmdSides[0], session);
	stratX.parseAndCalc();
	calcdExprFn[0] = stratX.calcdExprFn;      
		
	//* Right side - limit to numbers!
	cmdVolhist = Double.parseDouble(strCmdSides[1]);
	for(int i=InstrX.maxDysBk; i<InstrX.prc.length; i++)		
	  calcdExprFn[1][i] = cmdVolhist;
  }
  
}