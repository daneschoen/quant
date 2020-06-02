package program;

public class Strat_Mvg extends Strat_Abstract{
	
  static final String CMD="mvg";
	  
  private int arg_dys;
  private int arg_min;
  
  
  //Strat_Mvg(Strategy strategy, Instr InstrX, final String cmdExpression) {
  Strat_Mvg(final Instr InstrX, final String cmdExpression, Session session) {
	super(InstrX, cmdExpression, session);
  }
 
  
  @Override
  public void parseAndSetConditions() throws Exception{
    /*
     * da.mvg(da.c-da.c1, 50) > c/1000 
     * 
	 * mvg(H/L/C/O/P@1100, days) >= 50.4
	 * mvg(H/L/C/O/P@1100, days) >= mvg(H/L/C/O/P@1100, days)
	 * mvg(H/L/C/O/P@1100, days) >= h1
	 * 
	 * mvg(c-c1, 50) > ...
	 * mvg(c, 50) / mvg(c, 200) > 1.10
     * mvg(c, 50) > mvg(c, 200) + 100
     * mvg(c, 50) - 100 > mvg(c, 200)
     * mvg(c, 50) > mvg(c, 200)*1.10
     * 
     * ================================
     * for AGlobal.BUILD_VER == 1 ONLY!
     * 
     * mvg(abs(c-c1),c) 
     * 
     * Still fixed time, but intrady:
     * o > mvg(p@0930, 9, 30m) default 0000:2355 
     * o > mvg(p@0930, 9, 30m, 0930:1615)
     * o > mvg(p@0930, 9, 15m, 0930:1615)
     * 
     * E > mvg(b,10m)
     * E > mvg(b5,1h)
     * b > mvg(abs(b-b10), 15m)
     * 
     * us.mvg(c,14) > us.c
     * 
	 * mvg(H/L/C/O/P@1100, days) >= 50.4
	 * mvg(H/L/C/O/P@1100, days) >= mvg(H/L/C/O/P@1100, days)
	 * mvg(H/L/C/O/P@1100, days) >= H1
	 * 
	 * mvg(c, 50) / mvg(c, 200) > 1.10
     * mvg(c, 50) > mvg(c, 200) + 100
     * mvg(c, 50) - 100 > mvg(c, 200)
     * mvg(c, 50) > mvg(c, 200)*1.10
     * 
     * --------------------------------
     * True intrady, variable time entry:
     * 
     * Enter(0d, 0930:1520)
     * b + 2.0 > mvg(b, 9, 10m)   => returns all mvg prc's between entry times 
     * => returns every entry when prc + 2.0 > mvg
     * 
     * E > mvg(b, 10m)
     * E > mvg(b5, 1h)
     * b > mvg(abs(b-b10), 15m)
     * 
     *   Event(0@Ref->0@1555, 3rd time)
     *   Event(0@1800->2@1615)
     * B > mvg(b, 60m, -1.0, 1)
     * B > mvg(b, 60m, -1.5z, 2)  
	 */	    
	getParams();
	arg_Expression = params.get(0);
	arg_dys = Integer.parseInt(params.get(1));
	
	if(session.USERTYPE == 0) 
	  if(params.get(0).indexOf("-") >= 0 || params.get(0).indexOf("+") >= 0 || params.get(0).indexOf("*") >= 0 || params.get(0).indexOf("/") >= 0
	    || params.get(0).indexOf("(") >= 0	  )
		  throw new ExceptionCmd("Error in nested syntax");
	
  }	
	
  
  @Override
  void calc() throws Exception{	  
	nestExpressionParseAndCalc(InstrX, arg_Expression, session);
    if(InstrX.maxDysBk < arg_dys + InstrX.maxDysBk) 
       InstrX.maxDysBk = arg_dys + InstrX.maxDysBk;
    
    //for (int i=strategy.begTstDateIndex+maxDysBk; i<=strategy.endTstDateIndex; i++)        
    for(int i=0+InstrX.maxDysBk; i<InstrX.prc.length; i++) {
	  calcdExprFn[i] = calc(i);
    }
		  
  }  //* calc method

  double calc(int i) throws Exception{      
	double fdMvg_i=0;
	for(int n=0; n<arg_dys; n++)
	  fdMvg_i += calcdExprArg[i-n];
	fdMvg_i /= arg_dys;
	return fdMvg_i;
  }  //* calc_i method 
  
  
  /* Just returns the value on right
   * b(o, p@1500) < mvg(b, 15m)
   * b(o, p@1500) < mvg(c, 15m)    
   */	 
  /*
  double calc_intrady(int i) throws Exception{     
	  
	double fdMvg_ij=0;
	for(int k=0; k<arg_min; k++)
	  fdMvg_ij += InstrX.prc[i-n][i-n];
	
    boolean blFoundEvent = false;
    int startCol;
    int endCol;
    for (int iDysFwd=evtBegDyFwd; iDysFwd<=evtEndDyFwd; iDysFwd++) {	
   	  
 	  startCol = evtBegFrameTimeCol; 
       if(iDysFwd == evtBegDyFwd) 
   	    startCol = evtBegTimeCol; 
       endCol = evtEndFrameTimeCol;  
   	  if(iDysFwd == evtEndDyFwd) 
   	    endCol = evtEndTimeCol;
   		      
       for (int j=startCol; j<=endCol; j++) {  //* go across time
          prc_ij = InstrX.prc[i + iDysFwd][j];
   	     if ((ptsEnter <  0 && prc_ij <= prcThresh_i) || 
   		     (ptsEnter >= 0 && prc_ij >= prcThresh_i)) { 
   	    	 
   	    	 Strategy.trdEntryDyIndex.add(i + iDysFwd);   	
   	    	 Strategy.trdEntryDyCondIndex.add(i);
   	    	 Strategy.trdEntryMinIndex.add(j);	 
   	    	 Strategy.trdEntryPrc.add(prc_ij);  //prcThresh_i
   	    	 
   	    	 blFoundEvent = true;
		         break;
   	     }        
   	  }  //*  for look across in time 
   	  if(blFoundEvent) break;
   }  //* for look fwd in days
	
	
	fdMvg_ij /= arg_dys;
    return fdMvg_ij;	
  }  //* calc_intrady method  
  */
  
}
