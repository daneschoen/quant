package program;

import java.util.ArrayList;


abstract class Strat_Abstract {

  final String CMD="";	
  int nested;      //* RIGHT NOW NO NESTING FOR NESTER FN'S!

  protected ArrayList<String> params = new ArrayList<String>();  
  protected final String cmdExpression;
  protected String arg_Expression;
  protected Instr InstrX;
  protected Session session;
  
  protected double[] calcdExprArg;          
  protected double[] calcdExprFn;
  
  protected double[] calcdExprFn_min;
  protected double[] calcdExprArg_min;  
			  
  
  /* Normal returns:   
   * - InstrX.maxDysBk
   * - calcdExprFn[i] for(int i=InstrX.maxDysBk; i<InstrX.prc.length; i++)  
   * 
   * _p intra BUT fixed entry, needs:
   * - frameBeg_timeCol, frameEnd_timeCol
   *   returns:
   * - InstrX.maxDysBk
   * - calcdExprFn[i] for(int i=InstrX.maxDysBk; i<InstrX.prc.length; i++)  
   * 
   * _b intra, FUTURE entry needs:
   * - evtBegTimeCol, evtEndTimeCol;
   * - evtBegDyFwd, evtEndDyFwd;
   * - evtBegFrameTimeCol, evtEndFrameTimeCol; 
   * - d
   *   returns:
   * - calcdExprFn_b[j]
   * 
   * 
   * Intrady variables
   * E(o, p@1500) < mvg(b, 15m)  
   * E(o, p@1500) < mvg(c, 15m)  
   * 
   * b(o, p@1500) < mvg(b, 15m)  
   * b(o, p@1500) < mvg(c, 15m)  
   * 
   */
  //* 0: daily, 1: daily but minute calculations, 2:daily but intraday past, 3: intrady future
  int calcType=0;   
  int evtBegTimeCol, evtEndTimeCol;
  int evtBegDyFwd, evtEndDyFwd;
  int evtBegFrameTimeCol, evtEndFrameTimeCol; 
  int d;
  
  
  Strat_Abstract(final Instr InstrX, final String cmdExpression, Session session) {
	this.session = session;
	this.InstrX = InstrX;
	this.cmdExpression = cmdExpression; 
	
    this.calcdExprFn = new double[InstrX.prc.length];  
    //this.calcdExprArg;
  }
    
  
  void parseAndCalc() throws Exception{
    parseAndSetConditions();
    calc();
  }
  
  abstract void parseAndSetConditions() throws Exception;
	/* Usually:
	  
	   getParams();
	   arg_Expression = params.get(0);
	   arg_dys = Integer.parseInt(params.get(1));
	  
     */
  
  void getParams() throws Exception{
	/*
	 * c-c1 = min(mvg(c-c1,14),3) => "mvg(c-c1,14),3"
	 * c-c1 = min(c-c1,3) => "c-c1,3"
	 * c > h1
	 * 
	 * g( min(mvg(c-c1,14),3),14 )
     * g( m(n(c,12),14), 2, 74 )
     * g( m(n(c,12),14) )  a mono fn  abc)
     * g( p@1200,14 )
     */
    //params = cmdExpression.split(",");	
	int y_Pleft = cmdExpression.indexOf("("); 
	int y_Pright = cmdExpression.lastIndexOf(")");
	String strInnerArg = cmdExpression.substring(y_Pleft+1, y_Pright).trim().toLowerCase();  
    
	y_Pright = strInnerArg.lastIndexOf(")");
	if (y_Pright >= 0) { 
			
	    if (y_Pright != strInnerArg.length()-1 && 
			strInnerArg.substring(y_Pright+1).indexOf(",") < 0	) {
			params.add(strInnerArg);
			strInnerArg = "";
		} else {
		    params.add(strInnerArg.substring(0,y_Pright+1).trim());
		    if (y_Pright != strInnerArg.length()-1) {
		      strInnerArg = strInnerArg.substring(y_Pright+1);
		      strInnerArg = strInnerArg.substring(strInnerArg.indexOf(",")+1);
		      for (String param : strInnerArg.split(",")) params.add(param.trim());
		    }  
		    
		} 
			   
	} else {	
	  for (String param : strInnerArg.split(",")) params.add(param.trim());
	}       
  }
  
  protected String[] getSplitInstr(Instr Instr_par, String tok) {
	/*
	 * ["us", "mvg(us.c - us.c1)"]  <==  "us.mvg(us.c - us.c1)"
	 * ["",   "mvg(us.c - us.c1)"]  <==  "mvg(us.c - us.c1)"
     *
	 * ["es",   "c1"]  <==  "es.c1"
	 * ["da",   "pivot(...)"]  <==  "da.pivot(...)"
	 */
	String[] instr_tok = new String[2];
    instr_tok[0] = String.valueOf(Instr_par.key);
    instr_tok[1] = tok;
    for (int k=0; k<InstrSpecs.idNames.length; k++) {	
	  String strInstr_k = InstrSpecs.idNames[k].toLowerCase() + ".";
      if (tok.indexOf(strInstr_k) == 0) { 
    	  instr_tok[0] = String.valueOf(k);  
	      //int z = line.indexOf(strInstr_k);
    	  instr_tok[1] = tok.substring(strInstr_k.length());
	      break;
      }
    }

    return instr_tok;
  }
  
  public String[] getSplitInstr(final String strInstrFn) {
	
	String strFn = strInstrFn;
    String strInstr_r="";
    for (int r=0; r<InstrSpecs.idNames.length; r++) {	
	  strInstr_r = InstrSpecs.idNames[r].toLowerCase() + ".";	
      if (strInstrFn.indexOf(strInstr_r) == 0) {
	      strFn = strInstrFn.substring(strInstr_r.length());
	      break;
	  }
	}
    
    return new String[]{strInstr_r, strFn};
  }  
  
  
  
  /*
   * us.sum(c-c1, 5) > 23.54  
   */
  void nestExpressionParseAndCalc(final Instr InstrX, final String arg_Expression, Session session) throws Exception {     
    Strat_Abstract stratExpression = new Strat_Expression(InstrX, arg_Expression, session);
	stratExpression.parseAndCalc();
	//if(stratExpression.maxDysBk > maxDysBk) maxDysBk = stratExpression.maxDysBk;
	calcdExprArg = stratExpression.calcdExprFn;
  }
 
  /*
 void nestOnceExpressionParseAndCalc2(final String arg_Expression) throws Exception {    	 
     ParseUtils2 parseUtils = new ParseUtils2();
     String strDysBkAndTimeCol = parseUtils.getDysBkAndTimeCol(InstrDep, arg_Expression);
     ArrayList<String> lstDysBkAndTimeCol = new ArrayList<String>();
     for (String param : strDysBkAndTimeCol.split(",")) lstDysBkAndTimeCol.add(param.trim());
     int cmdDyBk = Integer.parseInt(lstDysBkAndTimeCol.get(0));
     int cmdTimeCol = Integer.parseInt(lstDysBkAndTimeCol.get(1));
     if (cmdDyBk > maxDysBk) maxDysBk = cmdDyBk;	      
     for (int i=strategy.begTstDateIndex+maxDysBk; i<=strategy.endTstDateIndex; i++) {   
	   this.calcdExprArg[i] = InstrDep.prc[i-cmdDyBk][cmdTimeCol];
	 }        
  } 
  */ 
 
  abstract void calc() throws Exception;
    /* MUST set these  
     *   calcdExpr = new double[InstrX.maxPrcIndex+1];
     *   calcdExprFn = new double[InstrX.maxPrcIndex+1];
     * MUST call parseAndCalcNestExpression
     * MUST set maxDysBk
     * MUST of course do the actual calc
     */  
 

  //abstract void calc_intrady(int iDy) throws Exception;
  /* MUST set these  ?
   *   calcdExpr = new double[InstrX.maxPrcIndex+1];
   *   calcdExprFn = new double[InstrX.maxPrcIndex+1];
   * MUST call parseAndCalcNestExpression
   * MUST set maxDysBk
   * MUST of course do the actual calc
   */
}


