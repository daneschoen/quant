package program;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Date;

public class Strategy {
  ArrayList<Integer> trdCondDyIndex;         //* this gets reset for every run!
  
  ArrayList<Integer> trdEntryDyCondIndex;	 //* Not every cond dy will prod trade!
  ArrayList<Integer> trdEntryDyIndex;
  ArrayList<Integer> trdEntryMinIndex;
  ArrayList<Double> trdEntryPrc;
  
  ArrayList<Integer> trdExitDyIndex;
  ArrayList<Integer> trdExitMinIndex;
  ArrayList<Double> trdExitPrc;
  ArrayList<Integer> trdExitReason;

  public int[] prcSuccess;        //* true or false for each index i, matches dependent instr
  
  public int cntSuccess;

  //* -------------------------------------------------------------------------
  ArrayList<String> arrCmdEntryDy;        // lstCmdsEntryDy //arrCmdsCondition
  ArrayList<String> arrCmdEntryIntrady;   // lstCmdsEntryIntrady  arrCmdsEventIntrady;
  ArrayList<String> arrCmdExitDy;         // lstCmdsExitDy arrCmdsExitDy;
  ArrayList<String> arrCmdExitIntrady;    // lstCmdsExitIntrady  arrCmdsExitIntrady;   
  
  public int begTstDateIndex;
  public int endTstDateIndex;
  public int timeRefCol;          //* ref time of the dependent instr, initially set in Gui
  public int timeRefDyFwd;

  public int MaxChgCols;
  public int[][] chgTimeDayCol;   //* [0:10][1] specifies +1 day, [0:10][2] which column ie 930, etc...
  public int cmdUserViewNumObs;
  
  public String depInstr;
  public int iDependentInstr;
  public int maxDysBk=0;
  
  public boolean blDebug;
  
  private String[] obsHdr;    //*  "Y  M  D   W   PLAST  08:20  08:30  08:40  ..."
  private String[] obsDt;     //*  2009/04/22, WED"
  private double[] obsDelta;  //*  12003,23,11  
  
  
  public Strategy() {  
  }
  

  public void calcStatsAndDisplay_FixedTimeEntry(){	
    Instr InstrDep = Instr.getInstance(iDependentInstr);
    SimpleDateFormat sdfDtime = new SimpleDateFormat("MM/dd/yyyy HH:mm");
    String strText;

    /********************************** 	   
     * Section I: Pre-header - entry, exit conditions, time stamp
     **********************************/
    Gui.jtextArea.setText("");	
	strText = sdfDtime.format(new Date());
	Gui.jtextArea.append("Ran at " + strText + "\n");
    strText = "Calculation results for " + InstrDep.idName +
      " from " + sdfDtime.format(InstrDep.prcDate[begTstDateIndex].getTime()) +
	  " to " + sdfDtime.format(InstrDep.prcDate[endTstDateIndex].getTime());
    Gui.jtextArea.append(strText + "\n");
    strText = "Reference time at " + InstrDep.prcTime[timeRefCol];
    Gui.jtextArea.append(strText + "\n\n");
	Gui.jtextArea.append("Entry Conditions:\n");
	//String strEntryWindow = Gui.jtxt_CmdConditions.getText();
	//Gui.jtextArea.append(strEntryWindow.trim());
    for(String strCmds: arrCmdsCondition)
      Gui.jtextArea.append(strCmds + "\n"); 
	
	Gui.jtextArea.append("\n");
    if(Scenarios.bl_RecProf) 
	  Gui.jtextArea.append(PostFilter_RecProf.strUserCmdLine);
    Gui.jtextArea.append("\n\n");
    
	/************************************ 	   
     * Section II: Header of Observations
     ************************************/
    Gui.jtextArea.append(String.format("%4s","Y"));
	Gui.jtextArea.append(String.format("%3s","M"));
	Gui.jtextArea.append(String.format("%3s","D"));
    Gui.jtextArea.append(String.format("%4s","W"));
    String prec = "%" + (InstrDep.precPrcLblShow + 1) + "s";
    Gui.jtextArea.append(String.format(prec,"PLAST"));  // price of entry - usually corresp to reftime
    prec = "%" + InstrDep.precPrcLblShow + "s";
    
    int dyFwd_f, timeFwdCol_f;
    for (int f=0; f<MaxChgCols; f++) {
  	  timeFwdCol_f = chgTimeDayCol[f][1];   // just time col's
      Gui.jtextArea.append(String.format(prec,InstrDep.prcTime[timeFwdCol_f]));
    }  
	//* "--- ... divider"
	String str = "\n";
	for(int z=0; z<((MaxChgCols+1)*InstrDep.precPrcShow)+17; z++)
	  str = str + "-";	
	Gui.jtextArea.append(str + "\n");
	
	/****************************************************************** 
     * Section II: Observations - Matrix of price changes from reference time/day/price
     ******************************************************************/
    int cntSig=0;
    int cntNumObs=0;
    double prcRefSignal;
    
    cntSuccess = 0;
    cntNumObs = 0;
    
    if(cmdUserViewNumObs == 0)
      cmdUserViewNumObs = Integer.MAX_VALUE;	
    
    for(int i=begTstDateIndex+maxDysBk; i<=endTstDateIndex; i++)		
      if(prcSuccess[i]==1)
        cntSuccess++;  

    int iBegViewNumObs = cntSuccess - cmdUserViewNumObs;  // 100 - 70 = 30 
    for (int i=begTstDateIndex+maxDysBk; i<=endTstDateIndex; i++) {
      if (prcSuccess[i]==1) {
    	cntNumObs++;  
    	if (cntNumObs > iBegViewNumObs) {
    	    //int iTrdMinIndex = trdEntryDyIndex.get(t);
    		int iTrdEntryDyIndex = i;
    		Gui.jtextArea.append(String.format("%4s",InstrDep.getYear(iTrdEntryDyIndex)));
    		Gui.jtextArea.append(String.format("%3s",InstrDep.getMonth(iTrdEntryDyIndex)));
    		Gui.jtextArea.append(String.format("%3s",InstrDep.getDay(iTrdEntryDyIndex)));
			switch (InstrDep.getWeekday(iTrdEntryDyIndex)) {
			  case 0:
				str = "SUN";
				break;
		      case 1:
		        str = "MON";
		        break;
		      case 2:
		        str = "TUE"; 	
		        break;
		      case 3:
		        str = "WED";
		        break;
		      case 4:
		        str = "THU";
		        break;
		      case 5:
		        str = "FRI"; 	
		        break;
		    }
		    Gui.jtextArea.append(String.format("%4s",str));
	
		    //* Show PLAST entry prc, then price changes from PLAST thruout day
		    prcRefSignal = InstrDep.prc[iTrdEntryDyIndex][timeRefCol];    //* "PLAST" - the reference price
		    prec = "%" + (InstrDep.precPrcShow + 1) + "f";
		    Gui.jtextArea.append(String.format(prec,prcRefSignal)); 
		    prec = "%" + InstrDep.precPrcShow + "f";
		    
            for (int f=0; f<MaxChgCols; f++) {
    	      dyFwd_f = chgTimeDayCol[f][0];
    	      timeFwdCol_f = chgTimeDayCol[f][1];
              if ((iTrdEntryDyIndex+dyFwd_f) < InstrDep.prc.length) {  //* in case last signal is last data row
		          Gui.jtextArea.append(String.format(prec,InstrDep.prc[iTrdEntryDyIndex+dyFwd_f][timeFwdCol_f]-prcRefSignal));
		          //Gui.jtextArea.append(String.format(prec,InstrDep.getPrice("day","time","c") - prcRefSignal));
              }
            }
	        Gui.jtextArea.append("\n");  //* goto next signal
    	}   //* if < cmdUserViewNumObs
      }   //* if prcSuccess
      
    }   // * for loop
    Gui.jtextArea.append("\n\n");      
	
    /**********************************************  
     * Section III: Stats - by time and couple days
     **********************************************/
    //*  Header
    prec = "%" + InstrDep.precStatsLblShow + "s";  
    Gui.jtextArea.append(String.format("%3s","D"));
	Gui.jtextArea.append(String.format("%7s","HOUR"));
	Gui.jtextArea.append(String.format("%6s","N"));    
	Gui.jtextArea.append(String.format(prec,"MU+"));
	Gui.jtextArea.append(String.format(prec,"MU-"));
	Gui.jtextArea.append(String.format(prec,"MU"));
	Gui.jtextArea.append(String.format(prec,"MUD"));
	Gui.jtextArea.append(String.format(prec,"MED"));
	Gui.jtextArea.append(String.format(prec,"PCT+"));
	Gui.jtextArea.append(String.format(prec,"PCT-"));
	Gui.jtextArea.append(String.format(prec,"SDEV"));
	prec = "%" + (InstrDep.precStatsLblShow + 2) + "s";
	Gui.jtextArea.append(String.format(prec,"T"));
	Gui.jtextArea.append(String.format(prec,"TDRF"));
	//* "--- ... divider"
	str = "\n";
	for(int z=0; z<(8*InstrDep.precStatsLblShow)+3+7+6+4+2; z++) 
	  str = str + "-";	
	Gui.jtextArea.append(str + "\n");
    
    /* Stats: what is the change from the cls of signal
	 * to the next day 930, 9:40, etc...
	 * each column is for +1 930, etc... 
     */	   
    double[] diffPrc_f; 
	double statsMu_f;
	ArrayList<Double> statsMedLst_f;
	double statsMed_f;
	double statsMin_f;
    double statsMax_f;
    double statsMuPos_f;
	double statsMuNeg_f;    
    double statsPctPos_f;
    double statsPctNeg_f;
    
	double statsSdev_f;
	double statsT_f;
	double statsTdrf_f;
		    
	double statsDrift_f; //* mean of pop: mean of changes to +1 930, etc. everyday, not just signal days
	double statsMuAdj_f;
	double statsVar_f;
		    
	int cntN, cntNnon0, cntPos, cntNeg;
	
	for (int f=0; f<MaxChgCols; f++) {
	  dyFwd_f = chgTimeDayCol[f][0];  	
      timeFwdCol_f = chgTimeDayCol[f][1];
      
      diffPrc_f = new double[cntSuccess]; 		
	  statsMu_f = 0;
	  statsDrift_f = 0;
	  statsMuAdj_f = 0;
	  statsMedLst_f = new ArrayList<Double>();
	  statsMed_f = 0;
	  statsMin_f = 1000000;
	  statsMax_f = -1000000;
	  statsMuPos_f = 0;
	  statsMuNeg_f = 0;
	  statsPctPos_f = 0;
	  statsPctNeg_f = 0;
	  statsVar_f = 0;
	  statsSdev_f = 0;
	  statsT_f = 0;
	  statsTdrf_f = 0;
		      
	  cntN=0; 
	  cntNnon0=0;
	  cntPos=0;
	  cntNeg=0;
	  
	  //for (i=0; i<cntSignals;i++) {
	  for (int i=begTstDateIndex+maxDysBk; i<=endTstDateIndex-dyFwd_f;i++) {				
	    if(prcSuccess[i]==1) { 
	      //continue;
	    
		prcRefSignal = InstrDep.prc[i][timeRefCol];        //* PLAST 
		diffPrc_f[cntN] = InstrDep.prc[i+dyFwd_f][timeFwdCol_f] - prcRefSignal;
		statsMu_f += diffPrc_f[cntN];
		statsMedLst_f.add(diffPrc_f[cntN]);
		    
		if (diffPrc_f[cntN] > 0) {
			statsMuPos_f += diffPrc_f[cntN];
		    cntPos++;
		    cntNnon0++;
		} else if (diffPrc_f[cntN] < 0) {
			statsMuNeg_f += diffPrc_f[cntN];
		    cntNeg++;
		    cntNnon0++;
		}
		    
		if(diffPrc_f[cntN] < statsMin_f) {
		  statsMin_f = diffPrc_f[cntN];
		}  
		if(diffPrc_f[cntN] > statsMax_f) 
		  statsMax_f = diffPrc_f[cntN];
		
		cntN++; 	
	    }
	  }

	  statsMu_f /= cntN;
	  if(cntPos == 0)
		statsMuPos_f = 0;  
	  else	  
	    statsMuPos_f = statsMuPos_f/cntPos;
	  if(cntNeg == 0)
		statsMuNeg_f = 0;
	  else
	    statsMuNeg_f = statsMuNeg_f/cntNeg;
	  
	  //* Med calculations
	  Collections.sort(statsMedLst_f);
	  int lenLst = statsMedLst_f.size();
	  int k;
	  if (lenLst == 1) {  
		  statsMed_f = statsMedLst_f.get(0);
	  } else if ((lenLst & 1) == 1) {  //* odd
		  k = lenLst/2;
		  statsMed_f = statsMedLst_f.get(k);
	  } else {
		  k = lenLst/2;  //* ie 1 2 3 4 5 6
		  statsMed_f = (statsMedLst_f.get(k-1) + statsMedLst_f.get(k))/2.0;
	  }

	  if (cntNnon0 == 0) {
	      statsPctPos_f=0;
	      statsPctNeg_f=-0;
	  } else {    
          statsPctPos_f = (double)cntPos/cntNnon0*100.0;
          statsPctNeg_f = -(double)cntNeg/cntNnon0*100.0;
	  }
	  //* var_s = 1/(N-1)*Sum(x_i - mu)^2
	  //*       = ( N*Sum(x^2) - (Sum_x)^2 ) / N(N-1)
	  for(int i=0; i<cntN; i++)
	    statsVar_f += ((diffPrc_f[i] - statsMu_f)*(diffPrc_f[i] - statsMu_f));
	  statsVar_f /= (cntN-1);  //* unbiased
	  statsSdev_f = Math.sqrt(statsVar_f);
		      
	  //* Stats for population
	  cntN=0;
	  for (int i=begTstDateIndex+maxDysBk; i<=endTstDateIndex-dyFwd_f; i++) {  // mean of changes to +1 930, etc for EVERY day, not just signal				
		statsDrift_f += InstrDep.prc[i+dyFwd_f][timeFwdCol_f]-InstrDep.prc[i][timeRefCol];
		cntN++; 	
	  }
	  statsDrift_f = statsDrift_f/cntN;     //* mean of pop
	  statsMuAdj_f = statsMu_f-statsDrift_f;

	  /* T-statistic 
	   * = (sample mean)/(sample standard dev)* sqrt(Numbers of sample observations)*100
	   */
	  statsT_f = (statsMu_f/statsSdev_f)*Math.sqrt(cntSuccess)*100;
	  statsTdrf_f = (statsMuAdj_f/statsSdev_f)*Math.sqrt(cntSuccess)*100;

	  //* each f is +1 930,...,+2 930, etc
	  prec = "%" + InstrDep.precStatsShow + "f";
	  Gui.jtextArea.append(String.format("%3d",dyFwd_f));
	  Gui.jtextArea.append(String.format("%7s",InstrDep.prcTime[timeFwdCol_f]));
	  Gui.jtextArea.append(String.format("%6d",cntSuccess));
	  Gui.jtextArea.append(String.format(prec,statsMuPos_f));
	  Gui.jtextArea.append(String.format(prec,statsMuNeg_f));
	  Gui.jtextArea.append(String.format(prec,statsMu_f));
	  Gui.jtextArea.append(String.format(prec,statsMuAdj_f));
	  Gui.jtextArea.append(String.format(prec,statsMed_f));
	  Gui.jtextArea.append(String.format(prec,statsPctPos_f));
	  Gui.jtextArea.append(String.format(prec,statsPctNeg_f));
	  Gui.jtextArea.append(String.format(prec,statsSdev_f));
	  prec = "%" + (InstrDep.precStatsShow + 2.0) + "f";
	  Gui.jtextArea.append(String.format(prec,statsT_f));
	  Gui.jtextArea.append(String.format(prec,statsTdrf_f));
	  if (f+1<MaxChgCols && 
		  (chgTimeDayCol[f][0] != chgTimeDayCol[f+1][0]
          || InstrDep.prcTime[timeFwdCol_f].equals("16:15"))) { 
	      Gui.jtextArea.append(str+"\n");
	  } else {  
	      Gui.jtextArea.append("\n");
	  }      

    }  //* g loop
    Gui.jtextArea.append("\n\n");
    
  }  //* end calcStatsAndDisplayFix10Min
  
}
