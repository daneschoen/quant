package program;


public class Strat_Factory {
  
  private Strat_Factory() {
  }
  
  
  static private Strat_Abstract getStrat(final Strat_Abstract strat) throws Exception {
	strat.nested = 0;
	return strat; 
  }
  
  static Strat_Abstract getInstance(final Instr InstrX, final String cmdExpression, Session session) throws Exception {   
	  
	if (cmdExpression.indexOf("min(") == 0 || cmdExpression.indexOf("max(") == 0) {
		return getStrat(new Strat_MaxMin(InstrX, cmdExpression, session));
	} else if (cmdExpression.matches("h\\d*|h\\(.+") || cmdExpression.matches("l\\d*|l\\(.+")) {
		return getStrat(new Strat_HighLow(InstrX, cmdExpression, session));
	} else if (cmdExpression.indexOf("abs(") == 0 && session.USERTYPE == 4) {
		return getStrat(new Strat_Abs(InstrX, cmdExpression, session));	
	} else if (cmdExpression.indexOf("mvg(") == 0) {
		return getStrat(new Strat_Mvg(InstrX, cmdExpression, session));		
	//} else if (cmdExpression.indexOf("mvg_p(") == 0 && session.USERTYPE == 4) {
	//	return getStrat(new Strat_Mvg_p(InstrX, cmdExpression, session));
	//} else if (cmdExpression.indexOf("mvg_b(") == 0 && session.USERTYPE == 4) {
	//	return getStrat(new Strat_Mvg_b(InstrX, cmdExpression, session));
	} else if (cmdExpression.indexOf("streak(") == 0) {  
		return getStrat(new Strat_Eqn_Streak(InstrX, cmdExpression, session));
	} else if (cmdExpression.indexOf("stdev(") == 0 && session.USERTYPE == 4) {	
		return getStrat( new Strat_Stdev(InstrX, cmdExpression, session));  		     		
	} else if (cmdExpression.indexOf("zscore(") == 0) {
		return getStrat(new Strat_Zscore(InstrX, cmdExpression, session));					
	} else if (cmdExpression.indexOf("pivot(") == 0) {		
		return getStrat(new Strat_Pivot(InstrX, cmdExpression, session));     
	//} else if (cmdExpression.indexOf("pivota(") == 0 && session.USERTYPE == 4) {
	//	return getStrat(new Strat_PivotA(InstrX, cmdExpression, session));  	
	//} else if (cmdExpression.indexOf("pivot2(") == 0 && session.USERTYPE == 4) {
	//	return getStrat(new Strat_Pivot2(InstrX, cmdExpression, session));     	
	//} else if (cmdExpression.indexOf("pivot3(") == 0 && session.USERTYPE == 4) {
	//	return getStrat(new Strat_Pivot3(InstrX, cmdExpression, session));  
	//} else if (cmdExpression.indexOf("pivot4(") == 0 && session.USERTYPE == 4) {
	//	return getStrat(new Strat_Pivot4(InstrX, cmdExpression, session));  
	//} else if (cmdExpression.indexOf("pivot4a(") == 0 && session.USERTYPE == 4) {
	//	return getStrat(new Strat_Pivot4A(InstrX, cmdExpression, session));  		
	//} else if (cmdExpression.indexOf("pivot4a(") == 0 && session.USERTYPE == 4) {
	//	return getStrat(new Strat_Pivot4A(InstrX, cmdExpression, session));
	//} else if (cmdExpression.indexOf("pivot7(") == 0 && session.USERTYPE == 4) {
	//	return getStrat(new Strat_Pivot7(InstrX, cmdExpression, session));  				
	} else if (cmdExpression.indexOf("volhist(") == 0) {
		return getStrat(new Strat_VolHist(InstrX, cmdExpression, session));		
	//} else if (cmdExpression.indexOf("sum(") == 0) {
	//	return getStrat(new Strat_VolHist(InstrX, cmdExpression, session));		
	//} else if (cmdExpression.indexOf("rank(") == 0) {
	//	return getStrat(new Strat_VolHist(InstrX, cmdExpression, session));		
	} else if (cmdExpression.indexOf("wait(") == 0) {
		return getStrat(new Strat_Eqn_Wait(InstrX, cmdExpression, session));				
	} else {
    	return null;
    }
	/*
	else {	
    	return getStrat(InstrX, new Strat_Expression(cmdExpression), cmdExpression);
    }
	*/
  }  
	
}
