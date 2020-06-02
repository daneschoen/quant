package program;

public class Strat_Zscore extends Strat_Abstract{

  static final String CMD = "zscore";
  /* cf: STDEV(C-C1, 10) > 20.7
   * ZSCORE(C-C1, 10) > 2 
   * ZSCORE(O-C1, 20) < -1.5 
   * ZSCORE(p@0930-p@0900,40d) < -3.2
   * ZSCORE(p@0930-p@0900,60m) < -3.2
   * ZSCORE(b-b3,40m,0600->0930) > 2.5
   *
   * zscore_i(b-b3,40m,i) > 2.5 	
   */
  
  int arg_dys; 	  	  
  int arg_min;

  
  Strat_Zscore(final Instr InstrX, final String cmdExpression, Session session) {
    super(InstrX, cmdExpression, session);  
  }
  
  
  @Override
  void parseAndSetConditions() throws Exception{ 
	getParams();
	arg_Expression = params.get(0);  
	
	if (session.USERTYPE == 4) {
		
		if (params.get(1).indexOf("m") == params.get(1).length()-1) {
		    arg_min = Integer.parseInt(params.get(1).substring(0, params.get(1).length()-1));
		    ////blIntrady = true;
		} else {
			arg_dys = Integer.parseInt(params.get(1));
		}
		
	} else {
		arg_dys = Integer.parseInt(params.get(1));
	    if (params.get(0).indexOf("(") >= 0) {
	        if (params.get(0).indexOf("h(") >= 0  ||
		        params.get(0).indexOf("l(") >= 0) {
	    	    //* pass
	        } else {   		
	            throw new ExceptionCmd("Error in nested syntax - zscore");
	        }
	    }    		
	}	  
	    
  }	
	
  
  @Override	
  public void calc() throws Exception{
    /*	  
	 * ZSCORE(C-C1, 10) > 2 
	 * ZSCORE(O-C1, 20) < -1.5 
	 * ZSCORE(p@0930-p@0900,40d) < -3.2
	 * ZSCORE(p@0930-p@0900,60m) < -3.2
	 *	   
	 * zscore(b-b3,40m) > 2.5 	
	 */  
    nestExpressionParseAndCalc(InstrX, arg_Expression, session);
    if(InstrX.maxDysBk < arg_dys + InstrX.maxDysBk) 
       InstrX.maxDysBk = arg_dys + InstrX.maxDysBk;	

    double mu_i;
	//double fdZband_i=0.0;
	double fdStd_i;
	double fdZscore_i;
	for (int i=InstrX.maxDysBk; i<InstrX.prc.length; i++) {			
	  /* var = E[(X-mu)^2]  	  
	   * var_s = 1/(N-1)*Sum(x_i - mu)^2
	   *       = ( N*Sum(x^2) - (Sum_x)^2 ) / N(N-1)
	   */       
	  mu_i=0.0;
	  fdStd_i=0.0;
	  for(int k=0; k<arg_dys; k++)
		mu_i += calcdExprArg[i-k];
	  mu_i /= arg_dys;
	  for(int k=0; k<arg_dys; k++)
	    fdStd_i += Math.pow(calcdExprArg[i-k] - mu_i, 2);
	  fdStd_i /= (arg_dys-1);  //* unbiased
	  fdStd_i = Math.sqrt(fdStd_i);
	      
	  //fdZband_i = cmdZscore*fdStd_i + mu;
	  fdZscore_i = (calcdExprArg[i] - mu_i)/fdStd_i;   
	  calcdExprFn[i] = fdZscore_i;
      //D System.out.println(i + "  " + calcdExpr[i] + "  " + calcdExprFn[i]);   
	}  //* i loop
	  
  }  //* calc method
  
  /*
  @Override	
  public void calc_intrady(int iDy) throws Exception{
    nestExpressionParseAndCalc(argExpression);
    int maxFnDysBk = cmdNDays + maxDysBk - 1;
    if (maxFnDysBk > maxDysBk) maxDysBk = maxFnDysBk;	

    double mu_i;
	//double fdZband_i=0.0;
	double fdStd_i;
	double fdZscore_i;
	for (int i = Strategy.begTstDateIndex + maxDysBk; i<=Strategy.endTstDateIndex; i++) {			
	  mu_i=0.0;
	  fdStd_i=0.0;
	  for(int k=0; k<cmdNDays; k++)
		mu_i += calcdExprArg[i-k];
	  mu_i /= cmdNDays;
	  for(int k=0; k<cmdNDays; k++)
	    fdStd_i += Math.pow(calcdExprArg[i-k] - mu_i, 2);
	  fdStd_i /= (cmdNDays-1);  //* unbiased
	  fdStd_i = Math.sqrt(fdStd_i);
	      
	  //fdZband_i = cmdZscore*fdStd_i + mu;
	  fdZscore_i = (calcdExprArg[i] - mu_i)/fdStd_i;   
	  calcdExprFn[i] = fdZscore_i;
      //D System.out.println(i + "  " + calcdExpr[i] + "  " + calcdExprFn[i]);   
	}  
	
  } 
  */
  
}
