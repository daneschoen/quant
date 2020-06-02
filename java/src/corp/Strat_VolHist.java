package program;

public class Strat_VolHist extends Strat_Abstract{

  //* volhist(days, H/L/C/O/P@1100) >= 50.4
  static final String CMD = "volhist";
  
  int arg_dys;

  
  Strat_VolHist(final Instr InstrX, final String cmdExpression, Session session) {
	super(InstrX, cmdExpression, session);
  }
	  
	  
  @Override
  public void parseAndSetConditions() throws Exception{
    getParams();
    //*** ATTENTION: params reversed !
    arg_Expression = params.get(0);
    arg_dys = Integer.parseInt(params.get(1));
    
    if(session.USERTYPE == 0) 
	  if(params.get(1).indexOf("-") >= 0 || params.get(1).indexOf("+") >= 0 || params.get(1).indexOf("*") >= 0 || params.get(1).indexOf("/") >= 0
	    || params.get(1).indexOf("(") >= 0)
	    throw new ExceptionCmd("Error in nested syntax"); 
  }
	
  
  @Override
  public void calc() throws Exception{
    /*
      volhist(O/H/L/C/P@1100, DAYS) >= 50.4
   
      x_t = ln (C_t/C_t-1)
      Take cmdDays mean 
      VolHist = sqrt[(1/cmdDays)Sigma_1_cmdDays(x_t-mu)^2]
    */	  
	nestExpressionParseAndCalc(InstrX, arg_Expression, session);
	if(InstrX.maxDysBk < arg_dys + InstrX.maxDysBk) 
	  InstrX.maxDysBk = arg_dys + InstrX.maxDysBk;	
 	
	double mu_i=0;
	double fdVar_i=0;
	double lnChg=0;
	for (int i=InstrX.maxDysBk; i<InstrX.prc.length; i++) {
	  //* first get mean for latest cmdDays (slow way to calc var...)	
	  mu_i=0;
      for (int n=0; n<arg_dys; n++) {
    	//lnChg = Math.log(cmdInstr.prices[i-cmdDaysBk-n][cmdTimeCol]/cmdInstr.prices[i-cmdDaysBk-n-1][cmdTimeCol]);
    	lnChg = Math.log(calcdExprArg[i-n]/calcdExprArg[i-n-1]);
    	mu_i += lnChg;
      }
      mu_i /= arg_dys;
	       
      //* volHist = sqrt[(1/cmdDays)Sigma_1_cmdNDays(x_t-mu)^2]
      fdVar_i=0;
	  for (int n=0; n<arg_dys; n++) {
		lnChg = Math.log(calcdExprArg[i-n]/calcdExprArg[i-n-1]);
	    fdVar_i += Math.pow(lnChg-mu_i, 2);
	  }  
	  calcdExprFn[i] = Math.sqrt((1.0/((double)arg_dys-1.0))*fdVar_i);
	  calcdExprFn[i] *= Math.sqrt(252)*100.0;
	}
	
  }  //* calc method
  
}
