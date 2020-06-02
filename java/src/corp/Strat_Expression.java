package program;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Pattern;
import java.util.regex.Matcher;


class Strat_Expression extends Strat_Abstract{
  
  protected String[] tok;	
  protected Instr[] tokInstr;
  protected int[] tokType;      //* 0: O,C,H,L,P   2:R   3:S   5:Lvl 
  protected int[] tokDayBk;
  protected int[] tokTimeCol;
  protected double[] tokfdLvl;
  protected String[] tokOp;
  protected Map<Integer, Strat_Abstract> tokStrat = new HashMap<Integer, Strat_Abstract>();	
    

  Strat_Expression(final Instr InstrX, final String cmdExpression, Session session) {
	super(InstrX, cmdExpression, session);
  }

  
  @Override
  public void parseAndSetConditions() throws Exception{
    /*
      c > us.c1	  
      "c" < "c1 - 10 / 2" 
	  "c2" < MIN("c3",5) + m(n()) * q()                
	  "p1@1100" > MAX("p1@1100", 10) 
	  min("C-C1", 15) - 10 + mvg("o-o1") > "c - c1 - 10"
	  foo(bar(C-C1, 15),28) - 10 + mvg(o-o1)
	*/       		 
	ArrayList <Integer> listOperPosition = new ArrayList<Integer>();
	ArrayList <String> listOper = new ArrayList<String>();
	int cntOpenParan=0;
	for (int p=0; p<cmdExpression.length(); p++) {
	    String symbol = cmdExpression.substring(p,p+1);  
	    if (symbol.equals("(")) {
	        cntOpenParan++;
	    } else if (symbol.equals(")")) {
	    	cntOpenParan--;
	    } else if (cntOpenParan == 0) {  //* only now can separate the operands
	    	if (p==0) {  //* only -,+ allowed
	    	    if (symbol.equals("+") || symbol.equals("-")) {
	    		   listOper.add(symbol);
	    		   listOperPosition.add(p);
	    	    } else {  // have to add +
	    		   listOper.add("+"); 
	    		   listOperPosition.add(-1);
	    	    }
	    	 } else {
	    	     if (symbol.matches("[*/+-]")) {
		    		 listOper.add(symbol);
		    		 listOperPosition.add(p);	    		 
	    	     }
	    	 }
	     }	
	}
	tokInstr = new Instr[listOper.size()];
	tokDayBk = new int[listOper.size()];	
	tokTimeCol = new int[listOper.size()];
	tokfdLvl = new double[listOper.size()];
	tokOp = new String[listOper.size()];      
	tokType = new int[listOper.size()];
	tok = new String[listOper.size()];   //* for each row and side gets renewed

	//* Now separate into operands ie tok
	if (listOperPosition.size()==0) {
	    //* ???
	} else {      
		int p=0;
	    for (p=0; p<listOperPosition.size()-1; p++) {  
	        tok[p] = cmdExpression.substring(listOperPosition.get(p)+1, listOperPosition.get(p+1)).trim();
	        tokOp[p] = listOper.get(p);
	    }
	    //* Now last one
	    tok[p] = cmdExpression.substring(listOperPosition.get(p)+1).trim();
	    tokOp[p] = listOper.get(p);
    } 
	
    for (int tk=0; tk<tok.length; tk++) {
      String[] instr_tok = getSplitInstr(InstrX, tok[tk]);
      tokInstr[tk] = Instr.getInstance(Integer.valueOf(instr_tok[0]));
      tok[tk] = instr_tok[1];      
      
      int y_T = 0;
      if (tok[tk].matches("c\\d*")) {             //* c, c1
          tokType[tk] = 0;
          tokTimeCol[tk] = tokInstr[tk].clsDyCol;
      } else if (tok[tk].matches("o\\d*")) {      //* o, o2
          tokType[tk] = 0;
          tokTimeCol[tk] = tokInstr[tk].opnDyCol;         
      } else if (tok[tk].matches("r\\d*")) {      //* Range HI-LO r, r2
          tokType[tk] = 2;
      } else if (tok[tk].matches("s\\d*") && session.USERTYPE == 4) {   //* Range CLS-OPN s, s3
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
      } else {
    	  //* If not the basic, c,o,p@ then goes to factory for all other functions:
    	  Strat_Abstract stratX = Strat_Factory.getInstance(tokInstr[tk], tok[tk], session);	
    	  if (stratX != null) {
    		 tokStrat.put(tk, stratX);
    		 tokType[tk] = 10;
    	  } else {
    		 throw new ExceptionCmd("Error in command - unknown command: " + cmdExpression);
    	  }
               
  	  } //* if tokType options
             
      //* Days back ex: O1  C  C2  C12  P
      tokDayBk[tk] = 0;
      if (tokType[tk] < 9) {	
          if (tok[tk].length() > y_T+1) {  // C2 instead of C
	          String strTmp = tok[tk].substring(y_T+1).trim();  // P>1< , C>1<
	          tokDayBk[tk] = Integer.parseInt(strTmp);
          }
      }
          
    } //* for tk loop
	
  }

  
  @Override
  public void calc() throws Exception{
    /* 
     * "c1 + h2" > "c3 + 0.90"
     * 
     * us.c1 > bn.c1/1000
     * us.c/es.c > 2.5
     * 
     * "C>C1 OR C1>C2"  <=  WAIT(C>C1 OR C1>C2) > 3 
     *
     * c + mvg(us.c,14) > us.c
     * us.c > us.mvg(us.c, 14)
     * us.c > us.mvg(c, 14)           X no sense
     * us.c > mvg(us.c2, 14)          X needs us.mvg
     * us.foo(us.bar(us.c, 21), 7)
     * 
     * streak(std(us.c - us.c1,14) > 3) = 3 
     * us.streak(std(c - c1,14) > 3) = 3
     * us.c = max(us.c5,5)
     *   
     * c>c1  <=  or(C>C1, C1>C2)  <=  WAIT(or(C>C1, C1>C2)) > 3 
     * 
     * dep          indp
     * 06/01/2000   06/01/2004     
     * 
     * 06/01/2004   06/01/2000
     * 
     * 06/14/2010   06/14/2010
     * 06/15/2010   06/14/2010
     * 06/16/2010   06/16/2010
     * 
     * 07/01/1997   
     * 09/01/2003   09/01/2003
     * 
     * 07/01/1997   
     * 09/02/2003   09/01/2003
     * 09/02/2003   09/02/2003
     *   
     *              07/01/2000  
     * 09/01/2003   09/01/2003
     *    
     *      es     us
     * 1/1   -     119 
     * 1/2  1023    -  119
     * 1/3  1021   121        us.c - us.c1
     * 1/4  1022    -  121    us.c - us.c1
     * 1/5   -     130 
     * 1/6 
     */
    
    for (int tk=0; tk<tokType.length; tk++) {		  
      //D System.out.println(InstrX.key + "   tokInstr[t].key: " + tokInstr[tk].key + "   tok[t]: " + tok[tk]);		
  	  if (tokType[tk] <= 9) {
          if(tokInstr[tk].maxDysBk <  tokDayBk[tk])
            tokInstr[tk].maxDysBk = tokDayBk[tk];	
            //System.out.println("   tokKey: "+ tokInstr[t].key + "   tokInstr[t].maxDysBk:" + tokInstr[t].maxDysBk + "   tokDayBk: "+ tokDayBk[t]);          
      } else {   //* find maxDysBk in relation to indp maxdysbk! 	  
	      tokStrat.get(tk).parseAndCalc();
          //System.out.println("   tokKey: "+ tokInstr[t].key + "   tokInstr[t].maxDysBk:" + tokInstr[t].maxDysBk + "   tokStrat.maxDysBk: "+ tokStrat.get(t).InstrX.maxDysBk);	  
      }
  	  
	  /* Determine max days back - for indp OR dep instr BUT indexed to dep instr!
	   *                         - for dep instr relative to indep instruments
	   * c > us.c1
	   * us.c1 > us.c2
	   * c > us.mvg(us.c, 5)
	   */
	  if (tokInstr[tk].key != InstrX.key) {
	      while(InstrX.prcDate[InstrX.maxDysBk].before(tokInstr[tk].prcDate[tokInstr[tk].maxDysBk]) &&
	        InstrX.maxDysBk < InstrX.prcDate.length - 1) 
	          InstrX.maxDysBk++;
	  }
	  
    }  //* tk loop for maxDysBk
    
    int dayBk;
    int jTimeCol;
    int jTimeCol0;
    int jTimeCol1;
    int i_indp;
    //for (int i=session.InstrDep.maxDysBk; i<session.InstrDep.prc.length; i++) {
    for (int i=InstrX.maxDysBk; i<InstrX.prc.length; i++) {	
      
 	  double fdSum_i=0.0;  // reset for each new i, this is array to be sorted	  
      for (int t=0; t<tokType.length; t++) {		    
        double fdSumTok = 0;  //* reset for each TOK, as well as each i
	    /* es           us
        * 11/09/2009   11/09/2009  X
        * 11/10/2009   11/10/2009  us.c < us.c1
        * 11/11/2009               X              shouldn't include this !
        * 11/12/2009   11/12/2009  X
        * 
        * ---------------------
        * 11/09        11/09  X
        *              11/10  us.c < us.c1
        * 11/12                                   should include this !      
        * 11/13        11/13
        * 
        * ---------------------
        * 11/08        
        *              11/09  us.c > us.c1
        *              11/10  us.c > us.c1
        * 11/12                                   should include this !
        * 11/13        11/13           
        */	  
        i_indp = i;	
        if (InstrX.key != tokInstr[t].key) {	       
           //D System.out.println(InstrX.key + " != " + tokInstr[t].key);
	       i_indp = tokInstr[t].prc.length-1;
	       while(i_indp >= tokInstr[t].maxDysBk &&
	    	 tokInstr[t].prcDate[i_indp].after(InstrX.prcDate[i])) 
	           i_indp--;	    
	       if(i_indp < tokInstr[t].maxDysBk)
		     continue;	   	       
	       if(!InstrX.prcDate[i].equals(tokInstr[t].prcDate[i_indp]) &&
	           InstrX.prcDate[i-1].equals(tokInstr[t].prcDate[i_indp]) &&
	           i > InstrX.maxDysBk)
	         continue;
	    }
	    	
	    if (tokType[t] == 0) {          //* O,C,H,L,HI,LO,P@   
		    dayBk = tokDayBk[t];
		    jTimeCol = tokTimeCol[t];
		    fdSumTok = tokInstr[t].prc[i_indp-dayBk][jTimeCol];
	    } else if (tokType[t] == 2) {   //* R: HI - LO
			dayBk = tokDayBk[t];
			jTimeCol0 = tokInstr[t].hiDyCol;
			jTimeCol1 = tokInstr[t].loDyCol;	      
			fdSumTok = tokInstr[t].prc[i_indp-dayBk][jTimeCol0] - tokInstr[t].prc[i_indp-dayBk][jTimeCol1];
	    } else if (tokType[t] == 3) {   //* S: CLS - OPN
	        dayBk = tokDayBk[t];
		    jTimeCol0 = tokInstr[t].clsDyCol;
		    jTimeCol1 = tokInstr[t].opnDyCol;
		    fdSumTok = tokInstr[t].prc[i_indp-dayBk][jTimeCol0] - tokInstr[t].prc[i_indp-dayBk][jTimeCol1];
	    } else if (tokType[t] == 9) {   //* pure number
		    fdSumTok = tokfdLvl[t];
	    } else if (tokType[t] == 10) {  //* the functions eg, us.mvg(us.c)
		    fdSumTok=tokStrat.get(t).calcdExprFn[i_indp];
	    }  
			       
	    if (tokOp[t].equals("+")) {         // +a - b / 10
		    fdSum_i += fdSumTok;	
	    } else if (tokOp[t].equals("-")) {  
		    fdSum_i -= fdSumTok;	
	    } else if (tokOp[t].equals("*")) { 
		    fdSum_i *= fdSumTok;
	    } else if (tokOp[t].equals("/")) { 
		    fdSum_i /= fdSumTok;
	    }  //* if tokOp statement
			 
	  }  //* loop t
      calcdExprFn[i] = fdSum_i;  
      //System.out.println("=>"+fdSum);      
 
    }  //* i loop  
		
 }  //* method exprParseCalc
 
}  

