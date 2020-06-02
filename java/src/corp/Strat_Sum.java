package program;

class Strat_Sum extends Strat_Abstract{

  int arg_dys;     	  	   
	                    
  Strat_Sum(final Instr InstrX, final String cmdExpression, Session session) {
	super(InstrX, cmdExpression, session);
  }
  
  
  @Override
  void parseAndSetConditions() throws Exception{
    /* SUM(c-c1,20) = 1.32
     * SUM(h,15) > 23.1
     * 
     * cf: COUNT(c>c1,6)=4 and rank
     * which take equation/predicates/sentences
     */
	getParams();
	arg_Expression = params.get(0);
	arg_dys = Integer.parseInt(params.get(1));  
	
	if(session.USERTYPE == 0) 
	  if(params.get(0).indexOf("(") >= 0)
		throw new ExceptionCmd("Error in nested syntax");
  }

  
  @Override
  void calc() throws Exception{
   /*
    * da.SUM(da.c - da.c1, 20) = 20
    * SUM(H,20) >= 7
    */	
	nestExpressionParseAndCalc(InstrX, arg_Expression, session);
	if (InstrX.maxDysBk < arg_dys + InstrX.maxDysBk) 
		InstrX.maxDysBk = arg_dys + InstrX.maxDysBk;	
	
	for (int i=InstrX.maxDysBk; i<InstrX.prc.length; i++) {		
	  double fdSum_i=0;  //* reset for each new i, this is array to be sorted	
	  //* Loop i=0 to N to calc and define array fdSum[N]
	  for(int n=0; n<arg_dys; n++)
	    fdSum_i += calcdExprArg[i-n];  
		        
	  calcdExprFn[i] = fdSum_i;
	}	  
  }  // calc() method		
	
}

	

