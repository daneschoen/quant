package program;

public class Strat_Eqn_Wait extends Strat_Abstract{

  static final String CMD = "wait";
  
                    
  Strat_Eqn_Wait(final Instr InstrX, final String cmdExpression, Session session) {
	super(InstrX, cmdExpression, session);  
  }
  
  
  @Override
  void parseAndSetConditions() throws Exception{ 
	getParams();
	arg_Expression = params.get(0);
  }	
	
  
  @Override
  public void calc() throws Exception{
    /*
	 * WAIT(C>C1) > 3
	 * WAIT(C = MAX(C,20))  >= 20
	 * WAIT(C1+50>C2) >= 7
	 * WAIT(C2>C6) = 4
	 * 
	 * WAIT(OR(C>C1; C1>C2)) > 3 
	 * 
	 * cf:
	 * STREAK(C < C1) > 3
	 * STREAK(C < C1) <= 3
	 * 
	 * COUNT(C1>C2,6) = 4
	 * COUNT(O<C1,4) = 4
	 * 
	 */   
    
	Strategy_Compare strategy_compare = new Strategy_Compare(InstrX, arg_Expression, session);  
	strategy_compare.parseAndSetConditions();  //* eg c = min(c,21) <== streak(c = min(c,21)) = 3	
	strategy_compare.calc();  	
			
    for (int i=InstrX.maxDysBk; i<InstrX.prc.length; i++) {
	  //* Only testing consec so STOP anytime a TRUE sig occurs	
      //* Note: this is opposite of streak !	
	  
	  int cntM = 0;
	  while (i-cntM >= InstrX.maxDysBk) {
	    if(strategy_compare.prcSucc[i-cntM] != 1)			  
		  cntM++;
		else 
		  break;		  
	  }
	  
	  calcdExprFn[i] = cntM; 	  
    }
        
  }   //* method calcFn    
  
}

