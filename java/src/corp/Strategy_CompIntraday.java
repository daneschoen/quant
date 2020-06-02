package program;

import java.util.ArrayList;

public class Strategy_CompIntraday extends Strategy_Abstract{

  int evtBegFrameTimeCol, evtEndFrameTimeCol; 
  int evtBegTimeCol, evtEndTimeCol;
  int evtBegDyFwd, evtEndDyFwd;  	

  
  Strategy_CompIntraday() {
    InstrDep = Instr.getInstance(Strategy.iDependentInstr);	
  }

  
  @Override
  void parseAndSetConditions(final String strCmdLine) throws Exception{
	/*    OR(b > b0:05, b0:05 > b0:10) 
	 * 0) Need to first check for OR
	 * 1) calc x cmd statements x times
	 * 2) combine into ONE prcSucc
	 * * NOTE: NOT recurrsion - or at most one recurrsion for all or statements!
	 */
	 
	if (strCmdLine.indexOf("or(") == 0) {
		blOr = true;
		ArrayList<String> arrCmdLine = getParams(strCmdLine);
		strategy = new Strategy_CompIntraday[arrCmdLine.size()];
	        
	    for (int x=0; x<arrCmdLine.size(); x++) {
	      String cmd_x = arrCmdLine.get(x);
	      strategy[x] = new Strategy_CompIntraday();
		  strategy[x].nested = 1;
		  strategy[x].parseAndSetConditions(cmd_x);
	    }  
	        
	} else {
	    splitSides(strCmdLine.trim().toLowerCase());	
	}
	    	  
  }
  
  @Override
  void calc() throws Exception{		
	if (!blOr) {  
		calcExpressionFnSides();  //* this often gets overriden!
	    evaluateEqn();
	} else {
		/*
			if (nested == 0) {
			    for (int x=0; x<strategy.length; x++) {		
		          strategy[x].calc();		      
		          for(int i=Strategy.begTstDateIndex+Strategy.maxDysBk; i<=Strategy.endTstDateIndex; i++) 
		    	    if(strategy[x].prcSucc[i]==1)
			  	      ParserCondition.prcSucc[i] = 1;
			    }    
		    } else if (nested == 1) {
		        prcSucc = new int[InstrDep.maxPrcIndex+1];
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

  
  @Override	  
  void calcExpressionFnSides() throws Exception{
    /*	  
      b < c1 - 10 / 2 
	  b < MIN(C3,5) + m(n()) * q()        
	  
	  b < p@1615 - 2.5    means given dy_i enter whenever bar < p@1615_i - 2.5
      b(o, p@1500) < p@1615 - 2.5
      b > h1 + 5
      b < p@1615 - 0.25z            
	  
      b > mvg(c, 15m)
      b > mvg(b, 15m, c1, p@1500)
      b > mvg(b, 15m, c1)
      b > mvg(b, 15m, 1440m)  60*24 = 1d
      b > mvg(b, 15m, 24h)  
      b > mvg(b, 15m, o, 24h)  
      b(o, p@1500) < mvg(b, 15m)
  
	  b-b15 = MIN(C-C1, 15)
	  
	*/
	  
	for (int s=0; s<2; s++) {	  
	   Strat_Abstract stratIntraday_lr = new Strat_ExprIntraday(strCmdSides[s]);
	   stratIntraday_lr.parseAndCalc();
	   calcdExprFn[s] = stratX.calcdExprFn;
		      
	   if (stratX.maxDysBk > Strategy.maxDysBk) Strategy.maxDysBk = stratX.maxDysBk;
	} 
    Strat_Abstract stratExprIntraday = new Strat_ExprIntraday(strCmdSides[1]);
    stratExprIntraday.parseAndCalc();
	calcdExprFn[1] = stratX.calcdExprFn;
	      
		  if (stratX.maxDysBk > maxDysBk) maxDysBk = stratX.maxDysBk;
		  if (maxDysBk > Strategy.maxDysBk) Strategy.maxDysBk = maxDysBk;
		
		  
  }
	  
  
  @Override	  
  void evaluateEqn() throws Exception {
	    
		if(nested==1)  
		  prcSucc = new int[InstrDep.maxPrcIndex+1];  
	    double[] lrValue;
	    
		for (int i=Strategy.begTstDateIndex+maxDysBk; i<=Strategy.endTstDateIndex; i++) {
	      //D System.out.println(calcdExprFn[0][i] + " "+ i + " " +  calcdExprFn[1][i]);
		  lrValue = new double[2];
		  for(int s=0; s<2; s++)
		    lrValue[s] = calcdExprFn[s][i];

		  boolean blSignal = false;
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

		  if (nested == 0) {
			  if(blSignal)
			  	ParserCondition.prcSucc[i] = 1;
			  else
			  	ParserCondition.prcSucc[i] = 0;		
		  } else if (nested == 1) {
			  if(blSignal)
			  	prcSucc[i] = 1;
			  else
			  	prcSucc[i] = 0;							
		  }
				  
		}  //* i loop

  }  //* method evaluate

}
