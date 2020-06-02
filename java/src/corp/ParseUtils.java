package program;

import java.util.regex.Pattern;
import java.util.regex.Matcher;


public class ParseUtils {
	
  public int splitSides_cmdEql;
  public String[] splitSides_strSides = new String[2];

  public Instr InstrDep;
  public Instr prefixInstr_Instr;
  public int prefixInstr_y_dot;
  
  public Instr ohlc_Instr;
  public String ohlc_Type;
  public int ohlc_TimeCol;
  public int ohlc_DaysBk;
  public double ohlc_fdLvl=0;
  
  public int featureCalc_maxDysBk;
  public double[] featureCalc_feature;
  
  private Utils utils;
  private Session session;
  
  public ParseUtils(Session session){
	utils = new Utils();
	this.session = session;
	InstrDep = session.InstrDep;
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
	  
    strCmdLine = strCmdLine.trim();
    strCmdLine = strCmdLine.toLowerCase();	
  
    int y_Ineq = -1;
	int y_ = -1;
	if (strCmdLine.lastIndexOf(">=") >= 0) {
	    y_Ineq = strCmdLine.lastIndexOf(">=");  
	    y_ = 2;	  
	    splitSides_cmdEql = 1;
	} else if (strCmdLine.lastIndexOf(">") >= 0) {
		y_Ineq = strCmdLine.lastIndexOf(">");
		y_ = 1;	  
		splitSides_cmdEql = 0;
	} else if (strCmdLine.lastIndexOf("<=") >= 0) {
		y_Ineq = strCmdLine.lastIndexOf("<=");
		y_ = 2;	  
		splitSides_cmdEql = 3;
	} else if (strCmdLine.lastIndexOf("<") >= 0) {
		y_Ineq = strCmdLine.lastIndexOf("<");
		y_ = 1;	  
		splitSides_cmdEql = 2;
	} else if (strCmdLine.lastIndexOf("=") >= 0) {
		y_Ineq = strCmdLine.lastIndexOf("=");
		y_ = 1;	  
		splitSides_cmdEql = 4;		
	}

	splitSides_strSides[0] = strCmdLine.substring(0,y_Ineq);
	splitSides_strSides[0] = splitSides_strSides[0].trim();
	splitSides_strSides[1] = strCmdLine.substring(y_Ineq+y_);
	splitSides_strSides[1] = splitSides_strSides[1].trim();
  }
  
  //* only used by vix ...
  public void OHLC(String strTok) {
    /*
     * For: O, H, L, C, R, P or Lvl(V) - ie just one token
     * return TimeCol, DaysBk or Lvl
     * US.O1, H2, L, P1@1100
     *
     */

	 strTok = strTok.trim();
	 strTok = strTok.toLowerCase();	
	 String strTmp;
	 
	 ParseUtils parse = new ParseUtils(session);
	 parse.prefixInstr(strTok);
	 ohlc_Instr = parse.prefixInstr_Instr;
	 int y_dot = parse.prefixInstr_y_dot;
	 if(y_dot >= 0)
	   strTok = strTok.substring(y_dot+1); 
 
     String strFind = "[ohlcrsp]";
     Pattern pattern = Pattern.compile(strFind); 
	 Matcher matcher = pattern.matcher(strTok); 	      
	 if (matcher.find()) {          
         int y_T = -1;
         if (strTok.indexOf("c") >= 0) {          // Close
        	 ohlc_Type = "c";	
             y_T = strTok.indexOf("c");
             ohlc_TimeCol = ohlc_Instr.clsDyCol;
         } else if (strTok.indexOf("o") >= 0) {   // Open
       	      ohlc_Type = "o";	
              y_T = strTok.indexOf("o");
              ohlc_TimeCol = ohlc_Instr.opnDyCol;            
         } else if (strTok.indexOf("h") >= 0) {   // HIGH
      	     ohlc_Type = "h";	
             y_T = strTok.indexOf("h");
             ohlc_TimeCol = ohlc_Instr.hiDyCol;
         } else if (strTok.indexOf("l") >= 0) {   // LOW
      	     ohlc_Type = "l";	
             y_T = strTok.indexOf("l");
             ohlc_TimeCol = ohlc_Instr.loDyCol;
         } else if (strTok.indexOf("r") >= 0) {   // Range HI-LO
      	     ohlc_Type = "r";	
             y_T = strTok.indexOf("r");
         } else if (strTok.indexOf("s") >= 0) {   // Range CLS-OPN
      	     ohlc_Type = "s";	
             y_T = strTok.indexOf("s");
         } else if (strTok.indexOf("p") >= 0) {   // P1@1100
      	     ohlc_Type = "p";	
             y_T = strTok.indexOf("p");
             int y_Ar = strTok.indexOf("@");
             int y_EndTime = y_Ar+1;
             boolean blMoreNum = true;
	         while (y_EndTime < strTok.length() && blMoreNum) {
                try {
                  y_EndTime++;	
                  //int x = Integer.parseInt(tok[tk].substring(y_At+1, y_EndTime));
                } catch(NumberFormatException nfe) {
    	          blMoreNum = false;
                }
	          }
	          String strTime = strTok.substring(y_Ar+1,y_EndTime);
	          ohlc_TimeCol = utils.strTimeToCol(strTime, ohlc_Instr);
	          strTok = strTok.substring(y_T,y_Ar).trim();
        }  //* if else "p"
        
        //* Now for any O,C,H,L,R,S,P : Days back
        ohlc_DaysBk = 0;     //* Current day - default	
        if (strTok.length() > y_T+1) {  // C2 instead of C
          strTmp = strTok.substring(y_T+1).trim();  // P>1< , C>1<
          ohlc_DaysBk = Integer.parseInt(strTmp);
        }
    
      } else {  //* matcher did not find O,H,L... - so last possibility: level + or -       
          ohlc_fdLvl = Double.parseDouble(strTok);
    	  ohlc_Type = "v";
      
	  } //* if all the else tokType options

  }  //* method OHLC  
  
}  
