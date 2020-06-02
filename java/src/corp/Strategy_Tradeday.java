package program;

public class Strategy_Tradeday  extends Strategy_Abstract{

  private int arg_dayOfMonth;
  private int _begLast;
  
  
  Strategy_Tradeday(Instr InstrX, String cmdStatement, Session session) {
	super(InstrX, cmdStatement, session);
  }
  
  @Override	  
  public void parseAndSetConditions() throws Exception{

	//* TRADEDAY(0), TRADEDAY(-1), TRADEDAY(1)
	int y_P0 = cmdStatement.indexOf("(");  	  
	int y_P1 = cmdStatement.lastIndexOf(")");
	
    arg_dayOfMonth = Integer.parseInt(cmdStatement.substring(y_P0+1,y_P1).trim());
	
    if (arg_dayOfMonth > 0) {
    	_begLast = 0;
    } else if (arg_dayOfMonth < 0) {
    	_begLast = 1;
	} else {
		_begLast = 1;
	}
	  
  }
  
  
  @Override
  public void calc() {

	int mth, mth0;
	if (_begLast == 0) {  //* tradeday(1), tradeday(2)
		int tradeDay = 0;
	    mth0 = Integer.parseInt(InstrX.getYear(InstrX.maxDysBk));
	    boolean signal = false;		      		
	    for (int i=InstrX.maxDysBk; i<InstrX.prc.length; i++) {	    	
	      
	      mth = Integer.parseInt(InstrX.getMonth(i));
	      
	      if(mth == mth0)
		    tradeDay++;
	      else 
		    tradeDay=1;
	      
	      mth0 = mth;
		
	      if (tradeDay == arg_dayOfMonth) {
		      signal = true;  
		  } else { signal = false;}
      
          if(signal)   
	        prcSucc[i] = 1;
	      else
	        prcSucc[i] = 0;
	    }  //* for i loop  
	    
	} else {  //* tradeday(-1), tradeday(-2)
		
		int tradeDay = 0;
		mth0 = Integer.parseInt(InstrX.getYear(InstrX.prc.length-1));
	    boolean signal = false;		      	
		for (int i=InstrX.prc.length-1; i>=InstrX.maxDysBk; i--) {		
			mth = Integer.parseInt(InstrX.getMonth(i));
		  
		    if(mth == mth0)
			  tradeDay++;
		    else
			  tradeDay=1;
		    
		    mth0 = mth;
			
		    if(tradeDay == -arg_dayOfMonth)
			  signal = true;  
			else
			  signal = false;
	      
	        if(signal)   
		      prcSucc[i] = 1;
		    else 
		      prcSucc[i] = 0;
		   	
		}  //* for i loop  
		  
	}  
	
  }  // Method calc
}
