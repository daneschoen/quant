package program;

import java.util.Hashtable;
import java.text.SimpleDateFormat;
import java.util.Date;

public class Mod_CondProb {
  
  //* These get set from Gui, thus static	
  public static String strWindowPosterior = "";
  public static String strWindowConditional = "";

  public double[] plUnreal;
  public double[] plUnrealCum;
  public double[] plReal;
  public double[] plRealCum;
  public double[] plTrades;
  
  public int error=0;
  
  private int cntTot=0;  
  private int cntSuccConditional=0;
  private int cntSuccPosterior=0;
  private int[] prcSuccConditional;   
  private int[] prcSuccPosterior;
  
  private Instr InstrDep; 
  private Utils utils;
  
  
  public Mod_CondProb() {
    InstrDep = Instr.getInstance(Strategy.iDependentInstr);
    utils = new Utils();
  }
  
  
  public void run() throws Exception{
	calc();
	//displayObservations();    
	calcStatsAndDisplay();
  }
 
    
  private void displayHeader() {
	//* First general info and header
    Gui.jtextArea.setText("");
    Gui.jtextArea.append("Systematic Trade Testing\n");
	SimpleDateFormat sdf = new SimpleDateFormat("MM/dd/yyyy HH:mm:ss");
	String strText = sdf.format(new Date());
	Gui.jtextArea.append("Ran at " + strText + "\n");
	strText = "Calculation results for " + InstrDep.idName + " from " +
		       Integer.toString((int)InstrDep.prices[Strategy.begTstDateIndex][InstrDep.mthCol]) + "/" + 
			   Integer.toString((int)InstrDep.prices[Strategy.begTstDateIndex][InstrDep.dayCol]) + "/" +
			   Integer.toString((int)InstrDep.prices[Strategy.begTstDateIndex][InstrDep.yrCol]) + 
					  " to " +
			   Integer.toString((int)InstrDep.prices[Strategy.endTstDateIndex][InstrDep.mthCol]) + "/" +
			   Integer.toString((int)InstrDep.prices[Strategy.endTstDateIndex][InstrDep.dayCol]) + "/" +
			   Integer.toString((int)InstrDep.prices[Strategy.endTstDateIndex][InstrDep.yrCol]);  
	Gui.jtextArea.append(strText + "\n");
	strText = "Reference time at " + InstrDep.hdr[Strategy.timeRefCol];
	Gui.jtextArea.append(strText + "\n\n");
	    
	Gui.jtextArea.append("Entry Conditions:\n");
	Gui.jtextArea.append(strWindowPosterior);
	Gui.jtextArea.append("\n\n");
	  
  }
  
  
  private void displayObservations() {
     
  }  //* method: display observations 
  
  
  private void calcStatsAndDisplay() {
	double prConditional;
	double prPosterior;
	  
    double totPl = 0;
	double avgPl = 0;  //* totPts/trade
	double stdev = 0;
	double sharpRatio;
	double sharpT = 0;
	
	/*
	 *   Pr(A|B) = Pr(AB)/Pr(B)
	 */ 

	int maxDaysFwd=0;    
    int numWinningTrades=0;
    int numLosingTrades=0;
    int consecWinningTrades=0;
    int consecLosingTrades=0;
    int cntWinStreak=0;
    int cntLoseStreak=0;
    int localMaxWinStreak=0;
    int localMaxLoseStreak=0;
    boolean blWinConsec=false;
    boolean blLoseConsec=false;
    
    plReal = new double[InstrDep.maxPrcIndex+1];     
    plUnreal = new double[InstrDep.maxPrcIndex+1];  
    plRealCum = new double[InstrDep.maxPrcIndex+1];
    plUnrealCum = new double[InstrDep.maxPrcIndex+1];
    for (int i=Strategy.begTstDateIndex; i<=Strategy.endTstDateIndex-maxDaysFwd; i++) {
    	
      	 
    }  //* for i beg and end test dates
    
    
    prConditional = (double)cntSuccConditional/(double)cntTot;
    prPosterior = (double)cntSuccPosterior/(double)cntSuccConditional;

    Gui.jtxt_CondProb.append("Total Count              : ");
    Gui.jtxt_CondProb.append(String.format("%8d\n", cntTot));    
    Gui.jtxt_CondProb.append("Conditional Count        : ");
    Gui.jtxt_CondProb.append(String.format("%8d\n", cntSuccConditional));    
    Gui.jtxt_CondProb.append("Conditional Probability  : ");
    Gui.jtxt_CondProb.append(String.format("%8.2f\n", prConditional));
    Gui.jtxt_CondProb.append("Posterior Count          : ");
    Gui.jtxt_CondProb.append(String.format("%8d\n", cntSuccPosterior));    
    Gui.jtxt_CondProb.append("Posterior Probability    : ");
    Gui.jtxt_CondProb.append(String.format("%8.2f\n\n", prPosterior));

    
  }  //* method: display stats
  
  
  public void calc() throws Exception{

    if (strWindowPosterior.length() == 0) {
        Gui.jtxt_CondProb.append("ERROR: No Posterior Conditions \n");
        // later just display the formatted raw data
	    //* Chk dependent imported first, then independent	
    } else if (!InstrDep.blImported) {
 	    Gui.jtxt_CondProb.append("ERROR: Dependent instrument not imported \n");
    } else if (!utils.checkIfAllImported(strWindowPosterior)) {   	  
        Gui.jtxt_CondProb.append("ERROR: Independent instruments not imported \n");
    } else if (!utils.checkIfAllImported(strWindowConditional)) {   	  
        Gui.jtxt_CondProb.append("ERROR: Independent instruments not imported \n");        
    } else { 	  
 	
    //* Pr(A|B) = Pr(AB)/Pr(B)	
    prcSuccConditional = new int[InstrDep.maxPrcIndex+1];  //* from Exit window
    prcSuccPosterior = new int[InstrDep.maxPrcIndex+1];   //* from Entry window

    Parser parser;
	//* Start off with Conditional of course   
    if (strWindowConditional.length() == 0) {  //* no conditional
        for (int i=Strategy.begTstDateIndex; i<=Strategy.endTstDateIndex; i++) {	
      	  cntSuccConditional++;
          prcSuccConditional[i] = 1;
        }    	
    } else { 	
        parser = new Parser();
        parser.blDontOutputParser = true;
        parser.parseAllStrategies(strWindowConditional); 
        for (int i=Strategy.begTstDateIndex; i<=Strategy.endTstDateIndex; i++) {	
          if (Strategy.prcSuccess[i]==1) {    //* need to cp since gets reset in Parser for each run
    	      cntSuccConditional++;
              prcSuccConditional[i] = 1;
          }
        }
    }
    
    //* Posterior - of course dependent on Conditional
    parser = new Parser();
    parser.blDontOutputParser = true;
    parser.parseAllStrategies(strWindowPosterior);  
    for (int i=Strategy.begTstDateIndex; i<=Strategy.endTstDateIndex; i++) {
      cntTot++;		
      if (Strategy.prcSuccess[i]==1 && prcSuccConditional[i]==1) {   //* need to cp since gets reset in Parser for each run
    	  cntSuccPosterior++;
          prcSuccPosterior[i] = 1;
      }
    }
     
    }  //* if no pre-errors
  }  //* calc method
	
}	

