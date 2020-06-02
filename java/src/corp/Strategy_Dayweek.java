package program;

public class Strategy_Dayweek  extends Strategy_Abstract{

  private int arg_dow;
  /* 
   * Day of week: 1-5 
   * 
   */	
  
  Strategy_Dayweek(Instr InstrX, String cmdStatement, Session session) {
	super(InstrX, cmdStatement, session);
  }
  
  
  @Override
  public void parseAndSetConditions() throws Exception{

	String strCmd = cmdStatement.trim();
	strCmd = strCmd.toLowerCase();
    	
	//* DAYWEEK(1...5, 1...5)
	int y_P0 = strCmd.indexOf("(");  	  
	int y_P1 = strCmd.lastIndexOf(")");
	
	strCmd = strCmd.substring(y_P0+1,y_P1);
    strCmd = strCmd.trim();

    int y_C = strCmd.indexOf(",");
    String strTok = strCmd.substring(0,y_C);
    strTok = strTok.trim();
    arg_dow = Integer.parseInt(strTok);

    strTok = "";
    strTok = strCmd.substring(y_C+1);
    strTok = strTok.trim();
  }
  

  public void calc() throws Exception{

	boolean signal = false;		      
	for (int i=InstrX.maxDysBk; i<InstrX.prc.length; i++) {		
  
	  signal = false;
  	  if(InstrX.getWeekday(i) == arg_dow)
		signal = true;  
      
      if(signal)
	    prcSucc[i] = 1;
	  else
	    prcSucc[i] = 0;		    	  
	}  //* for i loop
		
  }  // Method calc
}
