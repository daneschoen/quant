package program;


public abstract class Process_Abstract {

  //Strategy_Cmd[] cmd;
  //String[] cmdLine;	
  //int[] cmdLineNot;		  	
  //String[] cmdIntradyLine;	
  //int[] cmdIntradyLineNot;
  
  //protected Utils utils;
  protected ParseUtils2 parseUtils;
    
  //public static int[] prcSucc;
  //protected String strCmdWindow;
  protected Session session;
  protected Instr InstrDep;
  protected Trades trds;	

  
  Process_Abstract(Session session){  
    this.session = session;
	InstrDep = session.InstrDep;
	trds = new Trades(InstrDep.key);
	
	//parseUtils = new ParseUtils2(session);
	//utils = new Utils();  
  }

  /* 0) Check if imported 
   * 1) Compose array of cmd objects
   * 2) runStrategies: 
   *    for (i=0+start; i< es.length(); i++)
   *      if day is false:
   *        break;
   *      for each cmd 
   *        if prc_i is false:
   *          break;
   *        add latest time  
   * 3)    
   * 
   */
  
  abstract Trades go_enter() throws Exception;
  
  abstract Trades go_exit() throws Exception;
    
  //* this should be overriden depending on daily or intraday multiple entries
  abstract void parseAndCalcStrategies() throws Exception; 
	
}

