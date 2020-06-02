package program;


public class Strat_MaxMin extends Strat_Abstract{
  
  String CMD;
  private int arg_dys;
  
  
  Strat_MaxMin(final Instr InstrX, final String cmdExpression, Session session) {
	super(InstrX, cmdExpression, session);
  }
  
  
  @Override
  void parseAndSetConditions() throws Exception{
	if (cmdExpression.indexOf("min") == 0) CMD = "min";
	else if (cmdExpression.indexOf("max") == 0) CMD = "max"; 	
	getParams();
	arg_Expression = params.get(0);
	arg_dys = Integer.parseInt(params.get(1));

	if(session.USERTYPE == 0) {
	  if(params.get(0).indexOf("-") >= 0 || params.get(0).indexOf("+") >= 0 || params.get(0).indexOf("*") >= 0 || params.get(0).indexOf("/") >= 0)
	    throw new ExceptionCmd("Error in MAX/MIN nested syntax");
	  if (params.get(0).indexOf("(") >= 0) {
		  if (params.get(0).indexOf("vix") >= 0 || 
			  params.get(0).indexOf("volhist") >= 0 ||
			  params.get(0).indexOf("h(") >= 0  ||
			  params.get(0).indexOf("l(") >= 0 		
			 ) {
		      //* pass	
	      } else {   		
		      throw new ExceptionCmd("ERROR - in MAX/MIN nested syntax");
	      }  
	  } 		  
	}	  
  }
  
  
  @Override
  void calc() throws Exception{
    /*	  
      C > MAX(US.C1,10)   
	  C > MAX(C1,10)  means today’s close is greater than closes C1 to C11
	  C = MAX(C,10)   today’s close is the maximum close from C to C10, 
	                  i.e., closed at the 10 day high 
	  C2 < MIN(C3,5)                
	  P1@1100 > MAX(C1, 10) 
	  C + 50 > MAX(C1, 10) 
	  C > MAX(P1@1100, 10)
	  R = MIN(R,10) 
	  VIX(C1) = MAX(VIX(C1), 20) 
	  VolHist(30, C) = max(VolHist(30, C), 3)
	  h(p@1015,p@1435) = max(h(p@1015,p@1435),14)
	  
	for AGlobal.BUILD_VER == 1 ONLY!
	  C-C1 = MIN(C-C1, 15)  
      C1-C2 > MIN(C3-C4, 15)  
      ABS(C-C1) = MIN(ABS(C-C1), 15)
	*/
	  
	/*  
	if (AGlobal.BUILD_VER == 2) {  
      if (this.argExpression.indexOf("r") == 0) {
    	  int cmdDyBk = 0;     
  	      if(this.argExpression.length() > 1)
  	        cmdDyBk = Integer.parseInt(this.argExpression.substring(1).trim());   
          if (cmdDyBk > maxDysBk) maxDysBk = cmdDyBk;
	      int maxFnDysBk = arg_dys + maxDysBk;
	      if (maxFnDysBk > maxDysBk) maxDysBk = maxFnDysBk;	  
	      for (int i=Strategy.begTstDateIndex+maxDysBk; i<=Strategy.endTstDateIndex; i++) {   
		    calcdExprArg[i] = InstrDep.prc[i-cmdDyBk][InstrDep.hiDyCol] - InstrDep.prc[i-cmdDyBk][InstrDep.loDyCol];
		  } 
      } else {
	      ParseUtils2 parseUtils = new ParseUtils2();
          String strDysBkAndTimeCol = parseUtils.getDysBkAndTimeCol(InstrDep, this.argExpression);
          ArrayList<String> lstDysBkAndTimeCol = new ArrayList<String>();
          for (String param : strDysBkAndTimeCol.split(",")) lstDysBkAndTimeCol.add(param.trim());
          int cmdDyBk = Integer.parseInt(lstDysBkAndTimeCol.get(0));
          int cmdTimeCol = Integer.parseInt(lstDysBkAndTimeCol.get(1));
     
          if (cmdDyBk > maxDysBk) maxDysBk = cmdDyBk;
	      int maxFnDysBk = arg_dys + maxDysBk;
	      if (maxFnDysBk > maxDysBk) maxDysBk = maxFnDysBk;	  
	      for (int i=Strategy.begTstDateIndex+maxDysBk; i<=Strategy.endTstDateIndex; i++) {   
		    calcdExprArg[i] = InstrDep.prc[i-cmdDyBk][cmdTimeCol];
		  } 
	  }
	*/  

	nestExpressionParseAndCalc(InstrX, arg_Expression, session); 
	if(InstrX.maxDysBk < arg_dys + InstrX.maxDysBk) 
	  InstrX.maxDysBk = arg_dys + InstrX.maxDysBk;
		 		 
    if (CMD.equals("min")) {  
		double fdMin;
		for (int i=InstrX.maxDysBk; i<InstrX.prc.length; i++) {
		  fdMin = Double.MAX_VALUE;	
	      for(int m=0; m<=arg_dys; m++)
		    if(calcdExprArg[i-m] < fdMin) fdMin = calcdExprArg[i-m]; 	  
		  
		  calcdExprFn[i] = fdMin;
		}
		
    } else if (CMD.equals("max")) {  
        double fdMax;  
	    for (int i=InstrX.maxDysBk; i<InstrX.prc.length; i++) {
	      fdMax = -Double.MAX_VALUE;
		  for(int m=0; m<=arg_dys; m++)
		    if(calcdExprArg[i-m] > fdMax) fdMax = calcdExprArg[i-m]; 	  
		  
		  calcdExprFn[i] = fdMax;
          //System.out.println(i + " " +  calcdExprFn[i]);	  
	    }
    }
			  
  }  //* calc method

}
