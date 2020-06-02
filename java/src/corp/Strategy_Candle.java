package program;


public class Strategy_Candle extends Strategy_Abstract{

  public static final String CMD = "candle";	
  
  private double cmdOpn_Bot;
  private double cmdOpn_Top;
  private double cmdCls_Bot;
  private double cmdCls_Top;
  private int cmdDaysBk=0;
  private Instr cmdInstr;                    
  
  public void parseAndSetConditions(String strCmdLine) throws Exception{
		    
    /*
     * candle_DaysBk(Opn_Bot, Opn_Top, Cls_Bot, Cls_Top)	 
	 * candle(10, 30, 90, 100)
	 * candle_2(10, 30, 90, 100)	  
	 */ 
		
	//* Here we go 
	strCmdLine = strCmdLine.trim();
	strCmdLine = strCmdLine.toLowerCase();
	String strTmp="";
	
	//* Get cmdInstr
	ParseUtils2 parse = new ParseUtils2();
	parse.prefixInstr(strCmdLine);
	cmdInstr = parse.prefixInstr_Instr;
    if (parse.prefixInstr_y_dot >= 0) {
    	strCmdLine = strCmdLine.substring(parse.prefixInstr_y_dot+1);
    }
	
	//* 1) Get cmdDaysBk
	int y_Po = strCmdLine.indexOf("("); 
	int y_Pc = strCmdLine.indexOf(")");
	
	int y_DaysBk = strCmdLine.indexOf(CMD + "_");
	if (y_DaysBk >= 0) {	
		strTmp = strCmdLine.substring(CMD.length()+1,y_Po);	
		cmdDaysBk = Integer.parseInt(strTmp);	
	}
	
	strCmdLine = strCmdLine.substring(y_Po+1, y_Pc);
	strCmdLine = strCmdLine.trim();
    //* 2) "Opn_Bot, Opn_Top, Cls_Bot, Cls_Top"
	
	int y_C = strCmdLine.indexOf(",");
	strTmp = strCmdLine.substring(0,y_C);
	strTmp = strTmp.trim();
	cmdOpn_Bot = Double.parseDouble(strTmp);
	
	strCmdLine = strCmdLine.substring(y_C+1);
	strCmdLine = strCmdLine.trim();
	//* 2) "Opn_Top, Cls_Bot, Cls_Top"
	
	y_C = strCmdLine.indexOf(",");
	strTmp = strCmdLine.substring(0,y_C);
	strTmp = strTmp.trim();
	cmdOpn_Top = Double.parseDouble(strTmp);
	
	strCmdLine = strCmdLine.substring(y_C+1);
	strCmdLine = strCmdLine.trim();
	//* 3) "Cls_Bot, Cls_Top"
	
	y_C = strCmdLine.indexOf(",");
	strTmp = strCmdLine.substring(0,y_C);
	strTmp = strTmp.trim();
	cmdCls_Bot = Double.parseDouble(strTmp);
	
	strCmdLine = strCmdLine.substring(y_C+1);
	strCmdLine = strCmdLine.trim();
	//* 4) "Cls_Top"
	
	
	strTmp = strCmdLine;
	strTmp = strTmp.trim();
	cmdCls_Top = Double.parseDouble(strTmp);	
			
  }	

  
  public void calc() throws Exception{
   /*
    * candle(Opn_Bot, Opn_Top, Cls_Bot, Cls_Top)	 
	* candle(10, 30, 90, 100)	  
    */	
	  
	prcSucc = new int[InstrDep.prc.length];
	boolean blSignal = false;
	int opnDyCol = cmdInstr.opnDyCol;
	int clsDyCol = cmdInstr.clsDyCol;
	int hiDyCol = cmdInstr.hi24Col;
	int loDyCol = cmdInstr.lo24Col;
	double range;
	
	for (int i=Strategy.begTstDateIndex+cmdDaysBk; i<=Strategy.endTstDateIndex; i++) {
	
	  blSignal = false;
      range = cmdInstr.prc[i-cmdDaysBk][hiDyCol] - cmdInstr.prc[i-cmdDaysBk][loDyCol];
	  
	  if (cmdInstr.prc[i-cmdDaysBk][opnDyCol] >= cmdInstr.prc[i-cmdDaysBk][loDyCol] + ((cmdOpn_Bot/100.0)*range) &&
	      cmdInstr.prc[i-cmdDaysBk][opnDyCol] <= cmdInstr.prc[i-cmdDaysBk][loDyCol] + ((cmdOpn_Top/100.0)*range) &&	  
	      cmdInstr.prc[i-cmdDaysBk][clsDyCol] >= cmdInstr.prc[i-cmdDaysBk][loDyCol] + ((cmdCls_Bot/100.0)*range) &&
	      cmdInstr.prc[i-cmdDaysBk][clsDyCol] <= cmdInstr.prc[i-cmdDaysBk][loDyCol] + ((cmdCls_Top/100.0)*range)) {
		  blSignal = true;
	  } 
	  
	  System.out.println(cmdInstr.prc[i-cmdDaysBk][0] + " " +
			  cmdInstr.prc[i-cmdDaysBk][1] + " " +
			  cmdInstr.prc[i-cmdDaysBk][2] + " " +
			  cmdInstr.prc[i-cmdDaysBk][opnDyCol] + " " + 
			  cmdInstr.prc[i-cmdDaysBk][hiDyCol] + " " +  
			  cmdInstr.prc[i-cmdDaysBk][loDyCol] + " " + 
			  cmdInstr.prc[i-cmdDaysBk][clsDyCol]);
			  
	  
      if (nested == 0) {
  	      if (blSignal) {   
  	          ParserCondition.prcSucc[i] = 1;
  	      } else {
  	 	      ParserCondition.prcSucc[i] = 0;
  	      }			
  	  } else if (nested == 1) {
  		  if (blSignal) {   
  		      prcSucc[i] = 1;
  		} else {
  		      prcSucc[i] = 0;
  	    }							
  	  }
	  
    }  //* for i loop  

	System.out.println(">"+cmdDaysBk);	  
  }  //* end method calc()		
	
}

