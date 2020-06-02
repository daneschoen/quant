package program;


public class Strat_Eqn_Count extends Strat_Abstract{
  /*
   * count(c1>c2, 6) = 4
   * us.count(us.c1>us.c2, 6) = 4
   * 
   * COUNT(C>C1,7) >= 5
   * COUNT(O<C1 OR C1<C2,4) = 4
   * COUNT(C<P@1300,6)>=2
   * COUNT(C > MAX(C1,10), 6) >= 2 
   * 
   * us.count(us.c > us.c1, 6) = 4
   * 
   * cf: RANK(C-C1,6)=4 : M=4 days out of N=6 	  
   */ 
  static final String CMD = "count";	
  private int arg_dys;    
	  
		                    
  Strat_Eqn_Count(final Instr InstrX, final String cmdExpression, Session session) {
    super(InstrX, cmdExpression, session); 
  }
	  
	  
  @Override
  void parseAndSetConditions() throws Exception{
	getParams();
	arg_Expression = params.get(0);
	arg_dys = Integer.parseInt(params.get(1));  
		
	if(session.USERTYPE == 0) 
	  if(params.get(0).indexOf("(") >= 0)
	    throw new ExceptionCmd("Error in nested syntax");
  }

  @Override
  public void calc() throws Exception{
			
    Strategy_Compare strategy_eqn = new Strategy_Compare(InstrX, arg_Expression, session);
	strategy_eqn.parseAndSetConditions();
	strategy_eqn.calc();  
	
	if(InstrX.maxDysBk < arg_dys + InstrX.maxDysBk)
	   InstrX.maxDysBk = arg_dys + InstrX.maxDysBk;		
	
	int cntN;
	for (int i=InstrX.maxDysBk; i<InstrX.prc.length; i++) {				
	  cntN = 0;	
	  for(int n=0; n<arg_dys; n++)
	    if(strategy_eqn.prcSucc[i-n] == 1)			  
	      cntN++; 
			  
	  calcdExprFn[i] = cntN; 
	     
	}  //* for i loop  

  }  //* calc() method		

}
