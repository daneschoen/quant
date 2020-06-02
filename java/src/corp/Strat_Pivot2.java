package program;

class Strat_Pivot2 extends Strat_Pivot{

  static final String CMD="pivot2";

  
  Strat_Pivot2(final String cmdExpression) {
	super(cmdExpression);  
  }
  
  @Override
  public void calcZ() throws Exception{  	
    //* calculates z-score move using current std & mu !	
		int maxFnDysBk = cmdStdPeriod + maxDysBk + 1; 
		if (maxFnDysBk > maxDysBk) maxDysBk = maxFnDysBk;	
				
		double mu_i;
		double fdStd_i;
		double fdZscore_i;
		int cntNP=0;
		double fdPivot = calcdExprArg[Strategy.begTstDateIndex+maxDysBk-1];
				
    for (int i = maxDysBk + Strategy.begTstDateIndex; i <= Strategy.endTstDateIndex; i++) {			
				  	  
			  /*  
			   * var_s = 1/(N-1)*Sum(x_i - mu)^2
			   *       = ( N*Sum(x^2) - (Sum_x)^2 ) / N(N-1)
			   */       
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
			  
	  fdZscore_i = (calcdExprArg[i] - fdPivot)/fdStd_i;    
				      
	  if (fdZscore_i >= cmdfdMove) {
	      if (cntNP < 0) cntNP = 0;
	      cntNP++;
          fdPivot = calcdExprArg[i];
	  } else if (fdZscore_i < -cmdfdMove) {    
	       if (cntNP > 0) cntNP = 0;
	  	   cntNP--;     
		   fdPivot = calcdExprArg[i];
	  }    
			
	  calcdExprFn[i] = cntNP;
	  System.out.println(cntNP + "  " + calcdExprArg[i] + "  " + fdZscore_i);
	  
	}   //* i loop
     
  }
	  
	  
	  public void calcZnewstd() throws Exception{  	
	    //* calculates z-score move using current price +/- pivot price!	
			int maxFnDysBk = cmdStdPeriod + maxDysBk + 1; 
			if (maxFnDysBk > maxDysBk) maxDysBk = maxFnDysBk;	
					
			double mu_i;
			double fdStd_i;
			double fdZscore_i;
			int cntNP=0;
			double fdPivot = calcdExprArg[Strategy.begTstDateIndex+maxDysBk-1];
		int cntTemp=0;
			
		double fdPivotMove=0;
			
		for (int i = maxDysBk + Strategy.begTstDateIndex; i <= Strategy.endTstDateIndex; i++) {			
			  	  
		  /*  
		   * var_s = 1/(N-1)*Sum(x_i - mu_i)^2
		   *       = ( N*Sum(x^2) - (Sum_x)^2 ) / N(N-1)
		   */       
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
		      
		  if (fdPivot >= mu_i) { 
		    fdPivotMove = calcdExprArg[i] - (mu_i - fdPivot);   // = mu_i + (calcdExprArg[i] + fdPivot)
		    if (fdPivot > calcdExprArg[i]) {
		    	cntTemp++;
		    }
		    
		  } else if (fdPivot < mu_i)  {                      
		    fdPivotMove = calcdExprArg[i] + (mu_i - fdPivot);   // = mu_i + (calcdExprArg[i] - fdPivot) 
		    if (fdPivot > calcdExprArg[i]) {
		    	cntTemp++;
		    }
		  }
		  
		  fdZscore_i = (fdPivotMove - mu_i)/fdStd_i;    
		      
		  if (fdZscore_i >= cmdfdMove) {
		  //if (fdZscore_i >= cmdfdMove) {
		      if (cntNP < 0) cntNP = 0;
		      cntNP++;
		      fdPivot = calcdExprArg[i];
		          
	      } else if (fdZscore_i < -cmdfdMove) {    
		      if (cntNP > 0) cntNP = 0;
		      cntNP--;     
		      fdPivot = calcdExprArg[i];
		  }    
		
		  calcdExprFn[i] = cntNP;
	System.out.println(cntNP + "  " + calcdExprArg[i] + "  " + fdZscore_i);     
	    }   //* i loop
	System.out.println(cntTemp);    
	  
  }
}
