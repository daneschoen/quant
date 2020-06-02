package program;

import java.util.ArrayList;

public class Strat_HighLow extends Strat_Abstract{

  String CMD;
  
  private int arg_begTimeCol;
  private int arg_begDyBk;
  private int arg_endTimeCol;
  private int arg_endDyBk;
 
  private ParseUtils2 parseUtils;
  
  Strat_HighLow(final Instr InstrX, final String cmdExpression, Session session) {
	super(InstrX, cmdExpression, session);
	parseUtils = new ParseUtils2(session);
  }
  
  /* l
   * h2
   * 
   * h(t1@815,t@1435)
   * 
   * h(p1@815,p@1435)
   * p@1100 > h(o,p@1000) means p@1100 is greater than the max from o to p@1000
   * c > l(p1@1400,p@1000)
   */
  @Override
  public void parseAndSetConditions() throws Exception{
 
	if(cmdExpression.substring(0,1).equals("h")) 
	  CMD = "high";  
	else if(cmdExpression.substring(0,1).equals("l"))
	  CMD = "low";
	
	int y_Pleft = cmdExpression.indexOf("("); 
	//* h
	if (cmdExpression.length() == 1) {
	    arg_begTimeCol = InstrX.opnDyCol;
	    arg_begDyBk = 0; 
	    arg_endTimeCol = InstrX.clsDyCol;	
	    arg_endDyBk = 0;
	//* h3	  
	} else if (y_Pleft == -1  && cmdExpression.length() > 1) {
	    arg_begTimeCol = InstrX.opnDyCol;
	    arg_begDyBk = Integer.parseInt(cmdExpression.substring(1).trim());
	    arg_endTimeCol = InstrX.clsDyCol;	
	    arg_endDyBk = arg_begDyBk;
	//* h(p1@815,p@1435)	  
	} else {
        getParams();
        //String strDysBkAndTimeCol = parseUtils.getDysBkAndTimeCol(InstrX, params.get(0));
        String strDysBkAndTimeCol = parseUtils.parseTok(InstrX, params.get(0));
        ArrayList<String> lst = new ArrayList<String>();
        for(String param : strDysBkAndTimeCol.split(",")) 
          lst.add(param.trim());
        //InstrStart = Instr.getInstance(Integer.parseInt(lst.get(0)));
        arg_begDyBk = Integer.parseInt(lst.get(1));
        arg_begTimeCol = Integer.parseInt(lst.get(2));
        
        strDysBkAndTimeCol = parseUtils.parseTok(InstrX, params.get(1));    
        lst = new ArrayList<String>();
        for(String param : strDysBkAndTimeCol.split(","))
          lst.add(param.trim());
        arg_endDyBk = Integer.parseInt(lst.get(1));       
        arg_endTimeCol = Integer.parseInt(lst.get(2));
	}
  }
	

  @Override
  public void calc() throws Exception{
	/* l, h2
	 * 
	 * h(t1@815,t@1435)
	 * 
	 * h(p1@815,p@1435)
	 * p@1100 > h(o,p@1000) means p@1100 is greater than the max from o1 to p@1000
	 * c > l(p1@1400,p@1000)
	 */	  	  
	 if(InstrX.maxDysBk < arg_begDyBk + InstrX.maxDysBk) 
		InstrX.maxDysBk = arg_begDyBk + InstrX.maxDysBk;
	    	  	 
     if (CMD.equals("low")) {
	     for(int i=InstrX.maxDysBk; i<InstrX.prc.length; i++)
	       calcdExprFn[i] = calcLow(i);
	      
	 } else if (CMD.equals("high")) {
	     for(int i=InstrX.maxDysBk; i<InstrX.prc.length; i++) {
	       calcdExprFn[i] = calcHigh(i);   
	     }
	}  
    
  }  //* calc method
  
  
  double calc(int i) throws Exception{ 
	if(CMD.equals("low")) 
	  return calcLow(i);
	else 
	  return calcHigh(i);
  }
  
  //double calcHigh(int i) throws Exception{	  
  double calcHigh(int i) {
	
	double fdMax=0;
	try {  
    if (arg_begTimeCol==InstrX.opnDyCol && arg_endTimeCol==InstrX.clsDyCol 
    	&& arg_begDyBk == arg_endDyBk) {
          fdMax = InstrX.prc[i-arg_begDyBk][InstrX.hiDyCol];
    } else {
        int startTimeCol, endTimeCol;
	    fdMax=-Double.MAX_VALUE;
	    
	    startTimeCol=arg_begTimeCol;
	    endTimeCol=InstrX.lastTimeCol;
	    for (int iDyBk=arg_begDyBk; iDyBk>=arg_endDyBk; iDyBk--) {
	        
	      if(iDyBk != arg_begDyBk) startTimeCol = InstrX.firstTimeCol;
	      if(iDyBk == arg_endDyBk) endTimeCol = arg_endTimeCol;	    
	        
	      for (int jTimeCol=startTimeCol; jTimeCol<=endTimeCol; jTimeCol++) {
	        if(InstrX.prc[i-iDyBk][jTimeCol] > fdMax) 
	          fdMax = InstrX.prc[i-iDyBk][jTimeCol];  	  
	      }
	    }  
    }
    
	} catch(Exception e) {
	
	}
	return fdMax;
  }
  
  
  double calcLow(int i) throws Exception{
    double fdMin;
    if (arg_begTimeCol==InstrX.opnDyCol && arg_endTimeCol==InstrX.clsDyCol
	  && arg_begDyBk == arg_endDyBk){
        fdMin = InstrX.prc[i-arg_begDyBk][InstrX.loDyCol];
    } else {
	    int startTimeCol, endTimeCol;
        fdMin=Double.MAX_VALUE;
      
        startTimeCol=arg_begTimeCol;
        endTimeCol=InstrX.lastTimeCol;
        for (int iDyBk=arg_begDyBk; iDyBk>=arg_endDyBk; iDyBk--) {
    	  
            if(iDyBk != arg_begDyBk) startTimeCol = InstrX.firstTimeCol;
            if(iDyBk == arg_endDyBk) endTimeCol = arg_endTimeCol;	        	
        
            for (int jTimeCol=startTimeCol; jTimeCol<=endTimeCol; jTimeCol++) {
                if(InstrX.prc[i-iDyBk][jTimeCol] < fdMin) 
                fdMin = InstrX.prc[i-iDyBk][jTimeCol];  	  
            }
        }  
    }
    return fdMin;
  }  
    
}
