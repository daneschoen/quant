package program;

public class Mod_EquityCurve {
  
  public int cmd_exit_timetarget_dyfwd;
  public int cmd_exit_timetarget_timecol;
  public String cmd_str_exit_timetarget;
  
  protected Mod_SysTrade mod_systrade;
  protected Session session;
  protected Instr InstrDep; 
  
  public String strView="";
  
  
  public Mod_EquityCurve(Session session) throws Exception{
	this.session = session;  
    InstrDep = session.InstrDep; 	  
  }
  
  public void set_params() throws Exception{
    //* All the set up fr ServerApi for systrade - for this need to do here 
	mod_systrade = new Mod_SysTrade(session);
	mod_systrade.cmd_bl_exit_timetarget_fix=false;
	mod_systrade.cmd_bl_exit_timetarget_rel=true;
	mod_systrade.cmd_str_exit_timetarget = cmd_str_exit_timetarget;
	mod_systrade.cmd_exit_timetarget_dyfwd = cmd_exit_timetarget_dyfwd;
	mod_systrade.cmd_exit_timetarget_timecol = cmd_exit_timetarget_timecol;
	mod_systrade.cmd_maxopencontract = 1; 
	
    mod_systrade.init();
	  
  }
  
  public void set_run_view() throws Exception{
	set_params();
	mod_systrade.runLongOnly();
	strView = mod_systrade.strView;
  }
 	
}	


