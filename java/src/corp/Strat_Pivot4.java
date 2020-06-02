package program;


public class Strat_Pivot4 extends Strat_Pivot{
	
  public static final String CMD="pivot";
	  
  double cmdfdMove;
  String cmdMoveType;
  String cmdInterval;
  int cmdNbrMoves;
  int cmdStdPeriod=60;
  
  
  Strat_Pivot4(final String cmdExpression) {
	super(cmdExpression);  
  }
  
  @Override  
  public void calcPts() throws Exception{
		int maxFnDysBk = maxDysBk + 1; 
		if (maxFnDysBk > maxDysBk) maxDysBk = maxFnDysBk;	
			
	    int cntNP=0;
	    double fdPivot = calcdExprArg[Strategy.begTstDateIndex+maxDysBk-1];	  
	    
	for (int i=maxDysBk + Strategy.begTstDateIndex; i<=Strategy.endTstDateIndex; i++) {	
      if (calcdExprArg[i]-fdPivot >= cmdfdMove) {
    	  if (cntNP < 0) cntNP = 0;   //* reset 
    	  cntNP++;
          fdPivot = calcdExprArg[i];  
      } else if (calcdExprArg[i]-fdPivot <= -cmdfdMove) {
    	  if (cntNP > 0) cntNP = 0;   //* reset
    	  cntNP--;
          fdPivot = calcdExprArg[i];            
      }    
	  calcdExprFn[i] = cntNP;
 
	}  //* i loop
  }
    
  @Override	  
  public void calcZ() throws Exception{  	
	//* calculates z-score move using current price but OLD pivot mu and std!	
		int maxFnDysBk = cmdStdPeriod + maxDysBk + 1; 
		if (maxFnDysBk > maxDysBk) maxDysBk = maxFnDysBk;	
				
		double mu_i;
		double fdStd_i;
		double fdZscore_i;
		int cntNP=0;
		double fdPivot = calcdExprArg[Strategy.begTstDateIndex+maxDysBk-1];

	
	StatsUtils statsUtils = new StatsUtils();
    double[] initRegressor = new double[cmdStdPeriod];
    for (int k=0; k<cmdStdPeriod; k++)
	  initRegressor[k] = calcdExprArg[maxDysBk - k + Strategy.begTstDateIndex];
    statsUtils.stdev(initRegressor);
	double fdMuPivot = statsUtils.mu;
	double fdStdPivot = statsUtils.fdStd_i;
	double fdPivotMove=0;
	
	for (int i=maxDysBk + Strategy.begTstDateIndex; i<=Strategy.endTstDateIndex; i++) {			
	  	  
	  //* Calc the stdev of "C-C1" 
      //* var_s = 1/(N-1)*Sum(x_i - mu)^2
	  //*       = ( N*Sum(x^2) - (Sum_x)^2 ) / N(N-1)
	  mu_i=0.0;
	  fdStd_i=0.0;
	  fdZscore_i=0.0;
	  for(int k=0; k<cmdStdPeriod; k++)
		mu_i += calcdExprArg[i-k];
	  mu_i /= cmdStdPeriod;
	  for(int k=0; k<cmdStdPeriod; k++)
	    fdStd_i += Math.pow(calcdExprArg[i-k] - mu_i,2);
	  fdStd_i /= (cmdStdPeriod-1);  //* unbiased
      fdStd_i = Math.sqrt(fdStd_i);
   
	  if (calcdExprArg[i] >= fdMuPivot) { 
		  fdPivotMove = fdMuPivot + (calcdExprArg[i] - fdPivot);
	  } else { 
		  fdPivotMove = fdMuPivot + (calcdExprArg[i] - fdPivot);
	  }
      
      fdZscore_i = (fdPivotMove - fdMuPivot)/fdStdPivot;  
      
      //if (calcdExprArg[i] >= cmdfdMove*fdPivotStd+fdPivotMu) {
      if (fdZscore_i >= cmdfdMove) {
    	  if (cntNP < 0) cntNP = 0;
          cntNP++;
          fdMuPivot = mu_i;
          fdStdPivot = fdStd_i;
          fdPivot = calcdExprArg[i];
          
      } else if (fdZscore_i < -cmdfdMove) {    
    	  if (cntNP > 0) cntNP = 0;
    	  cntNP--;
          fdMuPivot = mu_i;
          fdStdPivot = fdStd_i; 
          fdPivot = calcdExprArg[i];
      }    

      calcdExprFn[i] = cntNP;
 //System.out.println(cntNP + "  " + calcdExprArg[i] + "  " + fdZscore_i);      
    }   //* i loop
  }
  
}
