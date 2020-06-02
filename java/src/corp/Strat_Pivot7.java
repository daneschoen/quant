package program;


class Strat_Pivot7 extends Strat_Abstract{
	
  static final String CMD="pivot7";
	  
  protected double cmdfdMove;
  protected double cmdfdNP;
  protected String cmdMoveType;
  protected int cmdStdPeriod=60;
  
  
  Strat_Pivot7(final String cmdExpression) {
	super(cmdExpression);  
  }
  
  
  @Override
  public void parseAndSetConditions() throws Exception{
    /*
	 * pivot7(c/o1/p@1000, -15.6, z/p, 60) >= 3
	 * pivot7(c/o/p@1000/60min/10min/5min, -15.6, p/z) >= 3
	 */	
    getParams();
	argExpression = params.get(0);
	cmdfdMove = Double.valueOf(params.get(1));
	cmdMoveType = params.get(2);
	if(cmdMoveType.equals("z"))	
	  cmdStdPeriod = Integer.parseInt(params.get(3));
	cmdfdNP = Double.valueOf(params.get(params.size()-1));
  }	
	
  
  @Override
  public void calc() throws Exception{ 
	nestExpressionParseAndCalc(this.argExpression);		
    
	if(cmdMoveType.equals("z"))
      calcZ();
    else if (cmdMoveType.equals("p"))
      calcPts();
  }  
	
  
  public void calcPts() throws Exception{
	int maxFnDysBk = maxDysBk + 1; 
	if (maxFnDysBk > maxDysBk) maxDysBk = maxFnDysBk;	
		
    int cntNP=0;
    double fdPivot = calcdExprArg[Strategy.begTstDateIndex+maxDysBk-1];
    
	for (int i=Strategy.begTstDateIndex+maxDysBk; i<=Strategy.endTstDateIndex; i++) {	
        if (calcdExprArg[i]-fdPivot >= cmdfdMove) {
    	     
    	    cntNP += (int)((calcdExprArg[i]-fdPivot)/cmdfdMove);
            fdPivot = calcdExprArg[i];  
        /*    
        } else if (calcdExprArg[i]-fdPivot <= -cmdfdMove) {
    	    if (cntNP > 0) cntNP = 0;   //* reset
    	    cntNP += (int)((calcdExprArg[i]-fdPivot)/cmdfdMove);
            fdPivot = calcdExprArg[i];
        */                
        }    
        
	    calcdExprFn[i] = cntNP;
System.out.println(cntNP + "  " + calcdExprFn[i]);
	    if (cntNP >= cmdfdNP) cntNP = 0;   //* reset
	    
	}  //* i loop
  }
    

  public void calcZ() throws Exception{  	
	int maxFnDysBk = cmdStdPeriod + maxDysBk + 1; 
	if (maxFnDysBk > maxDysBk) maxDysBk = maxFnDysBk;	
		
	//* calculates z-score move using current price but OLD pivot mu and std!	
	double mu_i;
	double fdStd_i;
	double fdZscore_i;
	int cntNP=0;
	double fdPivot = calcdExprArg[Strategy.begTstDateIndex+maxDysBk-1];
	
	for (int i=maxDysBk + Strategy.begTstDateIndex; i<=Strategy.endTstDateIndex; i++) {			
	  	  
	  //* Calc the stdev of "C-C1" 
      //* var_s = 1/(N-1)*Sum(x_i - mu)^2
	  //*       = ( N*Sum(x^2) - (Sum_x)^2 ) / N(N-1)
	  mu_i=0.0;
	  fdStd_i=0.0;
	  fdZscore_i=0.0;
	  /*
	  for(int k=0; k<cmdStdPeriod; k++)
		mu_i += calcdExpr[i-k];
	  mu_i /= cmdStdPeriod;
	  for(int k=0; k<cmdStdPeriod; k++)
	    fdStd_i += Math.pow(calcdExpr[i-k] - mu_i,2);
	  fdStd_i /= (cmdStdPeriod-1);  //* unbiased
      fdStd_i = Math.sqrt(fdStd_i);
      */
	  for(int k=0; k<cmdStdPeriod; k++)
	    mu_i += calcdExprArg[i-k] - calcdExprArg[i-k-1];
	  mu_i /= cmdStdPeriod;
	  for(int k=0; k<cmdStdPeriod; k++)
	    fdStd_i += Math.pow((calcdExprArg[i-k]-calcdExprArg[i-k-1]) - mu_i,2);
	  fdStd_i /= (cmdStdPeriod-1);  //* unbiased
	  fdStd_i = Math.sqrt(fdStd_i);
	  
      fdZscore_i = (calcdExprArg[i] - fdPivot)/fdStd_i;  
      //double diff = (calcdExpr[i] - fdPivot);
      if (fdZscore_i >= cmdfdMove) {
    	  if (cntNP < 0) cntNP = 0;
    	  cntNP += (int)((fdZscore_i)/cmdfdMove);
          fdPivot = calcdExprArg[i];
          
      } else if (fdZscore_i <= -cmdfdMove) {    
    	  if (cntNP > 0) cntNP = 0;
    	  cntNP += (int)((fdZscore_i)/cmdfdMove);
          fdPivot = calcdExprArg[i];
      }    

      calcdExprFn[i] = cntNP;
//System.out.println(cntNP + "  " + calcdExpr[i] + "  " + diff + "  " + fdStd_i + "  " + fdZscore_i);      
    }   //* i loop
  }
  
}

