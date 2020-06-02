package program;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Session {
	
  /* ------------------------------------------------------------------------------
   * Fields for state 
   */
  public Instr InstrDep;
  public int begTstDateIndex;
  public int endTstDateIndex;
  public int begDateIndex;
  public int endDateIndex;
  public boolean bl_entry_fixed=false;
  public boolean bl_entry_event=false;
  public boolean bl_exit_fixed=false;
  public boolean bl_exit_event=false;
  public int entryfixed_timecol;
  public int entryfixed_dyfwd;
  public int exitfixed_timecol;
  public int exitfixed_dyfwd;
  public String entryfixed_str;
  public String entryevent_str;
  public String exitfixed_str;
  public String exitevent_str;
  
  public int evtFrameBegTimeCol;
  public int evtFrameEndTimeCol;
  public int evtSrchBegTimeCol;
  public int evtSrchEndTimeCol;   
  public int evtSrchBegDyFwd;
  public int evtSrchEndDyFwd; 
  
  public String strCmdWindow;
  public String strCmdEntryDyWindow;
  public String strCmdEntryIntradyWindow;
  public String strCmdExitDyWindow;
  public String strCmdExitIntradyWindow;		  
	      
  public List<String[]> arrCmdEntryDy;
  public List<String[]> arrCmdEntryIntrady;
  public List<String[]> arrCmdExitDy;
  public List<String[]> arrCmdExitIntrady;
  public List<String[]> arrCmd_feature_dy;
  
  public String strViewOptionsWindow;
  public int viewNumObs;
  public int viewNumMin;
  public int viewNumHr;
  public int viewNumDy;
  public int viewMinIncr;
  public int viewHideBegTimeCol;
  public int viewHideEndTimeCol;
  public int [][] fwdDyTimeCol;
  
  //* Following are defaults
  public boolean bl_postscenario_hilo=false;
  public boolean bl_postfilter_recprof=false;
  public String str_postscenario_hilo="";
  public String str_postfilter_recprof="";
  public String str_postscenario="";
  
  String username;
  int USERTYPE=0;   //* 4: admin
  
  /* ------------------------------------------------------------------------------
   */
  public boolean blDebug=false;
  
  protected Utils utils;
  
  //// remove this
  String TMPSTUB_ENTER;
  
  //Session(){}  //* also acceptable: protected, {default}
		  
  Session(	  
      String strInstrDep, 
      String strDtBeg, String strDtEnd, String strDtBegIndx, String strDtEndIndx, 
      String strEnterTime, 
      String strCondition,
      String strViewOption,
      String username
    ) throws Exception{
	  
	Instr InstrDep = Instr.getInstance(Arrays.asList(InstrSpecs.idNames).indexOf(strInstrDep.toUpperCase()));  
	
	this.InstrDep = InstrDep;
	this.username = username;
	
	begTstDateIndex = Integer.parseInt(strDtBegIndx);
	endTstDateIndex = Integer.parseInt(strDtEndIndx);
	begDateIndex = begTstDateIndex;
	endDateIndex = endTstDateIndex;
	
	///timeRefCol = InstrDep.getTimeCol(strTimeEnter);
	TMPSTUB_ENTER = "enter(" + strEnterTime +")";
	
	strCmdWindow = strCondition.trim().toLowerCase();
	strViewOptionsWindow = strViewOption.trim().toLowerCase();
		    	
	utils = new Utils();
	
	init();
	
	if(username.equals("admin"))
	  USERTYPE = 4;
	
	/***
	 * remove this when implement event
	 */
	//if (USERTYPE != 4) {
	  bl_entry_fixed = true;
      int[] dyfwd_timecol = getIntradyFixed(TMPSTUB_ENTER);
      entryfixed_dyfwd = dyfwd_timecol[0]; 
      entryfixed_timecol = dyfwd_timecol[1]; //InstrDep.getTimeCol(strEnterTime); 
	//}
	
  }
  
  Session( 
    String strInstrDep, 
    String strDtBeg, String strDtEnd, String strDtBegIndx, String strDtEndIndx,  
    String strEnterTime, 
    String strCondition,
    String username
    ) throws Exception{
		
	this(strInstrDep, 
	     strDtBeg, strDtEnd, strDtBegIndx, strDtEndIndx,
	     strEnterTime,
	     strCondition,
	     "",
	     username);  
  }    
  
  Session( 
      String strInstrDep, 
	  String strDtBeg, String strDtEnd, String strDtBegIndx, String strDtEndIndx,
	  String username
    ) throws Exception{
	
	this(strInstrDep, 
	     strDtBeg, strDtEnd, strDtBegIndx, strDtEndIndx,
	     "00:00",
	     "","",
	     username);
  }     
  
  void init() throws Exception{
	/***
	 * Set variables and settings
	 */
	for (int i=0; i<InstrSpecs.idNames.length; i++) {  
	  Instr InstrX = Instr.getInstance(i);
	  InstrX.maxDysBk = 30;
	  if(i==InstrDep.key)
	    if(InstrX.maxDysBk < begTstDateIndex)
	      InstrX.maxDysBk = begTstDateIndex;
	}       	
	
	if(strCmdWindow.indexOf("entry:") >= 0)
      setArrayCmd();
    
	//* for regression - TODO: ADD INSTR CHECK FOR Y, X's
	if(!strCmdWindow.equals("") && !chkIfImported()) 
	  throw new ExceptionCmd("ERROR - Instrument(s) not imported");	
  }
  
  
  void setArrayCmd() throws Exception{	  
	/*** 
	 * Split features -> into ArrayList: entry, exit, dy and intrady event or fixed
	 */
	
	//* This fn may be run several times in one "run" eg strategy + hilo which runs mod_systrade 
	arrCmdEntryDy  = new ArrayList<String[]>();
	arrCmdEntryIntrady  = new ArrayList<String[]>();
	arrCmdExitDy  = new ArrayList<String[]>();
	arrCmdExitIntrady  = new ArrayList<String[]>();
	
	int pos = strCmdWindow.indexOf("exit:");
	if(pos <= 0)
	  throw new ExceptionCmd("'ENTRY:' and 'EXIT:' clauses must exist at beginning of their respective commands");
	
	String strCmdExit = strCmdWindow.substring(pos+5).trim(); 
	String strCmdEntry = strCmdWindow.substring(0,pos).trim();
			
	pos = strCmdWindow.indexOf("entry:");
	if(pos < 0)
	  throw new ExceptionCmd("'ENTRY:' clause must begin entry conditions");
	
	strCmdEntry = strCmdEntry.substring(pos+6).trim(); 
	
	int[] dyfwd_timecol;
	//* Entry 
	for (String str_cmdline : strCmdEntry.split("\n")) {	
	  str_cmdline = str_cmdline.trim().toLowerCase();
	  if (str_cmdline.equals("")) {
		  continue;
	  }	else if (str_cmdline.indexOf("//") == 0 && USERTYPE == 4) {
		  continue;
	  }	else if (str_cmdline.indexOf("debug") == 0 && USERTYPE == 4) {
	      blDebug=true;
	  }	else if (str_cmdline.indexOf("enter(") == 0 && USERTYPE == 4) {
		  bl_entry_fixed = true;
	      dyfwd_timecol = getIntradyFixed(str_cmdline);
	      entryfixed_dyfwd = dyfwd_timecol[0]; 
	      entryfixed_timecol = dyfwd_timecol[1];
	      entryfixed_str = str_cmdline;
	  }	else if (str_cmdline.indexOf("event(") == 0) {
	  	  bl_entry_event = true;
	  	  entryevent_str = str_cmdline;
	      //parseIntradyEvent();	      	      	      
	  } else if (str_cmdline.indexOf("not ") == 0) { 
		  arrCmdEntryDy.add(new String[]{str_cmdline.substring(4).trim(),"not","","","","",""});
	  } else {  
		  arrCmdEntryDy.add(new String[]{str_cmdline,"","","","","",""});
	  }
    }
	/***
	if (USERTYPE != 4) { 
	  bl_entry_fixed = true;
      dyfwd_timecol = getIntradyFixed(TMPSTUB_ENTER);
      entryfixed_dyfwd = dyfwd_timecol[0]; 
      entryfixed_timecol = InstrDep.getTimeCol(strEnterTime); //dyfwd_timecol[1];
	}
	*/
	//* Exit 
	for (String str_cmdline : strCmdExit.split("\n")) {	
	  str_cmdline = str_cmdline.trim().toLowerCase();
	  if (str_cmdline.equals("")) {
		  continue;
	  }	else if (str_cmdline.indexOf("//") == 0 && USERTYPE == 4) {
		  continue;
	  }	else if (str_cmdline.indexOf("debug") == 0 && USERTYPE == 4) {
	      blDebug=true;
	  }	else if (str_cmdline.indexOf("exit(") == 0) {
		  bl_exit_fixed = true;
	      dyfwd_timecol = getIntradyFixed(str_cmdline);
	      exitfixed_dyfwd = dyfwd_timecol[0]; 
	      exitfixed_timecol = dyfwd_timecol[1];
	      exitfixed_str = str_cmdline;
	  }	else if (str_cmdline.indexOf("event(") == 0 && USERTYPE == 4) {
	  	  bl_exit_event = true;
	  	  exitevent_str = str_cmdline;
	      ///parseIntradyEvent();	      	      
	  } else if (str_cmdline.indexOf("not ") == 0) { 
	      arrCmdExitDy.add(new String[]{str_cmdline.substring(4).trim(),"not","","","","","",""});
	  } else {       
	      arrCmdExitDy.add(new String[]{str_cmdline,"","","","","",""});
	  }
    } 

  }    	
  
  int[] getIntradyFixed(final String str_cmdline) throws Exception{
	/*** 
	 * Returns int [dyfwd, timecol]  
	 */
	   
	int[] param = new int[2];
	param[0] = 0;
    try {
      //ArrayList<String> dyfwd_timestr = new ArrayList<String>();
	  ArrayList<String> res = ParseUtils2.getParams(str_cmdline);
      if (res.size() < 1 || res.size() > 2){
        throw new ExceptionCmd("ERROR - Malformed enter/exit - requires parameters (DAY, TIME) : " + str_cmdline);
      } else if(res.size() == 1){	
	    param[1] = InstrDep.getTimeCol(res.get(0));
      } else if(res.size() == 2){	
        param[0] = Integer.parseInt(res.get(0));
        param[1] = InstrDep.getTimeCol(res.get(1));
      } 
      return param;
      
	} catch(Exception e){
		
	  if(e.getClass().equals(ExceptionCmd.class))   //* obj instanceof MyClass
	    throw new ExceptionCmd(e.getMessage());  
	  throw new ExceptionCmd("ERROR - Malformed enter/exit command: " + str_cmdline);
	}

  }

  
  boolean chkIfImported() {
	boolean blChk = false;
  	if (strCmdWindow.length() == 0) {
  	    //throw ("ERROR: No commands inputed\n");	
    } else if (!InstrDep.blImported) {  //* Chk dependent imported first, then independent
        // throw ("ERROR: Dependent instrument not imported \n");
    } else if (!utils.checkIfAllImported(strCmdWindow)) {   	  
        //throw ("ERROR: Independent instruments not imported \n");
    } else {
    	blChk = true;
    }
  	return blChk;
  }
  
}
