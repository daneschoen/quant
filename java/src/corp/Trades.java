package program;

import java.util.ArrayList;

class Trades {

  Instr InstrX;
  
  int[] conditionDy;
  int[] intradyMinSucc;
  
  ArrayList<Integer> evtSrchBegDyIdx = new ArrayList<Integer>();
  ArrayList<Integer> evtSrchBegTimeCol = new ArrayList<Integer>();
  ArrayList<Integer> evtSrchEndDyIdx = new ArrayList<Integer>();
  ArrayList<Integer> evtSrchEndTimeCol = new ArrayList<Integer>();
  
  //ArrayList<Integer> entryDyIdx = new ArrayList<Integer>();
  ArrayList<Integer> entry_cond_dyidx = new ArrayList<Integer>();
  ArrayList<Integer> entry_dyidx = new ArrayList<Integer>();
  ArrayList<Integer> entry_dyfwd = new ArrayList<Integer>();
  ArrayList<Integer> entry_timecol = new ArrayList<Integer>();
  ArrayList<Double>  entry_prc = new ArrayList<Double>();
  
  ArrayList<Integer> exit_cond_dyidx = new ArrayList<Integer>();
  ArrayList<Integer> exit_dyidx = new ArrayList<Integer>();
  ArrayList<Integer> exit_dyfwd = new ArrayList<Integer>();
  ArrayList<Integer> exit_timecol = new ArrayList<Integer>();
  ArrayList<Double>  exit_prc = new ArrayList<Double>();
  
  ArrayList<Double> dur = new ArrayList<Double>();
  ArrayList<String> type = new ArrayList<String>();
  /* -1/+1 Exit/Entry Daily
   * -2/+2 Exit/Entry Intrady 
   */

    
  /* 
   * These trades are used for everything: daily, intrady, entry, and exit 
   */
  Trades(int key){
	InstrX = Instr.getInstance(key);  
	
	conditionDy = new int[InstrX.prc.length];	
  }
    
}

