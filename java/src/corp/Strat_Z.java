package program;

public class Strat_Z extends Strat_Abstract{

  static final String CMD = "z";
  /* cf STDEV(C-C1, 10) > 20.7
   *    ZSCORE(C-C1, 10) > 2
   *    T > c1 + 1.5z(c1-c2, 40)
   *    T > b1 + 1.5z(b1-b2, 40)       	
   */
  
  int cmdN; 	
  double cmdZ;

                 
  Strat_Z(final String cmdExpression) {
	super(cmdExpression);  
  }
  
  
  @Override
  void parseAndSetConditions() throws Exception{ 
	cmdZ = Double.parseDouble(cmdExpression.substring(0,cmdExpression.indexOf("z")).trim());  
	getParams();
	argExpression = params.get(0);
	cmdN = Integer.parseInt(params.get(1));  
  }	
	
  
  @Override	
  public void calc() throws Exception{
    /*
     *    T > c + "1.5z(c-c1, 40)"     =>  1.5*std_i + mu_i  
     *    T > "1.5zs(c-c1, 40)"        =>  1.5*std_i + mu_i + c
     *    T > b + "1.5z(b-b2:00, 40)"
     *    T > "1.5zs(b-b2:00, 40)"     =>  1.5std_b + mu_b + b
	 */  
    nestExpressionParseAndCalc(argExpression);
    int maxFnDysBk = cmdN + maxDysBk - 1;
    if (maxFnDysBk > maxDysBk) maxDysBk = maxFnDysBk;	
	
	for (int i = Strategy.begTstDateIndex + maxDysBk; i<=Strategy.endTstDateIndex; i++) {			
	  calcdExprFn[i] = calc(i);
	}
	  
  }  //* calc method
  
  /* IF RUNNING DIRECTLY FOR i THEN 
   * MUST RUN nestExpressionParseAndCalc(argExpression) BEFORE ONCE AND ONLY ONCE
   */
  public double calc(int i) throws Exception{
	/* var = E[(X-mu)^2]  	  
	 * var_s = 1/(N-1)*Sum(x_i - mu)^2
	 *       = ( N*Sum(x^2) - (Sum_x)^2 ) / N(N-1)
	 */ 	  
    double mu_i=0.0;
    double fdStd_i=0.0;
    //double fdZscore_i;
    double fdZband_i=0.0;
	for(int k=0; k<cmdN; k++)
	  mu_i += calcdExprArg[i-k];
	mu_i /= cmdN;
	for(int k=0; k<cmdN; k++)
	  fdStd_i += Math.pow(calcdExprArg[i-k] - mu_i, 2);
	fdStd_i /= (cmdN-1);  //* unbiased
	fdStd_i = Math.sqrt(fdStd_i);
	      
	fdZband_i = cmdZ*fdStd_i + mu_i;
	//fdZscore_i = (calcdExprArg[i] - mu_i)/fdStd_i;   
	return fdZband_i;
  }
  
  
  public double calcB(int i, int j) throws Exception{
    double mu_b=0.0;
	double fdStd_b=0.0;
	//double fdZscore_b;
	double fdZband_b=0.0;
    for(int k=0; k<cmdN; k++)
mu_b += calcdExprArg[i-k];  //* b-b2:00
	mu_b /= cmdN;
	for(int k=0; k<cmdN; k++)
fdStd_b += Math.pow(calcdExprArg[i-k] - mu_b, 2);
	fdStd_b /= (cmdN-1);  //* unbiased
	fdStd_b = Math.sqrt(fdStd_b);
		      
	fdZband_b = cmdZ*fdStd_b + mu_b; 
	//D System.out.println(i + "  " + calcdExpr[i] + "  " + calcdExprFn[i]);
	return fdZband_b;	  
  }
  
}
