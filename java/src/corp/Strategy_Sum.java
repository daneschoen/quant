package program;


public class Strategy_Sum extends Strategy_Abstract{

  private double cmdfdSum;    
  /*
   *  SUM(C-C1,6)=4 : M=4 days out of N=6 	  
   *  cf: COUNT(C>C1,6)=4 and RANK
   */

  Strategy_Sum(Instr InstrX, String cmdStatement, Session session) {
	super(InstrX, cmdStatement, session);
  }
  
  @Override
  void calcExpressionFnSides() throws Exception{	
	
	//* Left side - the fn
	Strat_Abstract stratX = new Strat_Sum(InstrX, strCmdSides[0], session);  
	stratX.parseAndCalc();
	calcdExprFn[0] = stratX.calcdExprFn;  
		
	//* Right side - limit to numbers!
	cmdfdSum = Double.parseDouble(strCmdSides[1]);
	for(int i=InstrX.maxDysBk; i<InstrX.prc.length; i++)		
	  calcdExprFn[1][i] = cmdfdSum;
  }
  
}
