package program;

import java.util.ArrayList;
import java.util.Arrays;


class Processor {
  /***
   * ServerApi - controller/dispatcher
   *     |
   *     V
   * Strategy Processor(parser) = ProcessDy + ProcessIntrady
   * Mod_SysTrade  || ...
   *     |
   *     V
   * Statistics + View  ||       
   */
  private Session session;
  //private Statistics statistics;
  private Instr InstrDep;
  
  public Data_Payload data_payload = new Data_Payload();
  public String strView_statistics;
  
  //* Main constructor
  Processor( 
      String strInstrDep, 
	  String strDtBeg, String strDtEnd, String strDtBegIndx, String strDtEndIndx, 
	  String strTimeEnter, 
	  String strCondition,
	  String strViewOptions,
	  String str_scenario,
	  String str_bl_postscenario_hilo,
	  String str_bl_postfilter_recprof,
	  String username
	) throws Exception{
	
	session = new Session(strInstrDep,
	                      strDtBeg, strDtEnd, strDtBegIndx, strDtEndIndx,
	                      strTimeEnter,
	                      strCondition,
	                      strViewOptions,
	                      username
	                      );
	InstrDep = session.InstrDep;
	
	session.bl_postscenario_hilo = false;
	if (str_bl_postscenario_hilo.equals("true")){
	  session.bl_postscenario_hilo = true;
	  session.str_postscenario = str_scenario;
	}  
	session.bl_postfilter_recprof = false;
	if (str_bl_postfilter_recprof.equals("true")){
	  session.bl_postfilter_recprof = true;
	  session.str_postscenario = str_scenario;
	}  
	
	session.blDebug = false;		
  }  
  
  Processor(Session session) throws Exception{ 
	this.session = session;        //* session.init() should already be done - setarraycmd, etc...
	InstrDep = session.InstrDep;   //* convenience - scope
	//* No postfilter's, NO statistics time exit matrix
  }  
  
  public Trades run_entry_dy() throws Exception{  
	  
	Trades trds = new Process_Dy(session).go_enter();  
	
	return trds;	
  }

  
  public Trades run_entry_dy_intrady() throws Exception{  
	
	Trades trds = new Process_Dy(session).go_enter();
	trds = new Process_Intrady(session, trds).go_enter();  
	
	return trds;	
  }
  
  
  public Trades run_exit_dy() throws Exception{
	return new Process_Dy(session).go_exit();    
  }  
  
  public Trades run_exit_dy_intrady() throws Exception{
    Trades trds = new Process_Dy(session).go_exit();
	return new Process_Intrady(session, trds).go_exit();    
  }  
  
  public void run_all() throws Exception{  
	  
	Process_Dy process_dy = new Process_Dy(session);    
	Trades trds = process_dy.go_enter();	
	trds = new Process_Intrady(session, trds).go_enter();  
	
	new SetUserOptions(session).parseAndSetViewForStatistics();
	
	Statistics_Data stats_data = new Statistics(session, trds).calc_ExitMatrix();
	data_payload.stats_data = stats_data;
	
	/* D */
	//strView_statistics = data_payload.stats_data.head;
	/* D
	strView_statistics = session.InstrDep.opnTimeStamp + "   " + session.InstrDep.clsTimeStamp;
	strView_statistics = "\n" + session.InstrDep.getTimeCol(session.InstrDep.opnTimeStamp);
	strView_statistics = "\n" + session.InstrDep.getTimeCol(session.InstrDep.clsTimeStamp);
	*/
	
	View view = new View(session);
	strView_statistics = view.construct_statistics(data_payload.stats_data);
	
    //* Extra scenarios
	if (session.bl_postscenario_hilo) {
	    PostScenario_Hilo postscenario_Hilo = new PostScenario_Hilo(session, trds);  
	    postscenario_Hilo.parseAndSetConditions();
	    postscenario_Hilo.calc();
		//data_payload.hilo_data = postscenario_HiLo;
		strView_statistics += postscenario_Hilo.strView;	
	}	  
	
  }	  //* run all fn

}   //* Parser class

