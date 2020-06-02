package program;


import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;
import java.util.regex.Matcher;


public class ParseUtils2 {
	
  public Instr InstrDep;
  public Instr prefixInstr_Instr;
  public int prefixInstr_y_dot;
  
  public String cmdEql;
  public String[] strSides;
  
  private Session session;
  
  public ParseUtils2(Session session){
	this.session = session;
	InstrDep = session.InstrDep;
  }
  
  
  String[] getArrCmd(String strCmdWindow) throws Exception{
    List<String> lst_cmd = new ArrayList<String>();
    for (String strCmdLine : strCmdWindow.split("\n")) {
        strCmdLine = strCmdLine.trim().toLowerCase();
        if (strCmdLine.equals("")) {
            continue;
        } else if (strCmdLine.indexOf("//") == 0 && session.USERTYPE == 4) {
            continue;
      } else {
        lst_cmd.add(strCmdLine);
      }
    }

    String[] arr_cmd = lst_cmd.toArray(new String[lst_cmd.size()]);    
    //for(int k=0; k<cmdStr.size(); k++)
    //      cmdLines[k] = cmdStr.get(k);
    return arr_cmd;
  }
	

  public void prefixInstr(String strTok) {
	  
	prefixInstr_y_dot = -1;
    int cmdInstrNum = session.InstrDep.key;  //* first set to default
	
    for (int r=0; r<InstrSpecs.idNames.length; r++) {	
	  String strOverDefaultInstr = InstrSpecs.idNames[r] + ".";	
	  strOverDefaultInstr = strOverDefaultInstr.toLowerCase();
      if (strTok.indexOf(strOverDefaultInstr) >= 0) {
	      cmdInstrNum = r;
	      prefixInstr_y_dot = strTok.indexOf(".");
	  }
	}
  
    if (cmdInstrNum == session.InstrDep.key) {
    	prefixInstr_Instr = InstrDep;
    } else {
    	prefixInstr_Instr = Instr.getInstance(cmdInstrNum);
    }
    
  }
  
  
  public void splitSides(String strCmdLine) {  
	/* c <= c1
	 * streak(c<c1) = 3
	 * streak(pivot(c,5,p)=3) = 3
	 * 
	 * 1 = foo((bar)) 
	 * abs(c-c1) > abs(c1-c2)
	 * 5 < abs(c-c1)
	 * abs(c-c1) > 5
	 * 
	 * Note: means cannot have : "(c <= c1)" 
	 */ 
	  
    strCmdLine = strCmdLine.trim().toLowerCase();	
    
    int y_Po=0;
    int y_Sep=-1;
    int y_Eql = 0;
    
    String strFind = "[<=,>=,<,>,=]";
	Pattern pattern; 
	Matcher matcher; 
    pattern =  Pattern.compile(strFind);
	matcher = pattern.matcher(strCmdLine);
	if (matcher.find()) {
		y_Eql = matcher.start();
	}
    
    y_Po = strCmdLine.indexOf("(");
    if (y_Po == -1) {
    	y_Sep = 0;            				//* simplest: c>c1
    } else if (y_Eql < y_Po) {   			//* 5 < foo(c<c1),  5 = foo(c=c1)
    	y_Sep = 0;
    } else {	
    	/*	
         * foo(c-c1) = 5, foo(pivot(c,5,p)) = 3   
    	 * foo(c=c1) = 5, streak(pivot(c,5,p) = 3) = 3
    	 * abs((c-c1)) > abs(((c1-c2)))
    	 * bar(c>c1) <=m(n(c<c1,5),10)
    	 */		           										  							
    	 int y = 0;
    	 int cntPo=0;
         while (strCmdLine.indexOf("(",y) >= 0 &&
    			strCmdLine.indexOf("(",y) < strCmdLine.indexOf(")",y)) {
    	   cntPo++;
    	   y = strCmdLine.indexOf("(",y) + 1;
    	 }
    	 //* now found last "(" on one side
    	 for (int i=0; i < cntPo; i++) {
    	   y = strCmdLine.indexOf(")",y) + 1;
    	 }
    	 y_Sep = y;
    }
    
    int y_Ineq = -1;
	int y_ = 0;
	if (strCmdLine.indexOf(">=", y_Sep) >= 0) {
	    y_Ineq = strCmdLine.indexOf(">=", y_Sep);  
	    y_ = 2;	  
	    cmdEql = ">=";
	} else if (strCmdLine.indexOf(">", y_Sep) >= 0) {
		y_Ineq = strCmdLine.indexOf(">", y_Sep);
		y_ = 1;	  
		cmdEql = ">";
	} else if (strCmdLine.indexOf("<=", y_Sep) >= 0) {
		y_Ineq = strCmdLine.indexOf("<=", y_Sep);
		y_ = 2;	  
		cmdEql = "<=";
	} else if (strCmdLine.indexOf("<", y_Sep) >= 0) {
		y_Ineq = strCmdLine.indexOf("<", y_Sep);
		y_ = 1;	  
		cmdEql = "<";
	} else if (strCmdLine.indexOf("=", y_Sep) >= 0) {
		y_Ineq = strCmdLine.indexOf("=", y_Sep);
		y_ = 1;
		cmdEql = "=";		
	}

	strSides = new String[2];
	strSides[0] = strCmdLine.substring(0,y_Ineq).trim();
	strSides[1] = strCmdLine.substring(y_Ineq+y_).trim();
  }
  

  String parseTok(Instr InstrX, String strTok) throws Exception{
		
    //* first get instrX
	strTok = strTok.trim().toLowerCase();
	Instr tok_Instr = Instr.getInstance(InstrX.key);
	
	int y_InstrDot;
    for (int r=0; r<InstrSpecs.idNames.length; r++) {	
	  String strOverDefaultInstr = InstrSpecs.idNames[r] + ".";	
	  strOverDefaultInstr = strOverDefaultInstr.toLowerCase();
      if (strTok.indexOf(strOverDefaultInstr) == 0) {
	      y_InstrDot = strTok.indexOf(".");
	      strTok = strTok.substring(y_InstrDot+1).trim();
	      tok_Instr = Instr.getInstance(r);
	      break;
	  }
	}
    
    //* get time col
    int dysBk=0;
	int timeCol;    	
	int y_T = -1;
	if (strTok.indexOf("c") == 0) {          // Close
		timeCol = tok_Instr.clsDyCol;
		y_T = 1;
	} else if (strTok.indexOf("o") == 0) {   // Open
		timeCol = tok_Instr.opnDyCol;
		y_T = 1;
	} else if (strTok.indexOf("p") == 0) {   // P1@1100
		y_T = 1;
		int y_Ar = strTok.indexOf("@");
		timeCol = tok_Instr.getTimeCol(strTok.substring(y_Ar+1).trim());
		if(y_Ar == 1)          
		  dysBk = 0;     //* Current day - default
		else 
		  dysBk = Integer.parseInt(strTok.substring(y_T,y_Ar).trim());
    } else {
    	return "";
    }	  
		
    //* Now get dys bk
    if (strTok.indexOf("p") != 0) {   // P1@1100
        if(strTok.length() == 1)
		   dysBk = 0;     //* Current day - default
		 else 
		   dysBk = Integer.parseInt(strTok.substring(y_T).trim());        
    }
  
	return tok_Instr.key + "," + dysBk + "," + timeCol;	
  }	
  
 
  
  public String getDysBkAndTimeCol(Instr InstrX, String strTok) throws Exception{
    /*
	 * For: O, C, R, P - ie just one token
	 * return DaysBk,TimeCol as string 
	 * O1, P1@1100
	 */

	int dysBk=0;
	int timeCol=InstrX.clsDyCol;
	
	//* first get time col
    strTok = strTok.trim().toLowerCase();
	int y_T = -1;
	if (strTok.indexOf("c") == 0) {          // Close
	    timeCol = InstrX.clsDyCol;
	    y_T = 1;
	} else if (strTok.indexOf("o") == 0) {   // Open
	    timeCol = InstrX.opnDyCol;
	    y_T = 1;
	//} else if (strTok.indexOf("h") == 0) {   // HIGH
	//    timeCol = InstrX.hiDyCol;
	//    y_T = 1;	      	     
	} else if (strTok.indexOf("p") == 0 || strTok.indexOf("f") == 0) {   // P1@1100
	   y_T = 1;
	   int y_Ar = strTok.indexOf("@");
	   timeCol = InstrX.getTimeCol(strTok.substring(y_Ar+1).trim());
	   if(y_Ar == 1)          
		 dysBk = 0;     //* Current day - default
	   else 
		 dysBk = Integer.parseInt(strTok.substring(y_T,y_Ar).trim());
    } else { 
    	return -1+"";
    }
	
	//* Now get dys bk OR dys fwd now!
	if (strTok.indexOf("p") != 0 && strTok.indexOf("f") != 0) {   // P1@1100, f0@0930
	    if(strTok.length() == 1)
	      dysBk = 0;     //* Current day - default
	    else 
	      dysBk = Integer.parseInt(strTok.substring(y_T).trim());       
	}   
	
    return dysBk + "," + timeCol;
	
  }	
  
 
  static ArrayList<String> getParams(final String cmdExpression) throws Exception{
		/*
		 * c-c1 = min(mvg(c-c1,14),3) => "mvg(c-c1,14),3"
		 * c-c1 = min(c-c1,3) => "c-c1,3"
		 * c > h1
		 * 
		 * g( min(mvg(c-c1,14),3),14 )
	     * g( m(n(c,12),14), 2, 74 )
	     * g( m(n(c,12),14) )  a mono fn  abc)
	     * g( p@1200,14 )
	     * 
	     * foo(bar(univariate))
	     * 
	     * enter/exit(0, 0100)
	     * event(b > 1900 + 5, range, wait)
	     */
	if((cmdExpression.length() - cmdExpression.replace("(", "").length()) != (cmdExpression.length() - cmdExpression.replace(")", "").length()))
	  throw new ExceptionCmd("Error - Malformed statement: " + cmdExpression);
	
	ArrayList<String> params = new ArrayList<String>(); 
    //params = cmdExpression.split(",");	
    int s_Pleft = cmdExpression.indexOf("("); 
    int s_Pright = cmdExpression.lastIndexOf(")");
    String strInnerArg = cmdExpression.substring(s_Pleft+1, s_Pright).trim().toLowerCase();  
	    
    s_Pright = strInnerArg.lastIndexOf(")");
	if (s_Pright >= 0) { 
		params.add(strInnerArg.substring(0,s_Pright+1).trim());
		strInnerArg = strInnerArg.substring(s_Pright+1);
		strInnerArg = strInnerArg.substring(strInnerArg.indexOf(",")+1);
	}	
	for(String param : strInnerArg.split(","))
	  if(!param.trim().equals(""))
	    params.add(param.trim());      
	return params;
  }  
  
  
}