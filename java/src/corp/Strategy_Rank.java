package program;


public class Strategy_Rank extends Strategy_Abstract{

  private int cmd_rval;
  /*
   *  us.RANK(us.C-us.C1,6)=4 : M=4 days out of N=6
   *  cf: COUNT(C>C1,6)=4
   *  
   */

  Strategy_Rank(Instr InstrX, String cmdStatement, Session session) {
	super(InstrX, cmdStatement, session);
  }
  
  @Override
  void calcExpressionFnSides() throws Exception{	
	//* Left side - the fn	
	Strat_Abstract stratX = new Strat_Rank(InstrX, strCmdSides[0], session);
	stratX.parseAndCalc();
	calcdExprFn[0] = stratX.calcdExprFn;   
		
	//* Right side - limit to numbers!
	cmd_rval = Integer.parseInt(strCmdSides[1]);
	for(int i=InstrX.maxDysBk; i<InstrX.prc.length; i++)		
	  calcdExprFn[1][i] = cmd_rval;
  }
  
}
