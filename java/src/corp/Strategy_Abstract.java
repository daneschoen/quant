package program;

import java.util.ArrayList;
import java.util.List;

/*
 * Superclass for two-sided equations
 */

class Strategy_Abstract {

  static final String CMD="";	
  //int nested=0;    

  private Strategy_Abstract[] strategy;
  private boolean blOr = false;  //false = "and"
  
  protected int[] prcSucc;   //* each index represents a signal
  protected String[] strCmdSides;
  protected String cmdEql;
		
  protected double[][] calcdExprFn;	  
  
  protected Instr InstrX;
  protected String cmdStatement;
  protected Session session;
  
  
  Strategy_Abstract(Instr InstrX, String cmdStatement, Session session) {
    this.InstrX = InstrX;
    this.cmdStatement = cmdStatement;
    this.session = session;
    
    calcdExprFn = new double[2][InstrX.prc.length];
    prcSucc = new int[InstrX.prc.length];   
  }
  
  
  void parseAndSetConditions() throws Exception{
	/*    OR(c > c1,c1 > c2) 
	 * 0) Need to first check for OR
	 * 1) calc x cmd statements x times
	 * 2) combine into ONE prcSucc
	 * * NOTE: NOT recursion - or at most one recursion for all or statements!
	 */
	   
	if (cmdStatement.indexOf("or(") == 0) {
		blOr = true;
		ArrayList<String> arrCmdLine = getParams(cmdStatement);
		strategy = new Strategy_Compare[arrCmdLine.size()];
        
		int maxOrStatements = arrCmdLine.size();
		if(session.USERTYPE==0)
	      maxOrStatements = 2;
		
        for (int x=0; x<maxOrStatements; x++) {
          String cmd_x = arrCmdLine.get(x);
          strategy[x] = new Strategy_Compare(InstrX, cmd_x, session);
	      strategy[x].parseAndSetConditions();
        }  
        
	} else {
		splitSides(cmdStatement.trim().toLowerCase());	
	}  
			
  }
  
  protected void splitSides(String strCmdLine) throws Exception {
	//* Split sides and get ineq
	strCmdSides = new String[2];
	ParseUtils2 parse = new ParseUtils2(session);
	parse.splitSides(strCmdLine);
	cmdEql = parse.cmdEql;
	strCmdSides = parse.strSides;	
  }
  
  protected ArrayList<String> getParams(final String cmdExpression) throws Exception{
   /*
    * c-c1 = min(mvg(c-c1,14),3) => "mvg(c-c1,14),3"
    * c-c1 = min(c-c1,3) => "c-c1,3"
    * c > h1
    * 
    * OR(wait(c<c1)>2; c=min(c,10))
    * WAIT(OR(C>C1; C1>C2)) > 3
    * 
    * g( min(mvg(c-c1,14),3),14 )
    * g( m(n(c,12),14), 2, 74 )
    * g( m(n(c,12),14) )  a mono fn  abc)
    * g( p@1200,14 )
    */
	
	ArrayList<String> params = new ArrayList<String>();    
	
	int y_Plf = cmdExpression.indexOf("("); 
	int y_Prt = cmdExpression.lastIndexOf(")");
	String strInnerArg = cmdExpression.substring(y_Plf+1, y_Prt).trim().toLowerCase();  
	
	int y_Semi = strInnerArg.lastIndexOf(";");
	if (y_Semi >= 0) {
		for (String eqn : strInnerArg.split(";")) params.add(eqn.trim());
	} else {
	    y_Prt = strInnerArg.lastIndexOf(")");
	    if (y_Prt >= 0) { 
		    params.add(strInnerArg.substring(0,y_Prt+1).trim());
		    strInnerArg = strInnerArg.substring(y_Prt+1);
		    strInnerArg = strInnerArg.substring(strInnerArg.indexOf(",")+1);
	    }	
	    for (String param : strInnerArg.split(",")) params.add(param.trim());
	}    
	return params;
  }  
  
  
  void calc() throws Exception{		

	if (!blOr) {  
		
	    calcExpressionFnSides();  //* this often gets overriden!
        evaluateEqn();
        
	} else {
		//if (nested == 0) {
		    for (int x=0; x<strategy.length; x++) {		
	          strategy[x].calc();		      
	          for(int i=InstrX.maxDysBk; i<InstrX.prc.length; i++)  
	    	    if(strategy[x].prcSucc[i]==1)
		  	      prcSucc[i] = 1;
		    }
		/*    
	    } else if (nested == 1) {
  	
	        prcSucc = new int[InstrDep.prc.length];
	    	for (int x=0; x<strategy.length; x++) {
	    	  strategy[x].calc();  //* here at this call blOr = FALSE!
	          for(int i=Strategy.begTstDateIndex+Strategy.maxDysBk; i<=Strategy.endTstDateIndex; i++) 
		        if(strategy[x].prcSucc[i]==1)
		    	  prcSucc[i] = 1;  	    	  
	        }
		}
		*/
	}
  }  
  
  void calcExpressionFnSides() throws Exception{
    /*
      us.c < us.c1
      	  
	  C2 < MIN(C3,5)                
	  P1@1100 > MAX(C1, 10) 
	  C + 50 > C4 
	  C > MAX(P1@1100, 10)
			  
	  C-C1 = MIN(C-C1, 15)    
	  ABS(C-C1) = MIN(ABS(C-C1), 15)
	  
	  c + 5 > m(n()) * q() + 10.5	  
	  
	  or(c > c1,c1 > c2)
    */   		
	
	for (int s=0; s<2; s++) {
	  Strat_Abstract stratExpr = new Strat_Expression(InstrX, strCmdSides[s], session);
      stratExpr.parseAndCalc();
      calcdExprFn[s] = stratExpr.calcdExprFn;  
	}
	  
  }
  
  void evaluateEqn() throws Exception {
    
	//if(nested==1)  
	//  prcSucc = new int[InstrDep.prc.length];  
    double[] lrValue;
    boolean blSignal; 
	for (int i=InstrX.maxDysBk; i<InstrX.prc.length; i++) {    
      //System.out.println(calcdExprFn[0][i] + " "+ i + " " +  calcdExprFn[1][i]);
	  lrValue = new double[2];
	  for(int s=0; s<2; s++)
	    lrValue[s] = calcdExprFn[s][i];

	  blSignal = false;
	  if (cmdEql.equals(">")) {  
		  if ( lrValue[0]  > lrValue[1] ) blSignal = true;  
	  } else if (cmdEql.equals(">=")) {
		  if ( lrValue[0] >= lrValue[1] ) blSignal = true;  
	  } else if (cmdEql.equals("<")) {
		  if ( lrValue[0]  < lrValue[1] ) blSignal = true;  	
	  } else if (cmdEql.equals("<=")) {		
		  if ( lrValue[0] <= lrValue[1] ) blSignal = true;  
	  } else if (cmdEql.equals("=")) {
		  if ( lrValue[0] == lrValue[1] ) blSignal = true;  
	  }   		  	  	  

	  if(blSignal)
	    prcSucc[i] = 1;
	  else
		prcSucc[i] = 0;							
			  
	}  //* i loop

  }  //* method evaluate
  
}
