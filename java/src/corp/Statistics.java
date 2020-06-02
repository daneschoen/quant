package program;

import java.text.SimpleDateFormat;
import java.util.List;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Date;


public class Statistics {	    

  private Session session;  
  private Trades trds;  
  private Instr InstrDep;
  
  private Statistics_Data stats = new Statistics_Data();
  
  
  public Statistics(Session session, Trades trds){ 
	this.session = session;
	this.InstrDep = session.InstrDep;
	this.trds = trds;
  }	  
  
  
  public Statistics_Data calc_ExitMatrix() throws Exception{	
	    
    SimpleDateFormat sdfDtime = new SimpleDateFormat("MM/dd/yyyy HH:mm");
	String strText;
	
	int entryfixed_timecol = session.entryfixed_timecol;
	
	/********************************** 	   
	* Section I: Pre-header - entry, exit conditions, time stamp
	* "Ran at ..."
	**********************************/
	strText = sdfDtime.format(new Date());
	stats.head = "Ran at " + strText + "\n";
	strText = "Calculation results for " + InstrDep.idName +
	      " from " + sdfDtime.format(InstrDep.prcDate[session.begTstDateIndex].getTime()) +
		  " to " + sdfDtime.format(InstrDep.prcDate[session.endTstDateIndex].getTime());
	stats.head += strText + "\n";
	if(session.bl_entry_fixed && session.USERTYPE != 4)
	  stats.head += "Reference time at " + InstrDep.prcTime[entryfixed_timecol] + "\n\n";
	else if(session.bl_entry_fixed && session.USERTYPE == 4)
	  //stats.head += "Reference time at: " + session.entryfixed_str; 	
	  stats.head += "Reference time at: " + session.entryfixed_dyfwd + ", " + InstrDep.prcTime[entryfixed_timecol];
	else if(session.bl_entry_event && session.USERTYPE == 4)
	  stats.head += "Reference time at: " + session.entryevent_str;   
    if(session.username.equals("admin"))
	  stats.head += "\nNumber of trades: " + trds.entry_dyidx.size() + "\n\n";
	
	stats.head += "Entry Conditions:\n";
    for(String[] strCmds: session.arrCmdEntryDy)
      if (strCmds[1] == "not")
        stats.head += "not " + strCmds[0] + "\n";
      else
    	stats.head += strCmds[0] + "\n"; 
    stats.head += "\n";
    
	if(session.bl_postfilter_recprof){ 
      stats.head += session.str_postfilter_recprof;
      stats.head += "\n";
	}
    stats.head += "\n";
    
	    
	/************************************ 	   
	 * Section II: Header of Observations
	 * obs_Hdr: "Y  M  D       W   PLAST  08:20  08:30  08:40  ..."
	 ************************************/
    int dyFwd_f, timeFwdCol_f;    
	stats.obs_Hdr = new String[5+session.fwdDyTimeCol.length];
	stats.obs_Hdr[0] = "Y";
	stats.obs_Hdr[1] = "M";
	stats.obs_Hdr[2] = "D";
	stats.obs_Hdr[3] = " W";
	stats.obs_Hdr[4] = "PLAST";
	for (int f=0; f<session.fwdDyTimeCol.length; f++) {   //* gChgSteps
	  timeFwdCol_f = session.fwdDyTimeCol[f][1];   // just time col's
	  stats.obs_Hdr[f+5] = InstrDep.prcTime[timeFwdCol_f];  
	}
	
    /****************************************************************** 
	 * Section II: Observations - Matrix of price changes from reference time/day/price
	 * obsDts: "2010 11 16  TUE"
	 * obs:                      "1283.25   -0.50    1.50    1.25  ..."
	 ******************************************************************/
	double prc_entry;
	String str=""; 
	    
	stats.obsDt = new String[trds.entry_dyidx.size()][4];
	stats.obsDelta = new double[trds.entry_dyidx.size()][session.fwdDyTimeCol.length+1];  //* +1 for prcRef 
	//for (int i=session.begTstDateIndex+trds.maxDysBk; i<=session.endTstDateIndex; i++) {
	for (int t=0; t<trds.entry_dyidx.size(); t++) {
	    int trd_entry_dyidx = trds.entry_dyidx.get(t);		
	    int trd_entry_timecol = trds.entry_timecol.get(t);
	    stats.obsDt[t][0] = InstrDep.getYear(trd_entry_dyidx);
	    stats.obsDt[t][1] = InstrDep.getMonth(trd_entry_dyidx);
	    stats.obsDt[t][2] = InstrDep.getDay(trd_entry_dyidx);
		switch (InstrDep.getWeekday(trd_entry_dyidx)) {
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
		stats.obsDt[t][3] = str;
		
	    //* Show PLAST entry prc, then price changes from PLAST thruout day
		//prc_entry = InstrDep.prc[trd_entry_dyidx][entryfixed_timecol];    //* "PLAST" - the reference price
		prc_entry = InstrDep.prc[trd_entry_dyidx][trd_entry_timecol];
	    stats.obsDelta[t][0] = prc_entry;
	    
	    //* Now all the deltas from PLAST
	    for (int f=0; f<session.fwdDyTimeCol.length; f++) {
	        dyFwd_f = session.fwdDyTimeCol[f][0];
	    	timeFwdCol_f = session.fwdDyTimeCol[f][1];
	        if((trd_entry_dyidx+dyFwd_f) < InstrDep.prc.length)  //* in case last signal is last data row
	          stats.obsDelta[t][1+f] = InstrDep.prc[trd_entry_dyidx+dyFwd_f][timeFwdCol_f]-prc_entry;
	    }    
	}   //* for trd loop
		
	/**********************************************  
	 * Section III: Stats - by time and couple days
	 **********************************************/
	//*  Header
	if (!session.username.equals("admin")){
		stats.stats_Hdr = new String[11];
		stats.stats_Hdr[0] = "D";
		stats.stats_Hdr[1] = "HOUR";
		stats.stats_Hdr[2] = "N";    
		stats.stats_Hdr[3] = "MAX";
		stats.stats_Hdr[4] = "MIN";  
		stats.stats_Hdr[5] = "MU";
		stats.stats_Hdr[6] = "MUD";
		stats.stats_Hdr[7] = "PPOS";
		stats.stats_Hdr[8] = "SDEV";
		stats.stats_Hdr[9] = "T";
		stats.stats_Hdr[10] = "TDRF";
	} else {
		stats.stats_Hdr = new String[13];
		stats.stats_Hdr[0] = "D";
		stats.stats_Hdr[1] = "HOUR";
		stats.stats_Hdr[2] = "N";    
		stats.stats_Hdr[3] = "MU+";
		stats.stats_Hdr[4] = "MU-";
		stats.stats_Hdr[5] = "MED";
		stats.stats_Hdr[6] = "MU";
		stats.stats_Hdr[7] = "MUD";
		stats.stats_Hdr[8] = "PCT+";
		stats.stats_Hdr[9] = "PCT-";
		stats.stats_Hdr[10] = "SDEV";
		stats.stats_Hdr[11] = "T";
		stats.stats_Hdr[12] = "TDRF";
	}
	    
	/* Reset for each time-day forward and calc (statistics for all trades | given a time forward)
	 * 
	 * D   HOUR     N     MIN     MAX      MU     MUD    PPOS    SDEV         T      TDRF
     * 1  02:30  1819   35.25  -42.75   -0.19   -0.20   44.58    4.30   -183.59   -197.27
	 */	   
	stats.statsDyTime = new String[trds.entry_dyidx.size()][2];            //* "0  09:35"
    stats.chgPrc = new double[trds.entry_dyidx.size()][session.fwdDyTimeCol.length];
    stats.statsMed = new double[session.fwdDyTimeCol.length];
    List<Double> statsMedLst_f;
    int cntPos, cntNeg, cntNon0;    
	stats.statsMu = new double[session.fwdDyTimeCol.length];
	stats.statsMuAdj = new double[session.fwdDyTimeCol.length];
	stats.statsMin = new double[session.fwdDyTimeCol.length];
	stats.statsMax = new double[session.fwdDyTimeCol.length];
	stats.statsMinAvg = new double[session.fwdDyTimeCol.length];
	stats.statsMaxAvg = new double[session.fwdDyTimeCol.length];
	stats.statsPpos = new double[session.fwdDyTimeCol.length];
	stats.statsPctPos = new double[session.fwdDyTimeCol.length];
	stats.statsPctNeg = new double[session.fwdDyTimeCol.length];
	stats.statsVar = new double[session.fwdDyTimeCol.length];
	stats.statsSdev = new double[session.fwdDyTimeCol.length];
	stats.statsT = new double[session.fwdDyTimeCol.length];
	stats.statsTdrf = new double[session.fwdDyTimeCol.length];
	stats.statsDrift = new double[session.fwdDyTimeCol.length]; //* mean of pop: mean of changes to +1 930, etc. everyday, not just signal days
	
	for (int f=0; f<session.fwdDyTimeCol.length; f++) {				
	  int fwdDy_f = session.fwdDyTimeCol[f][0];  	
	  int fwdTimeCol_f = session.fwdDyTimeCol[f][1];
	  
	  statsMedLst_f = new ArrayList<Double>();
	  cntPos=0;
	  cntNeg=0;
	  cntNon0=0;
	  stats.statsMed[f] = 0;		
	  stats.statsMu[f] = 0;
	  stats.statsDrift[f] = 0;
	  stats.statsMuAdj[f] = 0;
	  stats.statsMin[f] =  9999999;
	  stats.statsMax[f] = -9999999;
	  stats.statsMinAvg[f] = 0;
	  stats.statsMaxAvg[f] = 0;
	  stats.statsPpos[f] = 0;
	  stats.statsPctPos[f] = 0;
	  stats.statsPctNeg[f] = 0;
	  stats.statsVar[f] = 0;
	  stats.statsSdev[f] = 0;
	  stats.statsT[f] = 0;
	  stats.statsTdrf[f] = 0;
	  stats.cntN=0;			
	  
      for (int t=0; t<trds.entry_dyidx.size(); t++) {
	    int trd_entry_dyidx = trds.entry_dyidx.get(t);
	    int trd_entry_timecol = trds.entry_timecol.get(t);
	    if(trd_entry_dyidx+fwdDy_f >= InstrDep.prc.length)
	      break;
	    
	    stats.cntN++; 	
		
	    prc_entry = InstrDep.prc[trd_entry_dyidx][trd_entry_timecol];        //* PLAST 
		stats.chgPrc[t][f] = InstrDep.prc[trd_entry_dyidx+fwdDy_f][fwdTimeCol_f] - prc_entry;
		stats.statsMu[f] += stats.chgPrc[t][f];

		statsMedLst_f.add(stats.chgPrc[t][f]);
		
		if(stats.chgPrc[t][f] < stats.statsMin[f]) 
		  stats.statsMin[f] = stats.chgPrc[t][f];  
	    if(stats.chgPrc[t][f] > stats.statsMax[f]) 
	      stats.statsMax[f] = stats.chgPrc[t][f];  
			          
	    if(stats.chgPrc[t][f] > 0) {
	      stats.statsPpos[f]++;
	      stats.statsPctPos[f]++;
	      //statsMuPos_f += diffPrc_f[cntN];
	      stats.statsMaxAvg[f] += stats.chgPrc[t][f];
	      cntPos++;
	      cntNon0++;
	    } else if(stats.chgPrc[t][f] < 0){
		  stats.statsPctNeg[f]++;
	      stats.statsMinAvg[f] += stats.chgPrc[t][f];
	      cntNeg++;
	      cntNon0++;
        }
      	    
	  }

	  
	  //if (stats.cntN == 0){
	  //  stats.statsMu[f] = 0;
	  //	  stats.statsPpos[f] = 0;
	  //}else{
	  stats.statsMu[f] /= (stats.cntN);
	  stats.statsPpos[f] /= stats.cntN;
	  stats.statsPpos[f] *= 100.0;
	  //}
	  
	  if (cntNon0 == 0) {
		  stats.statsPctPos[f] = 0;
		  stats.statsPctNeg[f] = 0;
	  } else {    
		  stats.statsPctPos[f] = (double)cntPos/cntNon0*100.0;
		  stats.statsPctNeg[f] = -(double)cntNeg/cntNon0*100.0;
	  }
	  
	  if(cntPos == 0)
		stats.statsMaxAvg[f] = 0;
	  else	  
		stats.statsMaxAvg[f] = stats.statsMaxAvg[f]/cntPos;  
	  if(cntNeg == 0)
		stats.statsMinAvg[f] = 0;
	  else
		stats.statsMinAvg[f] = stats.statsMinAvg[f]/cntNeg;
	  	
	  //* var_s = 1/(N-1)*Sum(x_i - mu)^2
	  //*       = ( Sum(x^2) - 1/N(Sum_x)^2 ) / (N-1)
	  for(int n=0; n<stats.cntN; n++)
	    stats.statsVar[f] += ((stats.chgPrc[n][f] - stats.statsMu[f])*(stats.chgPrc[n][f] - stats.statsMu[f]));
	  stats.statsVar[f] /= (stats.cntN-1);  //* unbiased
	  stats.statsSdev[f] = Math.sqrt(stats.statsVar[f]);

	  //* MED calculations
	  Collections.sort(statsMedLst_f);
	  int len_lst = statsMedLst_f.size();
	  int k;
	  if (len_lst == 1) {  
		  stats.statsMed[f] = statsMedLst_f.get(0);
	  } else if ((len_lst & 1) == 1) {  //* odd
		  k = len_lst/2;
		  stats.statsMed[f] = statsMedLst_f.get(k);
	  } else {
		  k = len_lst/2;  //* ie 1 2 3 4 5 6
		  stats.statsMed[f] = (statsMedLst_f.get(k-1) + statsMedLst_f.get(k))/2.0;
	  }	  
	  
      //* Stats for population
	  int cntN=0;
	  if (session.USERTYPE != 4){
	      //for (int i=InstrDep.maxDysBk; i<=session.endTstDateIndex-fwdDy;i++) {  // mean of changes to +1 930, etc for EVERY day, not just signal
		  for (int i=InstrDep.maxDysBk; i<=session.endTstDateIndex;i++) {  // mean of changes to +1 930, etc for EVERY day, not just signal
			if(i+fwdDy_f >= InstrDep.prc.length) 
			  break;
			cntN++; 	
			stats.statsDrift[f] += InstrDep.prc[i+fwdDy_f][fwdTimeCol_f] - InstrDep.prc[i][entryfixed_timecol];
	      }
		  stats.statsDrift[f] /= cntN;     //* mean of pop
		  stats.statsMuAdj[f] = stats.statsMu[f] - stats.statsDrift[f];
	  } else if (session.bl_entry_fixed && session.USERTYPE == 4){
		  /***
		   * TODO
		   */
		  for (int i=InstrDep.maxDysBk; i<=session.endTstDateIndex;i++) {  // mean of changes to +1 930, etc for EVERY day, not just signal
			if(i+fwdDy_f >= InstrDep.prc.length) 
			  break;
			cntN++; 	
			stats.statsDrift[f] += InstrDep.prc[i+fwdDy_f][fwdTimeCol_f] - InstrDep.prc[i][0];
	      }
		  stats.statsDrift[f] /= cntN;     //* mean of pop
		  stats.statsMuAdj[f] = stats.statsMu[f] - stats.statsDrift[f];		  
	  }
	  
	  /* T-statistic 
	   * = (sample mean)/(sample standard dev)* sqrt(Numbers of sample observations)*100
	   */
	  stats.statsT[f] = (stats.statsMu[f]/stats.statsSdev[f])*Math.sqrt(stats.cntN)*100;
	  stats.statsTdrf[f] = (stats.statsMuAdj[f]/stats.statsSdev[f])*Math.sqrt(stats.cntN)*100;
  	}	
	
  	return stats;
  }  //* end calcStatsAndDisplay_FixedMin
	  
}
