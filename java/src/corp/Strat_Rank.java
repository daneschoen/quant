package program;

import java.util.Arrays;

class Strat_Rank extends Strat_Abstract{

  int arg_dys;    
  /* 
   * us.RANK(us.c-us.c1, 6) = 4 : M=4 days out of N=6 	
   * 
   * cf: COUNT(c > c1, 6)=4
   */
                   
	                    
  
  Strat_Rank(final Instr InstrX, final String cmdExpression, Session session) {
    super(InstrX, cmdExpression, session);  
  }
  
  
  @Override
  void parseAndSetConditions() throws Exception{
    //* RANK(C-C1,20) = 1,2,...,20    
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
    * RANK(C-C1,20) = 20
    * RANK(H,20) >= 7
    */	
	nestExpressionParseAndCalc(InstrX, arg_Expression, session);
	if(InstrX.maxDysBk < arg_dys + InstrX.maxDysBk) 
	   InstrX.maxDysBk = arg_dys + InstrX.maxDysBk;	
    
	for (int i=InstrX.maxDysBk; i<InstrX.prc.length; i++) {		

	  double[] fdCalcdExpr_n = new double[arg_dys];  //* reset for each new i, this is array to be sorted	
	  //* Loop i=0 to N to calc and define array fdSum[N]
	  for(int n=0; n<arg_dys; n++)
		fdCalcdExpr_n[n] = calcdExprArg[i-n];  
	  
	  //* Sort to see if "C-C1" is ranked 20 of 20
	  double fdCalcdExpr_0 = fdCalcdExpr_n[0];  // make sure to get before sorting bec array gets perm sorted!
	  Arrays.sort(fdCalcdExpr_n);
	  //* Java's search does not do equal very well, so do custom search
	  //* int iRank = Arrays.binarySearch(fdSum, fdSum0) + 1;
    boolean blFound = false;
    int r = 0;
    int iRank = 0;
    while (!blFound && r < fdCalcdExpr_n.length) {	
      if (fdCalcdExpr_0 == fdCalcdExpr_n[r] ) {
    	  blFound = true;
    	  iRank = r+1;  // return index from 1 (not 0)
      }
      r++;
    }
    
    calcdExprFn[i] = iRank;
	}	  
  }  // calc() method		
	
}

