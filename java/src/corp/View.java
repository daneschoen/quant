package program;


public class View {

  /* 0: Console
   * 1: Swing
   * 2: Browser_jQuery
   * 3: Browser_JSF
   * 4: Android
   * 5: iOS
   */
  protected String obs_csv="";
  protected String msg="";
  
  protected Session session;
  protected Instr InstrDep;

  public View(Session session){
    this.session = session; 
    InstrDep = session.InstrDep;
  }

  /*
  public abstract void displayMsg();
  public abstract void displayMsg(String msg);
  public abstract void constructMsg(String msg);
  */
  
  public String construct_statistics(Statistics_Data stats) {      

    /* 1) heading
     * 2) obs hdr
     * 3) obs
     * 3) stats hdr
     * 4) stats
     */
	 //* String head, String[] obsHdr, int[][] obsYMDW, double[][] obsDelta, int begViewObs, String[] statsHdr, String[][] statsDyHr, double[][] stats, String...varPost)
	 String strView_statistics = stats.head;
	 obs_csv = stats.head;
	 
	 strView_statistics += getObservations(stats);   
	 if (session.username.equals("admin")){
		 strView_statistics += getStatsReport_admin(stats);
	 } else {
	     strView_statistics += getStatsReport(stats);
	 }    
	 return strView_statistics;
  }
  
  private String getObservations(Statistics_Data stats) {
	
	StringBuilder strb = new StringBuilder();  
	
	//* Obs header  
	strb.append(String.format("%4s", "Y"));
	strb.append(String.format("%3s", "M"));
	strb.append(String.format("%3s", "D"));
	strb.append(String.format("%4s", "W"));
	String prec = "%" + (InstrDep.precPrcLblShow + 1) + "s";
	strb.append(String.format(prec, "PLAST"));  
	
	obs_csv += "BEGINOBS-HEADER:\n";
	obs_csv += "Y,M,D,W,PLAST";
	
	//* header - times
	prec = "%" + InstrDep.precPrcLblShow + "s";    
	for (int g=5; g<stats.obs_Hdr.length; g++) {  
	  strb.append(String.format(prec, stats.obs_Hdr[g]));
	  obs_csv += "," + stats.obs_Hdr[g];
	}  
	obs_csv += "\n";
	
	//* "--- ... divider"
	String div = "\n";
	for(int z=0; z<((stats.obs_Hdr.length+1)*InstrDep.precPrcShow)+10; z++) 
	  div += "-";	
	strb.append(div + "\n");
	
	//* Now the obs
	int begObsView = stats.obsDelta.length - session.viewNumObs;  // 85 - 10 = 75
	if(session.viewNumObs == 0 || begObsView <= 0)
	  begObsView = 0;	
    for (int t=begObsView; t<stats.obsDelta.length; t++) {

      //* Y M D W  
      strb.append(String.format("%4s",stats.obsDt[t][0]));
      strb.append(String.format("%3s",stats.obsDt[t][1]));
      strb.append(String.format("%3s",stats.obsDt[t][2]));
      strb.append(String.format("%4s",stats.obsDt[t][3]));
	  
	  //* Show PLAST entry prc, then price changes from PLAST thruout day(s)
	  prec = "%" + (InstrDep.precPrcShow + 1) + "f";
	  strb.append(String.format(prec,stats.obsDelta[t][0])); 	  

	  //* Now the deltas from PLAST
	  prec = "%" + InstrDep.precPrcShow + "f";
	  for(int j=1; j<stats.obsDelta[t].length; j++)
	    strb.append(String.format(prec,stats.obsDelta[t][j]));
	  strb.append("\n");	  
    }   // * for loop
    strb.append("\n\n"); 
    
    //* Text file
    //if (session.USERTYPE == 0) {
      for (int t=0; t<stats.obsDelta.length; t++) {
        //* Y M D W	
        obs_csv += stats.obsDt[t][0] + "," + stats.obsDt[t][1] + "," + stats.obsDt[t][2] + "," + stats.obsDt[t][3];
      
  	    //* PLAST: entry prc
        obs_csv += "," + stats.obsDelta[t][0]; 	  

  	    //* Now the deltas from PLAST
  	    for(int j=1; j<stats.obsDelta[t].length; j++)
  		  obs_csv += "," + stats.obsDelta[t][j];
  	    obs_csv += "\n";	  
      }   // * for loop
    
      Utils_IO.outputData(session, obs_csv);
    //}
    
    return strb.toString();
  }
  
  
  private String getStatsReport(Statistics_Data stats) {
	StringBuilder strb = new StringBuilder();
	
    //*  Header
	String prec = "%" + InstrDep.precStatsLblShow + "s";
	
	strb.append(String.format("%3s", stats.stats_Hdr[0]));    //* "D"
	strb.append(String.format("%7s", stats.stats_Hdr[1]));    //* "HOUR"));
	strb.append(String.format("%6s", stats.stats_Hdr[2]));    //* "N"));    
	strb.append(String.format(prec, stats.stats_Hdr[3]));     //* "MAX"));
	strb.append(String.format(prec, stats.stats_Hdr[4]));     //* "MIN"));  
	strb.append(String.format(prec, stats.stats_Hdr[5]));     //* "MU"));
	strb.append(String.format(prec, stats.stats_Hdr[6]));     //* "MUD"));
	strb.append(String.format(prec, stats.stats_Hdr[7]));     //* "PPOS"));
	strb.append(String.format(prec, stats.stats_Hdr[8]));     //* "SDEV"));
	prec = "%" + (InstrDep.precStatsLblShow + 2) + "s";
	strb.append(String.format(prec,"T"));
	strb.append(String.format(prec,"TDRF"));
	
	//* "--- ... divider"	
	String div = "\n";
	for(int z=0; z<(8*InstrDep.precStatsLblShow)+3+7+6+4+2; z++) 
	  div += "-";	
	strb.append(div + "\n");
	  
	/* D   HOUR     N     MIN     MAX      MU     MUD    PPOS    SDEV         T      TDRF
     * 1  02:30  1819   35.25  -42.75   -0.19   -0.20   44.58    4.30   -183.59   -197.27
	 */	   	
	for (int f=0; f<session.fwdDyTimeCol.length; f++) {
      /* each f is +1 930,...,+2 1615, etc. 
	   * hide 1615 ~ 0230     
	   */
	  int fwdDy = session.fwdDyTimeCol[f][0];  	
	  int fwdTimeCol = session.fwdDyTimeCol[f][1];
	  
	  if (fwdTimeCol < session.viewHideBegTimeCol &&
		  fwdTimeCol > session.viewHideEndTimeCol) {  
		  prec = "%" + InstrDep.precStatsShow + "f";
		  strb.append(String.format("%3d",fwdDy));
		  strb.append(String.format("%7s",InstrDep.prcTime[fwdTimeCol]));
		  strb.append(String.format("%6d",stats.cntN));
		  strb.append(String.format(prec,stats.statsMax[f]));
		  strb.append(String.format(prec,stats.statsMin[f]));
		  strb.append(String.format(prec,stats.statsMu[f]));
		  strb.append(String.format(prec,stats.statsMuAdj[f]));
		  strb.append(String.format(prec,stats.statsPpos[f]));
		  strb.append(String.format(prec,stats.statsSdev[f]));
		  prec = "%" + (InstrDep.precStatsShow +2.0) + "f";
		  strb.append(String.format(prec,stats.statsT[f]));
		  strb.append(String.format(prec,stats.statsTdrf[f]));
		  if (f+1<session.fwdDyTimeCol.length && session.fwdDyTimeCol[f][0] != session.fwdDyTimeCol[f+1][0]) { 
		      strb.append(div+"\n");
		  } else {  
			  strb.append("\n");
		  }      
	  }  //* fwd loop
	}
	
	strb.append("\n\n");
	return strb.toString();
  }        
  
  
  private String getStatsReport_admin(Statistics_Data stats) {
	StringBuilder strb = new StringBuilder();
	
    //*  Header
	String prec = "%" + InstrDep.precStatsLblShow + "s";
	
	strb.append(String.format("%3s", stats.stats_Hdr[0]));    //* "D"
	strb.append(String.format("%7s", stats.stats_Hdr[1]));    //* "HOUR"));
	strb.append(String.format("%6s", stats.stats_Hdr[2]));    //* "N"));    
	strb.append(String.format(prec, stats.stats_Hdr[3]));     //* "MU+"));
	strb.append(String.format(prec, stats.stats_Hdr[4]));     //* "MU-"));
	strb.append(String.format(prec, stats.stats_Hdr[5]));     //* "MED"));
	strb.append(String.format(prec, stats.stats_Hdr[6]));     //* "MU"));
	strb.append(String.format(prec, stats.stats_Hdr[7]));     //* "MUD"));
	strb.append(String.format(prec, stats.stats_Hdr[8]));     //* "PCT+"));
	strb.append(String.format(prec, stats.stats_Hdr[9]));     //* "PCT-"));
	strb.append(String.format(prec, stats.stats_Hdr[10]));    //* "SDEV"));
	prec = "%" + (InstrDep.precStatsLblShow + 2) + "s";
	strb.append(String.format(prec,"T"));
	strb.append(String.format(prec,"TDRF"));
	
	//* "--- ... divider"	
	String div = "\n";
	for(int z=0; z<(10*InstrDep.precStatsLblShow)+3+7+6+4+2; z++) 
	  div += "-";	
	strb.append(div + "\n");
	  
	for (int f=0; f<session.fwdDyTimeCol.length; f++) {
    /* each f is +1 930,...,+2 1615, etc. 
	   * hide 1615 ~ 0230     
	   */
	  int fwdDy = session.fwdDyTimeCol[f][0];  	
	  int fwdTimeCol = session.fwdDyTimeCol[f][1];
	  
	  if (fwdTimeCol < session.viewHideBegTimeCol &&
		  fwdTimeCol > session.viewHideEndTimeCol) {  
		  prec = "%" + InstrDep.precStatsShow + "f";
		  strb.append(String.format("%3d",fwdDy));
		  strb.append(String.format("%7s",InstrDep.prcTime[fwdTimeCol]));
		  strb.append(String.format("%6d",stats.cntN));
		  strb.append(String.format(prec,stats.statsMaxAvg[f]));
		  strb.append(String.format(prec,stats.statsMinAvg[f]));
		  strb.append(String.format(prec,stats.statsMed[f]));
		  strb.append(String.format(prec,stats.statsMu[f]));
		  strb.append(String.format(prec,stats.statsMuAdj[f]));
		  strb.append(String.format(prec,stats.statsPctNeg[f]));
		  strb.append(String.format(prec,stats.statsPctPos[f]));
		  strb.append(String.format(prec,stats.statsSdev[f]));
		  prec = "%" + (InstrDep.precStatsShow +2.0) + "f";
		  strb.append(String.format(prec,stats.statsT[f]));
		  strb.append(String.format(prec,stats.statsTdrf[f]));
		  if (f+1<session.fwdDyTimeCol.length && session.fwdDyTimeCol[f][0] != session.fwdDyTimeCol[f+1][0]) { 
		      strb.append(div+"\n");
		  } else {  
			  strb.append("\n");
		  }      
	  }  //* fwd loop
	}
	
	strb.append("\n\n");
	return strb.toString();
  }        

}
