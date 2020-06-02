package program;

public class Strat_Pivot3 extends Strat_Pivot{

  static final String CMD="pivot2";

  Strat_Pivot3(final String cmdExpression) {
	super(cmdExpression);  
  }
  
  @Override
  public void calcZ() throws Exception{ 
	//* simply difference between zscores	
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
			double fdZscorePivot = statsUtils.fdZscore_i;
						
			for (int i = maxDysBk + 1 + Strategy.begTstDateIndex; i <= Strategy.endTstDateIndex; i++) {			
			  //* Calc the stdev of "C-C1" 
			  //* var_s = 1/(N-1)*Sum(x_i - mu)^2
			  //*       = ( N*Sum(x^2) - (Sum_x)^2 ) / N(N-1)
			  mu_i=0.0;
			  fdStd_i=0.0;
			  fdZscore_i=0.0;
			  for (int k=0; k<cmdStdPeriod; k++)
				mu_i += calcdExprArg[i-k];
			  mu_i /= cmdStdPeriod;
			  for (int k=0; k<cmdStdPeriod; k++) 
				fdStd_i += Math.pow(calcdExprArg[i-k] - mu_i,2);
		      fdStd_i /= (cmdStdPeriod-1);  //* unbiased
			  fdStd_i = Math.sqrt(fdStd_i);
					      
			  fdZscore_i = (calcdExprArg[i] - mu_i)/fdStd_i;
			  //fdZband_i = cmdfdMove*fdStd_i;
					      
			  if (fdZscore_i-fdZscorePivot >= cmdfdMove) {
			      if (cntNP < 0) cntNP = 0;
			      cntNP++;
				  fdZscorePivot = fdZscore_i;
					          
			  } else if (fdZscore_i-fdZscorePivot < -cmdfdMove) {    
				  if (cntNP > 0) cntNP = 0;
				  cntNP--;
				  fdZscorePivot = fdZscore_i;           
			  }    
			  
			  calcdExprFn[i] = cntNP;
		System.out.println(cntNP + "  " + calcdExprArg[i] + "  " + fdZscore_i);
					     		      
		    }   //* i loop
			  
		  }	
  }
