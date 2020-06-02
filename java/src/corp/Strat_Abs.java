package program;

class Strat_Abs extends Strat_Abstract{

  static final String CMD="abs";
  
  
  Strat_Abs(final Instr InstrX, final String cmdExpression, Session session) {
	super(InstrX, cmdExpression, session);
  }

  
  public void parseAndSetConditions() throws Exception{
    /*
	 * abs(c-c1)
	 * us.abs(us.c - us.c1) 
	 */	    
	getParams();
	arg_Expression = params.get(0);
  }	
  
  
  public void calc() throws Exception{
	
    nestExpressionParseAndCalc(InstrX, arg_Expression, session);
    
    for (int i=0+InstrX.maxDysBk; i<InstrX.prc.length; i++) {
        calcdExprFn[i] = Math.abs(calcdExprArg[i]);
    }
    
  }
  
}
