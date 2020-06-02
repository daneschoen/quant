package program;

class Strat_Stdev extends Strat_Abstract{

  //* STDEV(C-C1, 10) > 20.7 
  private int arg_dys; 	  	  
  
  
  Strat_Stdev(final Instr InstrX, final String cmdExpression, Session session) {
	super(InstrX, cmdExpression, session);
  }
  
  
  @Override
  void parseAndSetConditions() throws Exception{ 
	getParams();
	arg_Expression = params.get(0);
	arg_dys = Integer.parseInt(params.get(1));  
	
	if(session.USERTYPE == 0) 
	  if (params.get(0).indexOf("(") >= 0	  )
		throw new ExceptionCmd("Error in nested syntax");
  }	

  
  @Override
  void calc() throws Exception{
   /*
    * STDEV(C-C1, 10) > 20.7 
    * STDEV(O-C1, 20) < 94.5 
    */	
    nestExpressionParseAndCalc(InstrX, arg_Expression, session);
    if (InstrX.maxDysBk < arg_dys + InstrX.maxDysBk) 
    	InstrX.maxDysBk = arg_dys + InstrX.maxDysBk;	
	      
	for (int i=InstrX.maxDysBk; i<InstrX.prc.length; i++) {		
	  /* std == sigma == sqrt(var)
	   * var == sigma^2 
	   * s = 1/(N-1)*Sum(x_i - mu)^2
	   *   = ( N*Sum(x^2) - (Sum_x)^2 ) / N(N-1)
	   */   
	  double mu_i=0.0;
	  double fdStd_i=0.0;
	  
	  for(int k=0; k<arg_dys; k++)
		mu_i += calcdExprArg[i-k];  
	  mu_i /= arg_dys;
	  
	  for(int k=0; k<arg_dys; k++)
	    fdStd_i += Math.pow(calcdExprArg[i-k] - mu_i, 2);
	  fdStd_i /= (arg_dys-1);   //* unbiased
	  fdStd_i = Math.sqrt(fdStd_i); 
	        
      calcdExprFn[i] = fdStd_i;
	}	  
  }  // calc() method		
	
}

