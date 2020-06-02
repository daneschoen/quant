package program;


class Strat_Pivot extends Strat_Abstract{
	
  static final String CMD="pivot";
	  
  protected double arg_fdMove;
  protected String arg_MoveType;
  protected int arg_StdPeriod=60;
  
  
  Strat_Pivot(final Instr InstrX, final String cmdExpression, Session session) {
	super(InstrX, cmdExpression, session); 
  }
  
  
  @Override
  public void parseAndSetConditions() throws Exception{
    /*
	 * pivot(c/o1/p@1000, -15.6, z/p, 60) >= 3
	 * pivot(c/o/p@1000/60min/10min/5min, -15.6, p/z) >= 3
	 */	
    getParams();
	arg_Expression = params.get(0);
	arg_fdMove = Double.valueOf(params.get(1));
	arg_MoveType = params.get(2);
	if(params.size() > 3)	
	  arg_StdPeriod = Integer.parseInt(params.get(3));
	
	if(session.USERTYPE == 0) 
	  if(params.get(0).indexOf("-") >= 0 || params.get(0).indexOf("+") >= 0 || params.get(0).indexOf("*") >= 0 || params.get(0).indexOf("/") >= 0
	    || params.get(0).indexOf("(") >= 0	  )
		  throw new ExceptionCmd("Error in nested syntax");	
	
  }	
	
  
  @Override
  public void calc() throws Exception{ 
	nestExpressionParseAndCalc(InstrX, arg_Expression, session);			
    
	if(arg_MoveType.equals("z"))
      calcZ();
    else if (arg_MoveType.equals("p"))
      calcPts();
  }  
	
  
  public void calcPts() throws Exception{		 
	if(InstrX.maxDysBk < InstrX.maxDysBk + 1) 
	   InstrX.maxDysBk = InstrX.maxDysBk + 1;	
		
    int cntNP=0;
    double fdPivot = calcdExprArg[0+InstrX.maxDysBk-1];
    
    for (int i=InstrX.maxDysBk; i<InstrX.prc.length; i++) {		
      if (calcdExprArg[i]-fdPivot >= arg_fdMove) {
    	  if (cntNP < 0) cntNP = 0;   //* reset 
    	  cntNP += (int)((calcdExprArg[i]-fdPivot)/arg_fdMove);
          fdPivot = calcdExprArg[i];  
      } else if (calcdExprArg[i]-fdPivot <= -arg_fdMove) {
    	  if (cntNP > 0) cntNP = 0;   //* reset
    	  cntNP += (int)((calcdExprArg[i]-fdPivot)/arg_fdMove);
          fdPivot = calcdExprArg[i];            
      }    
	  calcdExprFn[i] = cntNP;
	}  //* i loop
  }
    

  public void calcZ() throws Exception{  	
	if(InstrX.maxDysBk < 1 + arg_StdPeriod + InstrX.maxDysBk) 
	  InstrX.maxDysBk = 1 + arg_StdPeriod + InstrX.maxDysBk;	
		
	//* calculates z-score move using current price but OLD pivot mu and std!	
	double mu_i;
	double fdStd_i;
	double fdZscore_i;
	int cntNP=0;
	double fdPivot = calcdExprArg[0+InstrX.maxDysBk-1];
	
	for (int i=InstrX.maxDysBk; i<InstrX.prc.length; i++) {			
	  	  	  
	  //* Calc the stdev of "C-C1" 
      //* var_s = 1/(N-1)*Sum(x_i - mu)^2
	  //*       = ( N*Sum(x^2) - (Sum_x)^2 ) / N(N-1)
	  mu_i=0.0;
	  fdStd_i=0.0;
	  fdZscore_i=0.0;
	  /*
	  for(int k=0; k<arg_StdPeriod; k++)
		mu_i += calcdExpr[i-k];
	  mu_i /= arg_StdPeriod;
	  for(int k=0; k<arg_StdPeriod; k++)
	    fdStd_i += Math.pow(calcdExpr[i-k] - mu_i,2);
	  fdStd_i /= (arg_StdPeriod-1);  //* unbiased
      fdStd_i = Math.sqrt(fdStd_i);
      */
	  for(int k=0; k<arg_StdPeriod; k++)
	    mu_i += calcdExprArg[i-k] - calcdExprArg[i-k-1];
	  mu_i /= arg_StdPeriod;
	  for(int k=0; k<arg_StdPeriod; k++)
	    fdStd_i += Math.pow((calcdExprArg[i-k]-calcdExprArg[i-k-1]) - mu_i,2);
	  fdStd_i /= (arg_StdPeriod-1);  //* unbiased
	  fdStd_i = Math.sqrt(fdStd_i);
	  
      fdZscore_i = (calcdExprArg[i] - fdPivot)/fdStd_i;  
      //double diff = (calcdExpr[i] - fdPivot);
      if (fdZscore_i >= arg_fdMove) {
    	  if (cntNP < 0) cntNP = 0;
    	  cntNP += (int)((fdZscore_i)/arg_fdMove);
          fdPivot = calcdExprArg[i];
          
      } else if (fdZscore_i <= -arg_fdMove) {    
    	  if (cntNP > 0) cntNP = 0;
    	  cntNP += (int)((fdZscore_i)/arg_fdMove);
          fdPivot = calcdExprArg[i];
      }    

      calcdExprFn[i] = cntNP;
      //D System.out.println(cntNP + "  " + calcdExpr[i] + "  " + diff + "  " + fdStd_i + "  " + fdZscore_i);      
    }   //* i loop
  }
  
}
