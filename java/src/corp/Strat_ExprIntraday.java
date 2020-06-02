package program;

import java.util.HashMap;
import java.util.Map;
import java.util.regex.Pattern;
import java.util.regex.Matcher;


class Strat_ExprIntraday extends Strat_Abstract{
  
  protected Instr[] tokInstr;
  protected int[] tokType;      //* 0: O,C,H,L,P   2:R   3:S   5:Lvl 
  protected int[] tokDayBk;
  protected int[] tokTimeBk;
  protected int[] tokTimeCol;
  protected double[] tokfdLvl;
  protected int[] tokOp;
  protected Map<Integer,Strat_Abstract> tokStrat = new HashMap<Integer,Strat_Abstract>();	
    

  Strat_ExprIntraday(final String cmdExpression) {
	super(cmdExpression);
  }
  
  @Override
  public void parseAndSetConditions() throws Exception{
    /*
      b < p@1445 - 2.5    means given dy_i enter whenever bar < p@1445_i - 2.5	  
      b < c1 - 10 / 2 
	  b < MIN(C3,5) + m(n()) * q()        
	  
      E(1615, 1d1500) < p@1615 - 2.5
      E(1do, 1500) < p@1615 - 2.5z
      E(1615, +1h) < p@1615 - 2.5z
      b > h1 + 5
      b < p@1615 - 0.25z            
	  
	search(0700, 1d1615, all/day)  
	  b > b5m
	  b - b1h2m > 1.5
	  b > b1d5m
	  
      b > mvg(c, 15m)
      b > mvg(b, 15m, c1, p@1500)
      b > mvg(b, 15m, c1)
      b > mvg(b, 15m, 1440m)  60*24 = 1d
      b > mvg(b, 15m, 24h)  
      b > mvg(b, 15m, o, 24h)  
      E(o, 1d1500) < mvg(b, 15m)
  
	  b-b15m = MIN(b-b15m, 15)
	  
	  streak(b <= b1h30m) = 3
	    streak(std(us.c - us.c1,14) > 3) = 3 
        us.streak(std(c - c1,14) > 3) = 3
	  
	*/       		  
    int numOp=0;
    String strFind = "[*/+-]";
    Pattern pattern = Pattern.compile(strFind); 
    Matcher matcher = pattern.matcher(cmdExpression); 
    while(matcher.find()) 
      numOp++;  
    if(cmdExpression.indexOf("-") != 0)
      numOp++;	

	tokInstr = new Instr[numOp];
	tokDayBk = new int[numOp];	
	tokTimeCol = new int[numOp];
	tokfdLvl = new double[numOp];
    tokOp = new int[numOp];      
    tokType = new int[numOp];
    String[] tok = new String[numOp];   //* for each row and side gets renewed
    	
    //* Set tokOp[tk], tokType[tk], tok[tk]
    strFind = "[*/+-]";
    pattern = Pattern.compile(strFind); 
    matcher = pattern.matcher(cmdExpression);
    int tk = 0;
    int y_OpPrev = 0;
    int tokOpTmp = 0;
    tokOp[0] = 0;  // default "+" for first tokOp of each side
    
    /* 
     * Now go through each token and set type, etc.
     */
    while (matcher.find()) {
      if(matcher.group().equals("+"))		
        tokOpTmp = 0;   
      else if(matcher.group().equals("-"))
    	tokOpTmp = 1;  
      else if(matcher.group().equals("*"))
    	tokOpTmp = 2;  
      else if(matcher.group().equals("/"))
    	tokOpTmp = 3;  
    	  
      if (matcher.start() == 0 && tokOpTmp == 1) {  // starts with -C1...
    	  y_OpPrev = 1;  
      } else {  
    	  tok[tk] = cmdExpression.substring(y_OpPrev,matcher.start());
    	  tok[tk] = tok[tk].trim();
    	  y_OpPrev = matcher.end();
    	  tk++;
      }
      tokOp[tk] = tokOpTmp;
    }  //* while Op tokens exist
    tok[tk] = cmdExpression.substring(y_OpPrev);
	tok[tk] = tok[tk].trim();
	
    for (tk=0;tk<numOp;tk++) {
      //* Set Instr's per token now, not cmd line
      int cmdInstrNum = Strategy.iDependentInstr;  //*first set to default	  
      for (int k=0;k<InstrSpecs.idNames.length;k++) {	
    	String strOverDefaultInstr = InstrSpecs.idNames[k] + ".";	
    	strOverDefaultInstr = strOverDefaultInstr.toLowerCase();
        if (tok[tk].indexOf(strOverDefaultInstr) == 0) {  //*****
    	    cmdInstrNum = k;  
    	    int z = tok[tk].indexOf(strOverDefaultInstr);
    	    tok[tk] = tok[tk].substring(0,z) + 
    	    tok[tk].substring(z+strOverDefaultInstr.length());
    	          
        }
      }
      tokInstr[tk] = Instr.getInstance(cmdInstrNum);       		
      

      //* O, H, L, C, R, or P time       
      int y_T = 0;
      if (tok[tk].matches("c\\d*")) {             //* c, c1
          tokType[tk] = 0;
          tokTimeCol[tk] = tokInstr[tk].clsDyCol;
      } else if (tok[tk].matches("o\\d*")) {      //* o, o2
          tokType[tk] = 0;
          tokTimeCol[tk] = tokInstr[tk].opnDyCol;         
      } else if (tok[tk].matches("r\\d*")) {      //* Range HI-LO r, r2
           tokType[tk] = 2;
      } else if (tok[tk].matches("s\\d*") && AGlobal.BUILD_VER==1) {      //* Range CLS-OPN s, s3
           tokType[tk] = 3;
      } else if (tok[tk].matches("p\\d*@\\d\\d\\d\\d?")) {     //* P1@1100 + 300  	  
           tokType[tk] = 0;
           int y_Ar = tok[tk].indexOf("@");
    	   String strTime = tok[tk].substring(y_Ar+1).trim();
    	   int timeCol = tokInstr[tk].getTimeCol(strTime);
    	   if(timeCol == -1)
    	     throw new ExceptionCmd("Error in command line - time does not exist: " + cmdExpression); 
    	   tokTimeCol[tk] = timeCol;	
    	   tok[tk] = tok[tk].substring(0,y_Ar).trim();
      } else if (tok[tk].matches("\\d*\\.?\\d*|\\.*\\d*")) {   //* 3.14, 3, .75	  
       	  tokType[tk] = 9;
 	      tokfdLvl[tk] = 0;	        
 		  tokfdLvl[tk] = Double.parseDouble(tok[tk]);	    	   
      } else {	    	      	                //* fns: h/l, min/max, mvg, for AGlobal.BUILD_VER=1 stdev 
    	  Strat_Abstract stratX = Strat_Factory.getInstance(tokInstr[tk], tok[tk]);
    	  if (stratX != null) {
    		 tokStrat.put(tk, stratX);
    		 tokType[tk] = 10;
    	  } else {
    		  throw new ExceptionCmd("Error in command - unknown command: " + cmdExpression);
    	  }
               
  	  } //* if tokType options
             
      //* Days back ex: O1  C  C2  C12  P  
      if (tokType[tk] < 9) {
          tokDayBk[tk] = 0;     // Current day - default	
          if (tok[tk].length() > y_T+1) {  // C2 instead of C
	          String strTmp = tok[tk].substring(y_T+1).trim();  // P>1< , C>1<
	          tokDayBk[tk] = Integer.parseInt(strTmp);
          }
      }
          
    } //* for tk loop
	
  }

  
  //* For given i, returns array of b
  public void calc(int iDyBeg) throws Exception{

    for (int t=0; t<tokStrat.size(); t++) {
	  tokStrat.get(t).parseAndCalc(i);
	  if(tokStrat.get(t).maxDysBk > maxDysBk) maxDysBk = tokStrat.get(t).maxDysBk;
    }  
	  
    //* Determine max days back - for indp OR dep instr BUT indexed to dep instr!	
    for (int tk=0; tk<tokType.length; tk++) {		  
      if (InstrDep.idName.equals(tokInstr[tk].idName)) {
	      if(tokDayBk[tk] > maxDysBk) maxDysBk = tokDayBk[tk];	
      } else {   //* find maxDysBk in relation to indp maxdysbk! 	  
          int maxDysBkIndp = tokDayBk[tk];
	      int maxDysBkDep=0;
	      while (InstrDep.prcDate[maxDysBkDep+Strategy.begTstDateIndex].before(tokInstr[tk].prcDate[maxDysBkIndp])) {      
	        maxDysBkDep++;
		    if(maxDysBkDep+Strategy.begTstDateIndex > Strategy.endTstDateIndex) 
		      break; 
	   }
	   if(maxDysBkDep > maxDysBk) maxDysBk = maxDysBkDep;
	  }
    }  //* tk loop for maxDysBk
  
    for (int i=iDyBeg+evtBegDyFwd; i<=Strategy.endTstDateIndex; i++) {
      if (i<Strategy.begTstDateIndex)	break;
      if (i>Strategy.endTstDateIndex)	break;
      for (int j=iDyBeg+evtBegDyFwd; i<=Strategy.endTstDateIndex; i++) {
	    double fdSum=0.0;  // reset for each new i, this is array to be sorted	  
	    int iDayBk = 0;
	    int jTimeCol = 0;
	    int jTimeColBk = 0;
	    int jTimeCol0 = 0;
	    int jTimeCol1 = 0;
		     
        for (int tk=0;tk<tokType.length; tk++) {
          double fdSumTok = 0;
			
	      //* Check if dep var date is same as dep: if not go back as long as enuf indp dates
	      int iw = i; 	    	
	      if (!InstrDep.idName.equals(tokInstr[tk].idName)) {	
	         iw = tokInstr[tk].maxPrcIndex;
	         while( InstrDep.prcDate[i].before(tokInstr[tk].prcDate[iw]) ) 
	           iw--;	    	    	    
	      }
	    	
	      if (tokType[tk] == 0) {          //* O,C,H,L,HI,LO,P@   
		      iDayBk = tokDayBk[tk];
		      iTimeCol = tokTimeCol[tk];
		      fdSumTok = tokInstr[tk].prc[iw-iDayBk][iTimeCol];
	      } else if (tokType[tk] == 1) {   //* b, b1d5m30s
		      iDayBk = tokDayBk[tk];
		      iTimeColBk = tokTimeColBk[tk];
	    	  fdSumTok = tokInstr[tk].prc[iw-iDayBk][j-iTimeCol];
	    } else if (tokType[tk] == 2) {   //* R: HI - LO
			iDayBk = tokDayBk[tk];
			iTimeCol0 = tokInstr[tk].hiDyCol;
			iTimeCol1 = tokInstr[tk].loDyCol;	      
			fdSumTok = tokInstr[tk].prc[iw-iDayBk][iTimeCol0] - tokInstr[tk].prc[iw-iDayBk][iTimeCol1];
	    } else if (tokType[tk] == 3) {   //* S: CLS - OPN
	        iDayBk = tokDayBk[tk];
		    iTimeCol0 = tokInstr[tk].clsDyCol;
		    iTimeCol1 = tokInstr[tk].opnDyCol;
		    fdSumTok = tokInstr[tk].prc[iw-iDayBk][iTimeCol0] - tokInstr[tk].prc[iw-iDayBk][iTimeCol1];
	    } else if (tokType[tk] == 9) {   //* pure number
		    fdSumTok = tokfdLvl[tk];
	    } else if (tokType[tk] == 10) {  //* hi/lo, min/max ONLY for now!
		    fdSumTok=tokStrat.get(tk).calcdExprFn[i];
	    }  //* if tokType 
			       
	    if (tokOp[tk] == 0) {         // + 
		    fdSum += fdSumTok;	
	    } else if (tokOp[tk] == 1) {  // - 
		   fdSum -= fdSumTok;	
	    } else if (tokOp[tk] == 2) {  // *
		   fdSum *= fdSumTok;
	    } else if (tokOp[tk] == 3) {  // /
		   fdSum /= fdSumTok;
	    }  //* if tokOp statement
			 
	  }  //* loop tk
      calcdExprFn[i][j] = fdSum;  
  
    }  //* i loop  
		
  }  //* method exprParseCalc
  
}  


