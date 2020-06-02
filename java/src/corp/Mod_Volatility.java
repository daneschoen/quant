package program;

public class Mod_Volatility {
  
  //* These get set from Gui, thus static
	
  //public static boolean blChk_;
  
  public static String cmdstrVolHist_Days = "";
  public static String cmdstrVolHist_Time = "";
  public static int cmdVolHist_Days;
  public static int cmdVolHist_TimeCol;

  public static String cmdstrVolHiLo_Days = "";
  public static int cmdVolHiLo_Days;
  
  private Instr InstrDep; 
  private Strategy_VolHist strategy_volhist;

  
  public Mod_Volatility() {
    InstrDep = Instr.getInstance(Strategy.iDependentInstr);
  }
  
  
  private void chart() throws Exception{
    
    Grapher grapher = new Grapher();
    grapher.titleChart = "Volatility - Historical Vol";
    grapher.series1 = new double[Strategy.endTstDateIndex-Strategy.begTstDateIndex+1];
    for (int i=Strategy.begTstDateIndex; i<=Strategy.endTstDateIndex; i++) {
      grapher.series1[i-Strategy.begTstDateIndex] = strategy_volhist.volHist[i];
    }
    
    grapher.go();
    
  }
  
  
  public void run() throws Exception{
	 
	//* volhist(days, H/L/C/O/P@1100) >= 50.4  
  
    strategy_volhist = new Strategy_VolHist();
    
    strategy_volhist.cmdDays = cmdVolHist_Days;
	strategy_volhist.cmdTimeCol = cmdVolHist_TimeCol;
	strategy_volhist.cmdEql = 1;  //* >=      
	strategy_volhist.cmdVolHist = 0;    	        
       
    strategy_volhist.calc();
  
    chart();
  }  
  
  
}	


