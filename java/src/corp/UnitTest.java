package program;

import java.util.Arrays;

public class UnitTest {

  public Session session;
  Trades trds;
  
  public static void main (String[] args) {
	  
    UnitTest ut = new UnitTest();
    
    String strCmdWindow = "ENTRY:foobar" +
    		" \n " +
    		"hol(0) \n " +
    		"c > c1+ 3.4 \n " +
    		"  c > h1 - 7 \n " +
    		"not o >= o1 \n " +
    		"p@1130 >= p1@0930 \n " +
    		"		 \n " +
    		"cowEXIT: x\n";
    //strCmdWindow = strCmdWindow.trim().toLowerCase();
    String str_scenario = "HiLo(E >= p@Ref + 5, 3, C, day)\nRecprof(2, 1, 1615) < 0";
    try{
      ServerApi.init_app(); 	
      Instr InstrDep = Instr.getInstance(Arrays.asList(InstrSpecs.idNames).indexOf("es".toUpperCase()));
      int x = 3939; //InstrDep.getTimeCol("1615");
      System.out.println(x + " "+ InstrDep.idName + "  " + InstrDep.lastTimeCol + " "+ InstrDep.blImported);
    /*	
      Session session = new Session("es", 
                             "07/04/2010","12/25/2015", "0", "1234", 
                             "1615", strCmdWindow,
                             "SetNumObs(20)\nSetViewTimes(120, 6, 2, 10)\nSetViewStartTime(0000)"
                             );
     
	  //if (str_bl_postscenario_hilo.equals("true")){
	  	  session.bl_postscenario_hilo = true;
	  	  session.str_postscenario = str_scenario;
	  //}  
      ut.session = session;	
	*/
		//Econ EconX = Econ.getInstance(cmdEconNameKey);  
		/*
		ut.setArrayCmd();
		
		String strView_statistics="";
		for(String s[]: session.arrCmdEntryDy)
		  strView_statistics += s[0] + " : " +  s[1] + "<<<";
		System.out.println(strView_statistics);
		
		System.out.println("EXIT=========" + session.arrCmdExitDy.size());
		for(String s[]: session.arrCmdExitDy)
		  System.out.println(s[0] + "$" +  s[1]);
		*/
	
      /*
      PostScenario_Hilo postscenario_Hilo = new PostScenario_Hilo(ut.session, ut.trds);  
	  postscenario_Hilo.parseAndSetConditions();
	  postscenario_Hilo.calc();
	  
	  System.out.println(">" + ut.session.str_postscenario_hilo);	
	  System.out.println(postscenario_Hilo.strView);
	  */
		
		
	} catch (Exception e) {
		//e.printStackTrace();
		System.out.println("ERR>" + e.getMessage());
	} 
  }
  
  
  void setArrayCmd() throws Exception{
	System.out.println(session.strCmdWindow);
	  
	//* Split condition -> entry, exit, dy and intrady:
	int p = session.strCmdWindow.indexOf("exit:");
	if(p <= 0)
	  throw new ExceptionCmd("'ENTER:' and 'EXIT:' clauses must exist at beginning of their respective commands");
	
	String strCmdExit = session.strCmdWindow.substring(p+5).trim(); 
	
	String strCmdEntry = session.strCmdWindow.substring(0,p).trim();
			
	p = session.strCmdWindow.indexOf("enter:");
	if(p < 0)
	  throw new ExceptionCmd("'ENTER:' clause must begin entry conditions");
	
	strCmdEntry = strCmdEntry.substring(p+6).trim(); 
	
	//* Entry 
	for (String strCmdLine : strCmdEntry.split("\n")) {	
	  strCmdLine = strCmdLine.trim().toLowerCase();
	  if (strCmdLine.equals("")) {
		  continue;
	  }	else if (strCmdLine.indexOf("//") == 0) {
		  continue;
	  }	else if (strCmdLine.indexOf("debug") == 0) {
	      session.blDebug=true;
	      continue;
	  } else if (strCmdLine.indexOf("not ") == 0) { 
		  session.arrCmdEntryDy.add(new String[]{strCmdLine.substring(4).trim(),"not","","","","",""});
	  } else {  
		  session.arrCmdEntryDy.add(new String[]{strCmdLine,"","","","","",""});
	  }
    } 
	
	//* Exit 
	for (String strCmdLine : strCmdExit.split("\n")) {	
	  strCmdLine = strCmdLine.trim().toLowerCase();
	  if (strCmdLine.equals("")) {
		  continue;
	  }	else if (strCmdLine.indexOf("//") == 0) {
		  continue;
	  }	else if (strCmdLine.indexOf("debug") == 0) {
	      session.blDebug=true;
	      continue;
	  } else if (strCmdLine.indexOf("not ") == 0) { 
	      session.arrCmdExitDy.add(new String[]{strCmdLine.substring(4).trim(),"not","","","","","",""});
	  } else {       
	      session.arrCmdExitDy.add(new String[]{strCmdLine,"","","","","",""});
	  }
    } 
    
  }    	

}
