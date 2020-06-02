package program;

import java.util.ArrayList;
import java.util.Arrays;
import java.text.SimpleDateFormat;
import java.util.Date;


public class Mod_SysTrade {
  
  public int cmd_maxopencontract;	
  public boolean cmd_bl_exit_feature_fixed=false;
  public boolean cmd_bl_exit_feature_event=false;  //* ENTRY/EXIT: event(b > p@1015) vs enter(0,1015)
  public String cmd_exit_feature_fixed_timestr;
  public int cmd_exit_feature_fixed_dyfwd;
  public int cmd_exit_feature_fixed_timecol;
  public boolean cmd_bl_exit_profittarget_p=false;	
  public boolean cmd_bl_exit_profittarget_z=false;
  public double cmd_fd_exit_profittarget_p;
  public double cmd_fd_exit_profittarget_z;  
  public boolean cmd_bl_exit_stoploss_p=false;	
  public boolean cmd_bl_exit_stoploss_z=false;
  public double cmd_fd_exit_stoploss_p;
  public double cmd_fd_exit_stoploss_z;  
  
  /* remove this! */
  public boolean cmd_bl_exit_timetarget_fix=false;
  public boolean cmd_bl_exit_timetarget_rel=false;
  public String cmd_str_exit_timetarget;
  public int cmd_exit_timetarget_dyfwd;
  public int cmd_exit_timetarget_timecol;
    
  public double[] plUnreal;
  public double[] plUnrealCum;
  public double[] plUnrealCum_long;
  public double[] plUnrealCum_short;
  public double[] plReal;
  public double[] plRealCum;
  public double[] plTrades;
  
  public ArrayList<Double[]> trades;
  public final int TRADEDETAILS_MAX=10;
  public int totTrades;
  
  public Trades trds_entry;
  public Trades trds_exit;
  
  private boolean blBuy;
    
  //* Stats
  private double avgPosIntraMinTrade;
  private double avgNegIntraMinTrade;

  public double totPl;
  public double avgPl;
  public double stdev;
  public double sharpT;
  public double ppos;
  public double maxTrade;
  public double minTrade;
  public double avgWinTrades;
  public double avgLoseTrades;
  public double medWinTrades;
  public double medLoseTrades;  
  public double stdIntraTrade;
  public double avgIntraTrade;
  public double maxIntradayTradesPl;
  public double minIntradayTradesPl;
  public double avgPosIntraTrade;
  public double avgNegIntraTrade;
  public double pctNegTimeSpentIntraday;
  public int    maxConsecWinTrades;
  public int    maxConsecLoseTrades;
  public double avgConsecWinTrades;
  public double avgConsecLoseTrades;
  public double avgHoldDur;
  public double maxHoldDur;
  public double minHoldDur;
  public double ptsPerDayHeld;
  public double maxDrawDn;
  public double maxDrawUp;
  public double avgDrawDn;
  public double maxIntraDrawDn;   //* intra-trade unrealized
  public double avgIntraDrawDn;        
  
  public double avgIntraDrawUp;
  public double ratioAvgIntraDrawDn;
 
  public double longestNbrTradesDrawDn; 
  public double longestDaysDrawDn; 
  public double avgNbrTradesDrawDn;
  public double avgDaysDrawDn;
  public double ratioAvgDaysDrawDn;
  
  public int cntDrawDn;
  public double avgDrawUp;
  public int cntDrawUp;
  public double maxMarginPerMini;
  
  int evtStopBegFrameTimeCol, evtStopEndFrameTimeCol; 
  int evtStopBegTimeCol, evtStopEndTimeCol;
  int evtStopBegDyFwd, evtStopEndDyFwd;  
  int evtStopStdPeriod;
  
  int evtProfitBegFrameTimeCol, evtProfitEndFrameTimeCol; 
  int evtProfitBegTimeCol, evtProfitEndTimeCol;
  int evtProfitBegDyFwd, evtProfitEndDyFwd;  
  int evtProfitStdPeriod;
  
  int evtFrameBeg_TimeCol, evtFrameEnd_TimeCol; 
  int evtSrchBeg_TimeCol, evtSrchEnd_TimeCol;
  int evtSrchBeg_DyFwd, evtSrchEnd_DyFwd;  
    
  protected Session session;
  protected Instr InstrDep; 
  
  public String strView="";
  
  
  public Mod_SysTrade(Session session) {
	this.session = session;  
    InstrDep = session.InstrDep;
  }
  
  public void init() throws Exception{
    	  
    evtProfitBegFrameTimeCol = InstrDep.firstTimeCol;
	evtProfitEndFrameTimeCol = InstrDep.lastTimeCol;
	evtProfitBegDyFwd = 0;
	evtProfitEndDyFwd = 999999999;
	evtProfitBegTimeCol = session.entryfixed_timecol+1;  
	evtProfitEndTimeCol = InstrDep.lastTimeCol;  	
	evtProfitStdPeriod = 40;
	if(InstrDep.maxDysBk < evtProfitStdPeriod+1) 
	  InstrDep.maxDysBk = evtProfitStdPeriod+1;

	evtStopBegFrameTimeCol = InstrDep.firstTimeCol;
	evtStopEndFrameTimeCol = InstrDep.lastTimeCol;
	evtStopBegDyFwd = 0;
	evtStopEndDyFwd = 999999999;
	evtStopBegTimeCol = session.entryfixed_timecol + 1; 
	evtStopEndTimeCol = session.InstrDep.lastTimeCol;  
	evtStopStdPeriod = 40;
	if(InstrDep.maxDysBk < evtStopStdPeriod+1) 
	  InstrDep.maxDysBk = evtStopStdPeriod+1;
	
  }
  
  
  public void run_constructView() throws Exception{  
	  
	//* Buy entry and observations  
	blBuy = true;
	trades = new ArrayList<Double[]>();
	calc_trades_entry_exit();
	strView = getHeader();
	strView += getObservations();
	calcStats();    //* Buy stats
	strView += getStatsReport();
	
	//plUnrealCum_long = Arrays.copyOfRange(plUnrealCum, 0, plUnrealCum.length);
	plUnrealCum_long = Arrays.copyOf(plUnrealCum, plUnrealCum.length);
	
	/*
    grapher.series1 = new double[session.endTstDateIndex-session.begTstDateIndex+1];
    for(int i=session.begTstDateIndex; i<=session.endTstDateIndex; i++) 
      grapher.series1[i-session.begTstDateIndex] = plUnrealCum[i];
    grapher.go();
    */
    Grapher grapher = new Grapher(session);
    grapher.series_name = new String[2];
    grapher.series_name[0] = "Long";
    grapher.series_name[1] = "Short";
    //grapher.series_name[2] = "Dep";
    grapher.series_fd = new double[2][session.endTstDateIndex-session.begTstDateIndex+1];
    //grapher.series_fd = new double[2][plUnrealCum.length];
    
    //grapher.series_fd[0] = plUnrealCum_long;   //* graph only portion that is being tested
    //System.arraycopy( plUnrealCum_long, 0, grapher.series_fd[0], 0, plUnrealCum_long.length );
    grapher.series_fd[0] = Arrays.copyOfRange(plUnrealCum_long, session.begTstDateIndex, session.endTstDateIndex+1);
    
    //* Sell entry and observations
    blBuy = false;
    trades = new ArrayList<Double[]>(); 
	calc_trades_entry_exit();
	strView += getObservations();
	calcStats();   //* Sell stats
	strView += getStatsReport();
	     
	plUnrealCum_short = Arrays.copyOf(plUnrealCum, plUnrealCum.length);
	grapher.series_fd[1] = Arrays.copyOfRange(plUnrealCum_short, session.begTstDateIndex, session.endTstDateIndex+1);
	
	grapher.construct_dataset_systrade();
	strView += ("CHART_DATA_LONG:" + Arrays.deepToString(grapher.series_str[0]));   //* Arrays.toString(plUnrealCum_long));
	strView += ("CHART_DATA_SHORT:" + Arrays.deepToString(grapher.series_str[1]));
	//strView += ("CHART_DATA_DEP:" + Arrays.deepToString(grapher.series_str[2]));
  }
 
  
  /*** run by Equity Curve
   * - long only and unlimited contracts
   */
  public void runLongOnly() throws Exception{   
	
	//* Buy observations  
	blBuy = true;
	trades = new ArrayList<Double[]>();
	calc_trades_entry_exit();
	strView = getHeader();	
	strView += getObservations();	
	calcStats();   //* Buy stats
	strView += getStatsReport();
	
	plUnrealCum_long = plUnrealCum;
	
    Grapher grapher = new Grapher(session);
    grapher.series_name = new String[1];
    grapher.series_name[0] = "Long";
    grapher.series_fd = new double[1][session.endTstDateIndex-session.begTstDateIndex+1];
    grapher.series_fd[0] = Arrays.copyOfRange(plUnrealCum_long, session.begTstDateIndex, session.endTstDateIndex+1);
    grapher.construct_dataset_systrade();
	strView += ("CHART_DATA_LONG:" + Arrays.deepToString(grapher.series_str[0]));
  }
  
  /*** Run by Hilo
   *** special thing is ENTRY is EVENT as well as event exit if profit/stop-loss *** 
   * but here exit is ONLY Time Target
   */
  public void runForHiLo(String strLvlEvent, boolean blBuy, boolean blZ) throws Exception{ 
	// init();  done by Scenario_HiLo.runSysTrade()
	this.blBuy = blBuy;
	trades = new ArrayList<Double[]>();
	
	//calcTradesDyEntryExit();
	if(blZ)
	  calcTradesEventIntradyEntryZ(strLvlEvent);
	else
	  calcTradesEventIntradyEntryP(strLvlEvent);
	calcStats();
	plUnrealCum_long = plUnrealCum;
	  
	strView = getHeader();
	strView += getObservations();
	strView += getStatsReport();
	
    Grapher grapher = new Grapher(session);
    grapher.series_name = new String[1];
    grapher.series_name[0] = "HiLo : Long enter at " + strLvlEvent;
    grapher.series_fd = new double[1][session.endTstDateIndex-session.begTstDateIndex+1];
    grapher.series_fd[0] = Arrays.copyOfRange(plUnrealCum_long, session.begTstDateIndex, session.endTstDateIndex+1);
    grapher.construct_dataset_systrade();
	strView += ("CHART_DATA_LONG:" + Arrays.deepToString(grapher.series_str[0]));
	
    /*
    if (AGlobal.BUILD_VER == 1) {
        grapher = new Grapher(session.sessionId);
        grapher.titleChart = "ES";
        grapher.series1 = new double[session.endTstDateIndex-session.begTstDateIndex+1];
        for(int i=session.begTstDateIndex; i<=session.endTstDateIndex; i++) 
          grapher.series1[i-session.begTstDateIndex] = InstrDep.prc[i][InstrDep.clsDyCol];
        grapher.go();
    }   
    */ 
  }  
  
  
  private String getHeader() {
	/********************************** 	   
	* Section I: Info header - entry, exit features, time stamp of run, etc for report
	* "Ran at ..."
	**********************************/
	StringBuilder strb = new StringBuilder();
	String strTxt="";
	int entryfixed_timecol = session.entryfixed_timecol;
	
    strb.append("Systematic Trading Analysis\n");
	SimpleDateFormat sdfDtime = new SimpleDateFormat("MM/dd/yyyy HH:mm");
	strTxt = sdfDtime.format(new Date());
	strb.append("Ran at " + strTxt + "\n");
	strTxt = "Calculation results for " + InstrDep.idName +
		     " from " + sdfDtime.format(InstrDep.prcDate[session.begTstDateIndex].getTime()) +
	  	     " to " + sdfDtime.format(InstrDep.prcDate[session.endTstDateIndex].getTime());
    strb.append(strTxt + "\n");
	if(session.bl_entry_fixed && session.USERTYPE != 4)
	  strTxt = "Reference time at: " + InstrDep.prcTime[entryfixed_timecol];
	else if(session.bl_entry_fixed && session.USERTYPE == 4)
	  strTxt = "Entry time at: " + session.entryfixed_dyfwd + ", " + InstrDep.prcTime[entryfixed_timecol]; 	
	else if(session.bl_entry_event && session.USERTYPE == 4)
	  strTxt = "Entry time at: " + session.entryevent_str;   	
    strb.append(strTxt + "\n\n");
	    
	strb.append("Entry Features:\n");
	strTxt = "";
    for(String[] arrstrCmd: session.arrCmdEntryDy)
      if(arrstrCmd[1] == "not")
        strTxt += "  not " + arrstrCmd[0] + "\n";
      else
      	strTxt += "  " + arrstrCmd[0] + "\n"; 
	strb.append(strTxt + "\n");
	
	strb.append("Exit Options Selected:\n");
	if (cmd_bl_exit_feature_fixed || cmd_bl_exit_feature_event) {
	    strb.append("- Exit Features:\n");                   
        strTxt = "  exit(" + session.exitfixed_dyfwd + ", " + InstrDep.prcTime[session.exitfixed_timecol] + ")\n"; // session.exitfixed_str;
	    for(String[] arrstrCmd: session.arrCmdExitDy)
	      if(arrstrCmd[1] == "not")
	        strTxt += "  not " + arrstrCmd[0] + "\n";
	      else
	    	strTxt += "  " + arrstrCmd[0] + "\n";	
		strb.append(strTxt + "\n");
	}
	if (cmd_bl_exit_profittarget_p) 
	    strb.append("- Profit Target: " + cmd_fd_exit_profittarget_p + "\n");
	if (cmd_bl_exit_profittarget_z) 
		strb.append("- Profit Target: " + cmd_fd_exit_profittarget_z + "z \n");
	if (cmd_bl_exit_stoploss_p) 
		strb.append("- Stop P: " + cmd_fd_exit_stoploss_p + "\n");
	if (cmd_bl_exit_stoploss_z) 
		strb.append("- Stop Z: " + cmd_fd_exit_stoploss_z + "z\n");
	if (cmd_bl_exit_timetarget_rel || cmd_bl_exit_timetarget_fix) 
		strb.append("- Time Target: " + cmd_exit_timetarget_dyfwd + ", " + cmd_str_exit_timetarget + "\n");  
	
	return strb.toString();
  }
  
  
  private String getObservations() {
	//* All the trades for the strategy  
	StringBuilder strb = new StringBuilder();
	
	//* Heading
	strb.append("\n");  
    if (blBuy) {
    	strb.append("Trade Observations - Long\n");
    } else {
    	strb.append("Trade Observations - Short\n");
    }
    String prec = "%" + (InstrDep.precPrcLblShow+1) + "s";
    strb.append(String.format("%4s","Y"));
	strb.append(String.format("%3s","M"));
	strb.append(String.format("%3s","D"));
    strb.append(String.format("%7s","Time"));
    strb.append(String.format(prec,"Entered"));
    strb.append(String.format("%9s","Y"));
	strb.append(String.format("%3s","M"));
	strb.append(String.format("%3s","D"));
    strb.append(String.format("%7s","Time"));
    strb.append(String.format(prec, "Exited"));
    strb.append(String.format("%9s", "Dur"));
    strb.append(String.format("%12s", "Exit Rule"));
    prec = "%" + (InstrDep.precPrcLblShow) + "s";
    strb.append(String.format(prec, "P&L"));
    strb.append("\n");
    
    //* Now observations:
    Double[] tradeDetails;
    double entry_prc_t;
    int entry_dyidx_t;
    int entry_timecol_t;
    //int enterRule_t;
    double exit_prc_t;
    int exit_dyidx_t;
    int exit_timecol_t;
    int exitRule_t;
    double pl_t;
    double dur;
    String strExitRule = "";    
 
    tradeDetails = new Double[TRADEDETAILS_MAX];
    for (int t=0; t<trades.size(); t++) {     
      tradeDetails = trades.get(t);
      entry_prc_t = tradeDetails[0];
      entry_dyidx_t = tradeDetails[1].intValue();
      entry_timecol_t = tradeDetails[2].intValue();
      exit_prc_t = tradeDetails[4];
      exit_dyidx_t = tradeDetails[5].intValue();
      exit_timecol_t = tradeDetails[6].intValue();  
      exitRule_t = tradeDetails[7].intValue();
      pl_t = tradeDetails[8];
      
      prec = "%" + (InstrDep.precPrcShow+1.0) + "f"; 
      strb.append(String.format("%4s",InstrDep.getYear(entry_dyidx_t)));
      strb.append(String.format("%3s",InstrDep.getMonth(entry_dyidx_t)));
      strb.append(String.format("%3s",InstrDep.getDay(entry_dyidx_t)));
	  strb.append(String.format("%7s",InstrDep.prcTime[entry_timecol_t]));
      strb.append(String.format(prec,entry_prc_t));  //InstrDep.prc[entry_dyidx_t][entry_timecol_t]));  
      strb.append(String.format("%9s",InstrDep.getYear(exit_dyidx_t)));
      strb.append(String.format("%3s",InstrDep.getMonth(exit_dyidx_t)));
      strb.append(String.format("%3s",InstrDep.getDay(exit_dyidx_t)));      
	  strb.append(String.format("%7s",InstrDep.prcTime[exit_timecol_t]));
      strb.append(String.format(prec, exit_prc_t)); //InstrDep.prc[exit_dyidx_t][exit_timecol_t]));
      
      String strDtime0 = InstrDep.getYear(entry_dyidx_t) + "/" + InstrDep.getMonth(entry_dyidx_t) + "/" + InstrDep.getDay(entry_dyidx_t)  
        + " " + InstrDep.prcTime[entry_timecol_t];
      String strDtime1 = InstrDep.getYear(exit_dyidx_t) + "/" + InstrDep.getMonth(exit_dyidx_t) + "/" + InstrDep.getDay(exit_dyidx_t)  
        + " " + InstrDep.prcTime[exit_timecol_t];
      
      if (session.USERTYPE != 4) {    	  
          dur = (exit_dyidx_t - entry_dyidx_t - 1.0);
          dur += (((InstrDep.clsDyCol-entry_timecol_t+1.0) + (exit_timecol_t-InstrDep.opnDyCol))/(InstrDep.clsDyCol-InstrDep.opnDyCol+1.0));
          dur = Math.abs(dur);
      } else {
          dur = Utils.diff_dtime(strDtime0, strDtime1);
      }
      strb.append(String.format("%9.2f",dur));
  
	  switch (exitRule_t) {
	    case 0:
	      strExitRule = "Qualif";
	      break;
	    case 1:
		  strExitRule = "Stop";
		  break;	      
	    case 2:
	      strExitRule = "Profit"; 	
	      break;
	    case 3:
	      strExitRule = "Time";  //Rel
	      break;
	    case 4:
		  strExitRule = "Time";  //Fix
		  break;	      
	    case 5:
	      //* more later?  
	      break;
	  }
      strb.append(String.format("%12s", strExitRule));
      prec = "%" + (InstrDep.precPrcShow) + "f";
      if(blBuy)
        strb.append(String.format(prec,pl_t));
      else 
    	strb.append(String.format(prec,-pl_t));
      strb.append("\n");
    }  //* for each trade
    
    strb.append("\n");
    
    return strb.toString();
  }  //* method: display observations 
  
  
  private void calcStats() {
    totPl=0;
	avgPl=0;           //* totPts/trade
	stdev=0;
	sharpT=0;
	
	ppos=0;
	maxTrade=-Double.MAX_VALUE;
	minTrade=Double.MAX_VALUE;
	avgWinTrades=0;
	avgLoseTrades=0;
	medLoseTrades=0;
	medWinTrades=0;
	
    maxConsecWinTrades=0;
    maxConsecLoseTrades=0;
    double avgConsecWinTrades=0;
    double avgConsecLoseTrades=0;
	
	maxDrawDn=0;        //* peak to valley
	maxDrawUp=0;        //* valley to peak
	avgDrawDn=0;        //* peak to valley
	avgDrawUp=0;        //* valley to peak
	maxIntraDrawDn=0;   //* intra-trade unrealized
	avgIntraDrawDn=0;        
	avgIntraDrawUp=0;
	ratioAvgIntraDrawDn=0;
 
	longestNbrTradesDrawDn=0; 
	longestDaysDrawDn=0; 
	avgNbrTradesDrawDn=0;
	avgDaysDrawDn=0;
	ratioAvgDaysDrawDn=0;
	
	double totHoldDur = 0;
	avgHoldDur = 0;
	maxHoldDur = 0;
	minHoldDur = Double.MAX_VALUE;
	ptsPerDayHeld = 0;  //* totPts/totHeld

	maxMarginPerMini=0;
	//double maxLeverage;
	
    Double[] tradeDetails = new Double[TRADEDETAILS_MAX];
    double entry_prc_t;
    int entry_dyidx_t;
    int entry_timecol_t;
    //int enterRule_t;
    double exit_prc_t;
    int exit_dyidx_t;
    int exit_timecol_t;
    int exitRule_t;
    double pl_t;
	
	/* calc - Realized PL PER TRADE
	 *      - 
	 */
	plTrades = new double[trades.size()];
	double holdDur = 0;
    for (int t=0; t<trades.size(); t++) {
      tradeDetails = trades.get(t);
      entry_prc_t = tradeDetails[0];
      entry_dyidx_t = tradeDetails[1].intValue();
      entry_timecol_t = tradeDetails[2].intValue();
      exit_prc_t = tradeDetails[4];
      exit_dyidx_t = tradeDetails[5].intValue();
      exit_timecol_t = tradeDetails[6].intValue();  
      exitRule_t = tradeDetails[7].intValue();
      pl_t = tradeDetails[8];
   
      //* PL (realized) PER TRADE!
      if (blBuy) {
          totPl += (exit_prc_t - entry_prc_t);
          plTrades[t] = exit_prc_t - entry_prc_t;
      } else {  
          totPl += (-exit_prc_t + entry_prc_t);
          plTrades[t] = -exit_prc_t + entry_prc_t;
      }  
      
      //* Holding periods - duration
      holdDur = (exit_dyidx_t - entry_dyidx_t - 1); 
      holdDur += (((InstrDep.clsDyCol-entry_timecol_t+1.0) + (exit_timecol_t-InstrDep.opnDyCol))/(InstrDep.clsDyCol-InstrDep.opnDyCol+1.0));
      holdDur = Math.abs(holdDur);
      if (holdDur > maxHoldDur) {
    	  maxHoldDur = holdDur;  
      }
      if (holdDur < minHoldDur) {
    	  minHoldDur = holdDur;  
      }
      totHoldDur += holdDur;
    }
    avgHoldDur = totHoldDur / totTrades;
    ptsPerDayHeld = totPl / totHoldDur;
    avgPl = totPl/totTrades;
    
    //* stdev
	for(int t=0; t<totTrades; t++)
	  stdev += Math.pow((plTrades[t] - avgPl),2);
	stdev /= (totTrades-1);  //* unbiased
    stdev = Math.sqrt(stdev);
    sharpT = avgPl/stdev*Math.sqrt(totTrades);
    
    /* Unrealized PL and Realized PL, changes and cum for both
	 *   plReal     
	 *   plUnreal  
	 *   plRealCum
	 *   plUnrealCum
     */
    calcIntraDayTradePl();
    
    /*
     * This is realized PER TRADE PL!
     * various stats dependent on per trade
     */ 
    int numWinTrades=0;
    int numLoseTrades=0;
    int consecWinTrades=0;
    int consecLoseTrades=0;
    int cntWinStreak=0;
    int cntLoseStreak=0;
    int localMaxWinStreak=0;
    int localMaxLoseStreak=0;
    boolean blWinConsec=false;
    boolean blLoseConsec=false;
    for (int t=0; t<totTrades; t++) {
      
      //* ppos	
      if(plTrades[t] > 0)
        ppos = ppos + 1.0;
      
      //* max and min trade
      if(plTrades[t] > maxTrade)
    	maxTrade = plTrades[t];
     
      if(plTrades[t] < minTrade)
    	minTrade = plTrades[t];
      
      //* avg of Win and Lose trades
      if (plTrades[t] > 0) {
    	  avgWinTrades += plTrades[t];
    	  numWinTrades++;
      } else {
    	  avgLoseTrades += plTrades[t];
    	  numLoseTrades++;
      }
      
      //* maxConsecWinTrades and maxConsecLoseTrades
      //for (int k=t; k<=totTrades; k++) {
      if (plTrades[t] > 0 ) {  //* new start of streak
          blWinConsec = true;
          localMaxWinStreak++;
          consecWinTrades++;
      } else if (blWinConsec) {
          blWinConsec = false;
          avgConsecWinTrades += localMaxWinStreak;
          cntWinStreak++;
          localMaxWinStreak=0;
          if(consecWinTrades > maxConsecWinTrades) 
	    	maxConsecWinTrades = consecWinTrades;
	      consecWinTrades = 0;
      }

      //* maxConsecLoseTrades
      //for (int k=t; k<=totTrades; k++) {
      if (plTrades[t] <= 0 ) {  //* new start of streak
          blLoseConsec = true;
          localMaxLoseStreak++;
          consecLoseTrades++;
      } else if (blLoseConsec) {
          blLoseConsec = false;
          avgConsecLoseTrades += localMaxLoseStreak;
          cntLoseStreak++;
          localMaxLoseStreak=0;
          if(consecLoseTrades > maxConsecLoseTrades)
	    	maxConsecLoseTrades = consecLoseTrades;
          consecLoseTrades = 0;
      }
    }  //* for t=trades
    
    ppos /= totTrades;
    avgWinTrades /= numWinTrades;
    avgLoseTrades /= numLoseTrades;
    
    if (blWinConsec) {
    	cntWinStreak++;
    	avgConsecWinTrades += localMaxWinStreak;
     	if(consecWinTrades > maxConsecWinTrades)
    	  maxConsecWinTrades = consecWinTrades;
    }
    if (cntWinStreak == 0 ) {
    	avgConsecWinTrades = 0;
    } else { 	
        avgConsecWinTrades /= cntWinStreak;
    }
    
    if (blLoseConsec) {
    	cntLoseStreak++;
    	avgConsecLoseTrades += localMaxLoseStreak;
     	if(consecLoseTrades > maxConsecLoseTrades)
    	  maxConsecLoseTrades = consecLoseTrades;
    }    
    if (cntLoseStreak == 0 ) {
    	avgConsecLoseTrades = 0;
    } else { 	
        avgConsecLoseTrades /= cntLoseStreak;
    }
       
    calcRealAndUnrealPl();
    
    /*
     * maxDrawDn and maxDrawUp (based on unrealized pl)
     */ 
    double plTmp=0;
    double localMaxDraw=0;
    int cntDrawDn=0;
    boolean blWentDn=false;
    double curHiPl = 0;
    int kBeg=session.InstrDep.maxDysBk; //begTstDateIndex;
    int kEnd=session.InstrDep.maxDysBk+1;
    while (kBeg < session.endTstDateIndex) {	
      for (kEnd=kBeg+1; kEnd<=session.endTstDateIndex; kEnd++) {
        plTmp = plUnrealCum[kEnd] - curHiPl;  
        if (plTmp < 0) {
            blWentDn = true;
            if (plTmp < localMaxDraw) {
              	localMaxDraw = plTmp;
            }
        } else {
      		if (blWentDn) {
      		    avgDrawDn += localMaxDraw;    
      		    cntDrawDn++;
                if (localMaxDraw < maxDrawDn) {
                  	maxDrawDn = localMaxDraw;
                }
      		    localMaxDraw = 0;
      		    blWentDn = false;
      		    curHiPl = plUnrealCum[kEnd];
      		    break;  
      		} else if (plUnrealCum[kEnd] > curHiPl) {
      			curHiPl = plUnrealCum[kEnd];
      		}
        }
      }   
      kBeg = kEnd;  
    }
    if (blWentDn) {
	    avgDrawDn += localMaxDraw;
	    cntDrawDn++;   	    
        if (localMaxDraw < maxDrawDn) {
          	maxDrawDn = localMaxDraw;
        }
    }
    if (cntDrawDn==0) {
    	avgDrawDn = 0;
    } else {
        avgDrawDn /= cntDrawDn;
    }    
    
    //* maxDrawUp - Note: avgDrawUp AND maxDrawUp different from draw down versions!
    int cntDrawUp=0;
    boolean blWentUp=false;
    plTmp=0;
    kBeg=session.InstrDep.maxDysBk;  //begTstDateIndex;
    while (kBeg < session.endTstDateIndex) {
      curHiPl = plUnrealCum[kBeg];
      localMaxDraw=0;
      blWentUp=false;
      for (kEnd=kBeg+1; kEnd<=session.endTstDateIndex; kEnd++) {
        plTmp = plUnrealCum[kEnd] - curHiPl;  
        if (plTmp > 0) {
            blWentUp = true;
            if (plTmp > localMaxDraw) {
              	localMaxDraw = plTmp;
            }
        } else {
      		if (blWentUp) {
      		    avgDrawUp += localMaxDraw;    
      		    cntDrawUp++;
                if (localMaxDraw > maxDrawUp) {
                  	maxDrawUp = localMaxDraw;
                }
      		    localMaxDraw = 0;
      		    blWentUp = false;
      		    break;
      		} else {
      			
      		}
        }
      }
      int prevBeg = kBeg;
      do {
        kBeg++;
        if(kBeg >= session.endTstDateIndex)
          break;
      } while (plUnrealCum[kBeg] == plUnrealCum[prevBeg]);
      
    }
    
    if(cntDrawUp==0)
      avgDrawUp = 0;
    else 
      avgDrawUp /= cntDrawUp;
    
    /*   
     * optimalF = (((1+winLossRatio)*pctWin)-1)/pctWin
     * optimal f = (((1 + win loss ratio) * probability of winning trade) - 1)/(win loss ratio)
     * maxLeverage = largestLoss*InstrX.optimalFmult/optimalF
     */
    double optimalF =  ( ((1.0+Math.abs(avgWinTrades/avgLoseTrades))*ppos)-1.0 )/Math.abs(avgWinTrades/avgLoseTrades);
    double marginPerMini = Math.abs(minTrade*InstrDep.optimalFmult)/optimalF;
    maxMarginPerMini = 1000000.0/marginPerMini;
	//maxLeverage = (maxMarginPerMini*InstrDep.optimalFmult*InstrDep.prc[InstrDep.maxPrcIndex][InstrDep.clsDyCol])/1000000.0;
	
    /*
     * Now output all the stats just calculated - using getStatsReport()
     */
  }

  
  String getStatsReport(){
	StringBuilder strb = new StringBuilder();
	  
    if(blBuy)
      strb.append("\nStatistics - Long\n");
    else
      strb.append("\nStatistics - Short\n");
    strb.append("------------------");
    strb.append("\nNbr of trades             : ");
    strb.append(String.format("%8d",+ totTrades));
    strb.append("\nTotal points              : ");
    strb.append(String.format("%8.2f", totPl));
    strb.append("\nAvg points                : ");
    strb.append(String.format("%8.2f", avgPl));
    strb.append("\nStdev                     : ");
    strb.append(String.format("%8.2f", stdev));
    strb.append("\nZ                         : ");
    strb.append(String.format("%8.2f", sharpT));
    strb.append("\n");
    
    strb.append("\nPct Win                   : ");
    strb.append(String.format("%8.2f", ppos));
    strb.append("\nMax Trade P&L             : ");
    strb.append(String.format("%8.2f", maxTrade));
    strb.append("\nMin Trade P&L             : ");
    strb.append(String.format("%8.2f", minTrade));
    strb.append("\nAvg PL Win Trades         : ");
    strb.append(String.format("%8.2f", avgWinTrades));
    strb.append("\nAvg PL Lose Trades        : ");
    strb.append(String.format("%8.2f", avgLoseTrades));
    
    if (session.USERTYPE == 4) {
    strb.append("\nRatio Avg PL Win/Lose     : ");
    strb.append(String.format("%8.2f", Math.abs((double)avgWinTrades/avgLoseTrades)));
    }
    strb.append("\n");
    
    if (session.USERTYPE == 4) {
    strb.append("\nStdev Intraday Trade      : ");
    strb.append(String.format("%8.2f", stdIntraTrade));
    strb.append("\nAvg Intraday Trade        : ");
    strb.append(String.format("%8.2f", avgIntraTrade));
    }	    	
    strb.append("\nMax Intraday Trade PL     : ");
    strb.append(String.format("%8.2f", maxIntradayTradesPl));
    strb.append("\nMin Intraday Trade PL     : ");
    strb.append(String.format("%8.2f", minIntradayTradesPl));
    strb.append("\nAvg Intraday Pos Trade PL : ");
    strb.append(String.format("%8.2f", avgPosIntraTrade));
    strb.append("\nAvg Intraday Neg Trade PL : ");
    strb.append(String.format("%8.2f", avgNegIntraTrade));
    if (session.USERTYPE == 4) {
    strb.append("\nPct Neg Intraday Time Spent : ");
    strb.append(String.format("%8.2f", pctNegTimeSpentIntraday));
    }
    
    strb.append("\n");
    strb.append("\nMax Consec Win Streak     : ");
    strb.append(String.format("%8d", maxConsecWinTrades));
    strb.append("\nMax Consec Lose Streak    : ");
    strb.append(String.format("%8d", maxConsecLoseTrades));
    if (session.USERTYPE == 4) {
    strb.append("\nAvg Consec Win Streak     : ");
    strb.append(String.format("%8.2f", avgConsecWinTrades));
    strb.append("\nAvg Consec Lose Streak    : ");
    strb.append(String.format("%8.2f", avgConsecLoseTrades));    
    strb.append("\nRatio Avg Streak Win/Lose : ");
    strb.append(String.format("%8.2f", (double)avgConsecWinTrades/avgConsecLoseTrades));        
    }
    strb.append("\n");
    
    strb.append("\nAvg duration              : ");
    strb.append(String.format("%8.2f", avgHoldDur));
    strb.append("\nMax duration              : ");
    strb.append(String.format("%8.2f", maxHoldDur));
    strb.append("\nMin duration              : ");
    strb.append(String.format("%8.2f", minHoldDur));
    strb.append("\nPts per day               : ");
    strb.append(String.format("%8.2f", ptsPerDayHeld));
    strb.append("\n");
    
    strb.append("\nLargest DrawDn            : ");
    strb.append(String.format("%8.2f", maxDrawDn));
    strb.append("\nLargest DrawUp            : ");
    strb.append(String.format("%8.2f", maxDrawUp));
    if (session.USERTYPE == 4) {
    strb.append("\nAvg DrawDn                : ");
    strb.append(String.format("%8.2f", avgDrawDn));
    strb.append("\nNbr of DrawDn's           : ");
    strb.append(String.format("%8d", cntDrawDn));    	
    strb.append("\nRatio DrawDn/Trades       : ");
    strb.append(String.format("%8.2f", (double)cntDrawDn/totTrades));    	    
    strb.append("\nAvg DrawUp                : ");
    strb.append(String.format("%8.2f", avgDrawUp));    	
    strb.append("\nNbr of DrawUp's           : ");
    strb.append(String.format("%8d", cntDrawUp));    	
    strb.append("\nRatio DrawUp/Trades       : ");
    strb.append(String.format("%8.2f", (double)cntDrawUp/totTrades));    	 
    }
    strb.append("\nMax Size Per $1 mil       : ");
    strb.append(String.format("%8.2f", maxMarginPerMini));    	     
    
    strb.append("\n\n");
    
    return strb.toString();
    
  }  //* method: view stats
  
  
  /* These are for INTER-DAY only, ie close to close:
   * Unrealized PL and Realized PL, changes and cum for both
   * Unreal is what gets graphed...
   */   
  private void calcRealAndUnrealPl() {
	plReal = new double[InstrDep.prc.length];     
	plUnreal = new double[InstrDep.prc.length];  
	plRealCum = new double[InstrDep.prc.length];
    plUnrealCum = new double[InstrDep.prc.length];
    
    Double[] tradeDetails;
    double entry_prc_t;
    int entry_dyidx_t;
    int entry_timecol_t;
    //int enterRule_t;
    double exit_prc_t;
    int exit_dyidx_t;
    int exit_timecol_t;
    int exitRule_t;
    double pl_t;
    double prcEnterInter;
    
	for (int i=InstrDep.maxDysBk; i<=session.endTstDateIndex; i++) {
		
	  for (int t=0; t<totTrades; t++) {
	    tradeDetails = trades.get(t);
	    entry_prc_t = tradeDetails[0];
	    entry_dyidx_t = tradeDetails[1].intValue();
	    entry_timecol_t = tradeDetails[2].intValue();
	    exit_prc_t = tradeDetails[4];
	    exit_dyidx_t = tradeDetails[5].intValue();
	    exit_timecol_t = tradeDetails[6].intValue();  
	    exitRule_t = tradeDetails[7].intValue();
	    //pl_t = tradeDetails[8];	    	    	
	    
	    if (entry_dyidx_t == i) {
	        //* mark to market at close of day price
	    	prcEnterInter = entry_prc_t;
	        for (int iDy=entry_dyidx_t; iDy<=exit_dyidx_t - 1; iDy++) { 
	          if(blBuy)
	            plUnreal[iDy] += (InstrDep.prc[iDy][InstrDep.clsDyCol] - prcEnterInter);
	          else 
	            plUnreal[iDy] += (-InstrDep.prc[iDy][InstrDep.clsDyCol] + prcEnterInter);
	          prcEnterInter = InstrDep.prc[iDy][InstrDep.clsDyCol];
	        }
	        //* Day of exit - note this could be also day of entry!
	        if(blBuy)
	          plUnreal[exit_dyidx_t] += (exit_prc_t - prcEnterInter);
	        else  
	          plUnreal[exit_dyidx_t] += (-exit_prc_t + prcEnterInter);    
	    }
	        
	    if (exit_dyidx_t == i) {
	        if(blBuy)
	          plReal[exit_dyidx_t] += (exit_prc_t - entry_prc_t);
	        else    
	          plReal[exit_dyidx_t] += (-exit_prc_t + entry_prc_t);
	    }
	  }  //* for t trades
	  
	  if (i > session.begTstDateIndex) {
	    plRealCum[i] = plReal[i] + plRealCum[i-1];
	    plUnrealCum[i] = plUnreal[i] + plUnrealCum[i-1];
	  }else {
		plRealCum[i] = plReal[i];
		plUnrealCum[i] = plUnreal[i];		  
	  }
    }  //* for i beg and end test dates	  
  }
  
  private void calcIntraDayTradePl() {    	
    maxIntradayTradesPl=-Double.MAX_VALUE;
	minIntradayTradesPl=Double.MAX_VALUE;
	avgPosIntraTrade=0.0;
	avgNegIntraTrade=0.0;
	avgPosIntraMinTrade=0.0;
	avgNegIntraMinTrade=0.0;
	avgIntraTrade=0.0;
	stdIntraTrade=0.0;
	int totIntraTrades=0;
	int totPosIntraTrades=0;
	int totNegIntraTrades=0;
	int totPosIntraMinTrades=0;
	int totNegIntraMinTrades=0;

    Double[] tradeDetails;
    double entry_prc_t;
    int entry_dyidx_t;
    int entry_timecol_t;
    //int enterRule_t;
    double exit_prc_t;
    int exit_dyidx_t;
    int exit_timecol_t;
    int exitRule_t;
    //double pl_t;

    for (int t=0; t<totTrades; t++) {
      tradeDetails = new Double[TRADEDETAILS_MAX];
      tradeDetails = trades.get(t);
      entry_prc_t = tradeDetails[0];
      entry_dyidx_t = tradeDetails[1].intValue();
      entry_timecol_t = tradeDetails[2].intValue();
      exit_prc_t = tradeDetails[4];
      exit_dyidx_t = tradeDetails[5].intValue();
      exit_timecol_t = tradeDetails[6].intValue();  
      exitRule_t = tradeDetails[7].intValue();
      //pl_t = tradeDetails[8];	
      
	  /* Get path of pl intraday for each trade until exit that trade
       * - first day of entry to cls of that day
	   * - then for all days from next day to day before exit
	   * - lastly day of exit opn to cls unless entry_dyidx_t == exit_dyidx_t
	   */
	  int begDaysTimeCol;
      double timeSpentNeg=0;
      double totTimeSpent=0;
	  double intradayPl=0;
  	  double minIntradaysPl=Double.MAX_VALUE;
	  double maxIntradaysPl=-Double.MAX_VALUE;

	  for (int iDay=entry_dyidx_t; iDay<=exit_dyidx_t-1; iDay++) {
		if(iDay == entry_dyidx_t)
		  begDaysTimeCol = entry_timecol_t+1;    
		else 
		  begDaysTimeCol = InstrDep.firstTimeCol;
		
		for (int jTimeCol=begDaysTimeCol; jTimeCol<=InstrDep.lastTimeCol; jTimeCol++) {
          if(blBuy)
            intradayPl = (InstrDep.prc[iDay][jTimeCol] - entry_prc_t);
          else
            intradayPl = (-InstrDep.prc[iDay][jTimeCol] + entry_prc_t);
          if (intradayPl > maxIntradayTradesPl) maxIntradayTradesPl = intradayPl;
          if (intradayPl > maxIntradaysPl) maxIntradaysPl = intradayPl;
          if (intradayPl < minIntradayTradesPl) minIntradayTradesPl = intradayPl;
          if (intradayPl < minIntradaysPl) minIntradaysPl = intradayPl;
          if (intradayPl >= 0) {
        	  avgPosIntraMinTrade += intradayPl;
        	  totPosIntraMinTrades++;
          } else {
        	  avgNegIntraMinTrade += intradayPl;
        	  totNegIntraMinTrades++;
        	  timeSpentNeg++;
          }
          totTimeSpent++;
          avgIntraTrade += intradayPl;
          totIntraTrades++;
		}
      }
	  
	  //* now on day exiting
	  if(exit_dyidx_t == entry_dyidx_t)
		begDaysTimeCol = entry_timecol_t+1;    
	  else 
		begDaysTimeCol = InstrDep.firstTimeCol;
	  
      for (int jTimeCol=begDaysTimeCol; jTimeCol<=exit_timecol_t; jTimeCol++) {
        if(blBuy)
          intradayPl = (InstrDep.prc[exit_dyidx_t][jTimeCol] - entry_prc_t);
        else    
          intradayPl = (-InstrDep.prc[exit_dyidx_t][jTimeCol] + entry_prc_t);
        
        if (intradayPl > maxIntradayTradesPl) maxIntradayTradesPl = intradayPl;
        if (intradayPl > maxIntradaysPl) maxIntradaysPl = intradayPl;
        if (intradayPl < minIntradayTradesPl) minIntradayTradesPl = intradayPl;
        if (intradayPl < minIntradaysPl) minIntradaysPl = intradayPl;
        if (intradayPl >= 0) {
      	    avgPosIntraMinTrade += intradayPl;
      	    totPosIntraMinTrades++;
        } else {
      	    avgNegIntraMinTrade += intradayPl;
      	    totNegIntraMinTrades++;
      	    timeSpentNeg++;
        }
        totTimeSpent++;
        avgIntraTrade += intradayPl;
        totIntraTrades++;
      }
      pctNegTimeSpentIntraday += (timeSpentNeg/totTimeSpent);
      
      if (maxIntradaysPl >= 0) {
          avgPosIntraTrade += maxIntradaysPl;
          totPosIntraTrades++;
      } 
      if (minIntradaysPl < 0) {    
          avgNegIntraTrade += minIntradaysPl;
          totNegIntraTrades++;
      }
      
    } //*  for each trade
    
    avgPosIntraMinTrade /= totPosIntraMinTrades;
    avgNegIntraMinTrade /= totNegIntraMinTrades;
    avgIntraTrade /= totIntraTrades;
    
    pctNegTimeSpentIntraday /= totTrades;
    
    avgPosIntraTrade /= totPosIntraTrades;
    avgNegIntraTrade /= totNegIntraTrades;  
  }  //*  method calcIntradayTradePl
  
     
  public void calc_trades_entry_exit() throws Exception{ 
	trds_entry = new Processor(session).run_entry_dy_intrady();    
    calc_trades_exit();
  }
  
  
  public void calc_trades_exit() throws Exception{
	/***
	 * Requires: Trades trds_entry
	 * Sets trades  
	 */
    double exit_prc;
    int exitReason;
    int exitFirstDayIndex;
    int exitFirstTimeCol;
    boolean blExitFound;
    Double[] tradeDetails;
    double entry_prc_t;
	int entry_dyidx_t;
	int entry_dyfwd_t;
	int entry_timecol_t;
	
	Trades trds_exit_fixed=null, trds_exit_event=null;
	ArrayList<Integer> tradesOpenContractKey = new ArrayList<Integer>();	
	int cntTrades=0;
	
    //* Exit Feature option - one or both can be set, in which case first entry
    if (cmd_bl_exit_feature_fixed) {
    	boolean bl_orig = session.bl_exit_event;
    	session.bl_exit_event = false;
    	trds_exit_fixed = new Processor(session).run_exit_dy_intrady();
    	session.bl_exit_event = bl_orig;
    }	
    if (cmd_bl_exit_feature_event) {
    	boolean bl_orig = session.bl_exit_fixed;
    	session.bl_exit_fixed = false;    	
    	trds_exit_event = new Processor(session).run_exit_dy_intrady();
    	session.bl_exit_fixed = bl_orig;
    }	
    if (cmd_bl_exit_feature_fixed && cmd_bl_exit_feature_event) {
        //* go through both and set the first trds_exit - BELOW
    } else if (cmd_bl_exit_feature_fixed && !cmd_bl_exit_feature_event) {
    	trds_exit = trds_exit_fixed;
    } if (!cmd_bl_exit_feature_fixed && cmd_bl_exit_feature_event) {
    	trds_exit = trds_exit_event;
    }
	
    //* Given each trade entry, now go through possible exits 
    //* and pick the one that happens first
    for (int t=0; t < trds_entry.entry_dyidx.size(); t++) {
    	entry_dyidx_t = trds_entry.entry_dyidx.get(t); 	 	
    	entry_dyfwd_t = trds_entry.entry_dyfwd.get(t);  //* NOT BEING USED! ESP Z SEARCH
        entry_timecol_t = trds_entry.entry_timecol.get(t);         
        entry_prc_t = InstrDep.prc[entry_dyidx_t][entry_timecol_t];   
        //System.out.println(">"+InstrDep.getYear(enterDyCondIdx_t)+"/"+InstrDep.getMonth(enterDyCondIdx_t)+"/"+InstrDep.getDay(enterDyCondIdx_t));
        
        exitFirstDayIndex=session.endTstDateIndex+1;
        exitFirstTimeCol=InstrDep.lastTimeCol+1;
        exitReason=-1;
        exit_prc=-9999999;
        blExitFound = false;    	  
          
        /*** 
         * Now which exit option(s) - only one!: take first which occurs if multiple options checked
         */
        //* Exit has to happen AFTER the entry AND the first of fixed or event
        if (( cmd_bl_exit_feature_fixed && !cmd_bl_exit_feature_event) || 
        	(!cmd_bl_exit_feature_fixed && cmd_bl_exit_feature_event))
          {
        	/* Entry: c > c1 enter(0,1615)  enter(2,1615)
        	 * Exit:  c > c1                exit(1,1615)
        	 * Exit:  o > c1 exit(0,1617)   exit(1,0300)
        	 * Exit:  c < c1 exit(0,1617)
        	 */
            int exit_dyidx_k;
            int exit_dyfwd_k;
            int exit_mincol_k;
    	    for (int k_exit=0; k_exit<trds_exit.exit_dyidx.size(); k_exit++) {
    	        exit_dyidx_k = trds_exit.exit_dyidx.get(k_exit);
    	        exit_dyfwd_k = trds_exit.exit_dyfwd.get(k_exit); 	 
    	        exit_mincol_k = trds_exit.exit_timecol.get(k_exit);
    	        if ((exit_dyfwd_k == 0 && exit_dyidx_k == entry_dyidx_t && exit_mincol_k > entry_timecol_t) ||
    	        	(exit_dyfwd_k == 0 && exit_dyidx_k > entry_dyidx_t) || 
    	        	(exit_dyfwd_k  > 0 && exit_dyidx_k - exit_dyfwd_k >= entry_dyidx_t)  //* same thing...
    	    	   ) {
    	            exitFirstDayIndex = exit_dyidx_k;
    	            exitFirstTimeCol = exit_mincol_k;
    	            exitReason = 0;
    	            exit_prc = InstrDep.prc[exitFirstDayIndex][exitFirstTimeCol];
    	            blExitFound = true;
    	            break;
    	        }
    	    }
        }    

        if (( cmd_bl_exit_feature_fixed && cmd_bl_exit_feature_event)){
    	/***
    	 * NEED TODO
    	 */
        }
        
        if (cmd_bl_exit_stoploss_p) {
        	String ret = searchEvtP(evtStopBegFrameTimeCol, evtStopEndFrameTimeCol,
		                            evtStopBegTimeCol, evtStopEndTimeCol,
                                    evtStopBegDyFwd, evtStopEndDyFwd, 
                                    entry_dyidx_t, entry_prc_t, cmd_fd_exit_stoploss_p, !blBuy);
            if (ret.length() > 0) {
                String params[] = ret.split(",");
                int k = Integer.parseInt(params[0]);	   
                int j = Integer.parseInt(params[1]);
 
                if ((k < exitFirstDayIndex) || 
                   ((k == exitFirstDayIndex) && (j < exitFirstTimeCol))) {
                    exitFirstDayIndex = k;	   
                    exitFirstTimeCol = j;
                    exit_prc = Double.valueOf(params[2]);  //InstrDep.prc[exitFirstDayIndex][exitFirstTimeCol];  //entry_prc_t + cmdfdProfitTarget;
                    exitReason = 1;
                    blExitFound = true;
                }
            }            
        }          
        
        if (cmd_bl_exit_stoploss_z) {
        	evtStopBegTimeCol = entry_timecol_t+1;
        	double zThresh = -cmd_fd_exit_stoploss_z;
        	if(!blBuy) zThresh = -zThresh;
        	                         
        	String ret = searchEvtZ(evtStopBegFrameTimeCol, evtStopEndFrameTimeCol,
	                                evtStopBegTimeCol, evtStopEndTimeCol,
                                    evtStopBegDyFwd, evtStopEndDyFwd,
                                    entry_dyidx_t, entry_prc_t, zThresh, evtStopStdPeriod);
        	if (ret.length() > 0) {
        	    String params[] = ret.split(",");
                int k = Integer.parseInt(params[0]);	   
                int j = Integer.parseInt(params[1]);
                
	    	    if ((k < exitFirstDayIndex) || 
	 	      	   ((k == exitFirstDayIndex) && (j < exitFirstTimeCol))) {
	 	            exitFirstDayIndex = k;	   
	 	            exitFirstTimeCol = j;
	 	            exit_prc = Double.valueOf(params[2]);  //InstrDep.prc[exitFirstDayIndex][exitFirstTimeCol];  //entry_prc_t + cmdfdProfitTarget;
	                exitReason = 1;
	                blExitFound = true;
	 	    	}

        	}    
        	//System.out.println("->"+ret); 
        }
        
        if (cmd_bl_exit_profittarget_p) {
            /*
            boolean blHitProfitTargetDay = false;
            for (int j=Strategy.timeRefCol+1; j<=InstrDep.lastTimeCol; j++) { //* first entry day - could be midday...
       	       if ((blBuy && (InstrDep.prc[entry_dyidx_t][j] - entry_prc_t >= cmd_fd_exit_profittarget_p)) || 
                  (!blBuy && (-(InstrDep.prc[entry_dyidx_t][j] - entry_prc_t) >= cmd_fd_exit_profittarget_p))) {    	        	
      	    	    blHitProfitTargetDay = true;
      	    	    if ((entry_dyidx_t < exitFirstDayIndex) || 
      	    	        (entry_dyidx_t == exitFirstDayIndex && j < exitFirstTimeCol)) {
      	                exitFirstDayIndex = entry_dyidx_t;
      	                exitFirstTimeCol = j;
      	                exitReason = 2;
     		    	    if(blBuy)
     		    		  exit_prc = InstrDep.prc[exitFirstDayIndex][exitFirstTimeCol]; //entry_prc_t + cmdfdProfitTarget;    
          		        else    
          		    	  exit_prc = InstrDep.prc[exitFirstDayIndex][exitFirstTimeCol];  //entry_prc_t - cmdfdProfitTarget;      	                
      	                blExitFound = true;
      	            }
      	            break;
      	        }  
        	}
        	if (!blHitProfitTargetDay) {
                boolean blHitProfitTarget = false;
    	        for (int k=entry_dyidx_t+1; k<=Strategy.endTstDateIndex; k++) {  //* now rest
    	          for (int j=InstrDep.firstTimeCol; j<=InstrDep.lastTimeCol; j++) {
      	            if ((blBuy && (InstrDep.prc[k][j] - entry_prc_t >= cmd_fd_exit_profittarget_p)) ||
                        (!blBuy && (-(InstrDep.prc[k][j] - entry_prc_t) >= cmd_fd_exit_profittarget_p))) {  	            	
      	    	        blHitProfitTarget = true;
      	    	        if ((k < exitFirstDayIndex) || 
      	    	           ((k == exitFirstDayIndex) && (j < exitFirstTimeCol))) {
      	                    exitFirstDayIndex = k;	   
      	                    exitFirstTimeCol = j;
      	                    exitReason = 2;
      	     		    	if(blBuy)
      	     		    	  exit_prc = InstrDep.prc[exitFirstDayIndex][exitFirstTimeCol];  //entry_prc_t + cmdfdProfitTarget;    
      	          		    else    
      	          		      exit_prc = InstrDep.prc[exitFirstDayIndex][exitFirstTimeCol];  //entry_prc_t - cmdfdProfitTarget;   
      	                    blExitFound = true;
      	                }
      	                break;
      	            }
    	          }
    	          if(blHitProfitTarget)
    	            break;
      	        }
            }
            */
        	
        	evtProfitBegTimeCol = entry_timecol_t+1;
        	String ret = searchEvtP(evtProfitBegFrameTimeCol, evtProfitEndFrameTimeCol,
        			                evtProfitBegTimeCol, evtProfitEndTimeCol,
                                    evtProfitBegDyFwd, evtProfitEndDyFwd, 
                                    entry_dyidx_t, entry_prc_t, cmd_fd_exit_profittarget_p, blBuy);
        	if (ret.length()>0) {
        	    String params[] = ret.split(",");
                int k = Integer.parseInt(params[0]);	   
                int j = Integer.parseInt(params[1]);
                
	    	    if ((k < exitFirstDayIndex) || 
	      	       ((k == exitFirstDayIndex) && (j < exitFirstTimeCol))) {
	                exitFirstDayIndex = k;	   
	                exitFirstTimeCol = j;
	                exit_prc = Double.valueOf(params[2]);  //InstrDep.prc[exitFirstDayIndex][exitFirstTimeCol];  //entry_prc_t + cmdfdProfitTarget;
                    exitReason = 2;
                    blExitFound = true;
	    	    }
        	}	
        }          

        if (cmd_bl_exit_profittarget_z) {
        	evtProfitBegTimeCol = entry_timecol_t+1;
        	//double prcRef_i = InstrDep.prc[entry_dyidx_t][Strategy.timeRefCol];
        	double zThresh = cmd_fd_exit_profittarget_z;
        	if(!blBuy) 
              zThresh = -zThresh;
        	
        	String ret = searchEvtZ(evtProfitBegFrameTimeCol, evtProfitEndFrameTimeCol,
        			                evtProfitBegTimeCol, evtProfitEndTimeCol,
                                    evtProfitBegDyFwd, evtProfitEndDyFwd, 
                                    entry_dyidx_t, entry_prc_t, zThresh, evtProfitStdPeriod);
        	if (ret.length()>0) {
        	    String params[] = ret.split(",");
                int k = Integer.parseInt(params[0]);	   
                int j = Integer.parseInt(params[1]);
                
	    	    if ((k < exitFirstDayIndex) || 
	      	       ((k == exitFirstDayIndex) && (j < exitFirstTimeCol))) {
	                exitFirstDayIndex = k;	   
	                exitFirstTimeCol = j;
	                exit_prc = Double.valueOf(params[2]);  //InstrDep.prc[exitFirstDayIndex][exitFirstTimeCol];  //entry_prc_t + cmdfdProfitTarget;
                    exitReason = 2;
                    blExitFound = true;
	    	    }
        	} 
        }
        
        if (cmd_bl_exit_timetarget_rel) {  //* "+1, 1430" this is rel from pt of entry!       	 
    	     if (entry_dyidx_t+cmd_exit_timetarget_dyfwd <= session.endTstDateIndex) {  
  	             if ((entry_dyidx_t+cmd_exit_timetarget_dyfwd < exitFirstDayIndex) || 
  	                ((entry_dyidx_t+cmd_exit_timetarget_dyfwd == exitFirstDayIndex && 
  	                  cmd_exit_timetarget_timecol < exitFirstTimeCol))) {
  	                 exitFirstDayIndex = entry_dyidx_t + cmd_exit_timetarget_dyfwd;
  	                 exitFirstTimeCol = cmd_exit_timetarget_timecol;
  	                 exitReason = 3;
  	                 exit_prc = InstrDep.prc[exitFirstDayIndex][exitFirstTimeCol];
  	                 blExitFound = true;
  	             }
    	     }
         }        
         
         if (cmd_bl_exit_timetarget_fix) {  //* "1, 1430" this is fixed time forward fr ref time + day!	
    	     if (trds_entry.evtSrchBegDyIdx.get(t) + cmd_exit_timetarget_dyfwd <= session.endTstDateIndex) {  
  	             if (((trds_entry.evtSrchBegDyIdx.get(t) + cmd_exit_timetarget_dyfwd < exitFirstDayIndex) || 
  	                  (trds_entry.evtSrchBegDyIdx.get(t) + cmd_exit_timetarget_dyfwd == exitFirstDayIndex &&
  	                   cmd_exit_timetarget_timecol < exitFirstTimeCol)) &&
  	                 ((entry_dyidx_t <  trds_entry.evtSrchBegDyIdx.get(t) + cmd_exit_timetarget_dyfwd) ||
  	                  (entry_dyidx_t == trds_entry.evtSrchBegDyIdx.get(t) + cmd_exit_timetarget_dyfwd &&		
  	                   entry_timecol_t <= cmd_exit_timetarget_timecol))
  	                ) {
  	                 exitFirstDayIndex = trds_entry.evtSrchBegDyIdx.get(t) + cmd_exit_timetarget_dyfwd;
  	                 exitFirstTimeCol = cmd_exit_timetarget_timecol;
  	                 exitReason = 4;
  	                 exit_prc = InstrDep.prc[exitFirstDayIndex][exitFirstTimeCol];
  	                 blExitFound = true;
  	             }
    	     }
         }    
          
         //* 0) Go thru all OPN trades and see if exited out before today's entry  
         for (int toc=0; toc<tradesOpenContractKey.size(); toc++) {
            Double[] tradeInfo = trades.get(tradesOpenContractKey.get(toc));   //* these are only the open contracts!         
      	    	
      	    if ((tradeInfo[5].intValue() < entry_dyidx_t) ||
      	        (tradeInfo[5].intValue() == entry_dyidx_t && tradeInfo[6].intValue() <= entry_timecol_t)) {
      	        tradesOpenContractKey.remove(toc);
      	    }
         }
        
         //* 1) Now add contract ONLY if below contract limit  
         if (tradesOpenContractKey.size() < cmd_maxopencontract && blExitFound) {
         	 tradesOpenContractKey.add(cntTrades);
         	 
	         tradeDetails = new Double[TRADEDETAILS_MAX];
	         tradeDetails[0] = entry_prc_t;
	         tradeDetails[1] = (double)entry_dyidx_t;
	         tradeDetails[2] = (double)entry_timecol_t;
	         tradeDetails[3] = -1.0;
	         tradeDetails[4] = exit_prc;
	         tradeDetails[5] = (double)exitFirstDayIndex;
	         tradeDetails[6] = (double)exitFirstTimeCol;
	         tradeDetails[7] = (double)exitReason;
	         tradeDetails[8] = exit_prc - entry_prc_t;
	         tradeDetails[9] = -1.0;
	         trades.add(tradeDetails);
		     cntTrades++;
       }   
      
    }  //* t for loop for all entries 
    totTrades = cntTrades;
    
  }  //* calc method
	
  
  /* 
   * For HiLo
   * All these must have been set BEFORE:
   *  evtFrameBeg_TimeCol, evtFrameEnd_TimeCol
   *  evtSrchBeg_TimeCol, evtSrchEnd_TimeCol
   *  evtSrchBeg_DyFwd, evtSrchEnd_DyFwd
   */
  public void calcTradesEventIntradyEntryP(String strLvlEvent) throws Exception{  //* given day cond occurred | enter at intrady evt, NOT time
    /* For now - this is used only by hilo: 
     *  E > p@ref + "5", 0, 1615, day/all
	 *  E > p@ref + "2.0z"
	 *  E > "h1"
	 *  E < "l(p1@0600,p1@1615)"
	 */
	double ptsEnter;
    double prc_ij;	  
    double prcThresh_i;
    
    trds_entry = new Processor(session).run_entry_dy();   
    
    Strat_HighLow strat_HighLow = null;
    if (strLvlEvent.equals("h1")) {
    	ptsEnter = 1;
    } else if (strLvlEvent.equals("l1")) {
    	ptsEnter = -1;
    } else if (strLvlEvent.indexOf("h(") >= 0) {
    	strat_HighLow = new Strat_HighLow(InstrDep, "h(p1@0600,p1@1615)", session);
    	//strat_HighLow.InstrX = InstrDep;
    	strat_HighLow.parseAndSetConditions();
    	ptsEnter = 1;
    } else if (strLvlEvent.indexOf("l(") >= 0) {
    	strat_HighLow = new Strat_HighLow(InstrDep, "l(p1@0600,p1@1615)", session);
    	//strat_HighLow.InstrX = InstrDep;
    	strat_HighLow.parseAndSetConditions();
    	ptsEnter = -1;
    } else {
    	ptsEnter = Double.parseDouble(strLvlEvent);
    }
    
    //for (int t=0; t < trds_entry.dyIdx.size(); t++) {
    for (int i=session.InstrDep.maxDysBk; i<=session.endTstDateIndex-cmd_exit_timetarget_dyfwd; i++) {
        //for (int i=0; i<trds.conditionDy.length; i++) {
        if(trds_entry.conditionDy[i]!=1)
          continue;    
       
        //System.out.println(InstrDep.getYear(i)+"/"+InstrDep.getMonth(i)+"/"+InstrDep.getDay(i));      
        if (strLvlEvent.equals("h1")) {
    	    prcThresh_i = InstrDep.prc[i-1][InstrDep.hiDyCol];
            //System.out.println(" " + prcThresh_i + " " + Strategy.timeRefCol);  
            //System.out.println(" " + InstrDep.prc[i + evtSrchBeg_DyFwd][evtSrchBeg_TimeCol]);  
        } else if (strLvlEvent.equals("l1")) {    	   
    	   prcThresh_i = InstrDep.prc[i-1][InstrDep.loDyCol];
        } else if (strLvlEvent.indexOf("h(") >= 0) {
    	   prcThresh_i = strat_HighLow.calcHigh(i);   
        } else if (strLvlEvent.indexOf("l(") >= 0) {
    	   prcThresh_i = strat_HighLow.calcLow(i);
        } else { 	
    	   prcThresh_i = InstrDep.prc[i][session.entryfixed_timecol] + ptsEnter; 	
        }
        //System.out.println(" " + evtSrchBeg_DyFwd + ","+ evtSrchBeg_TimeCol + " to " + evtSrchEnd_DyFwd+ "," + evtSrchEnd_TimeCol);       
        boolean blFoundEvent = false;
        int begCol_d;
        int endCol_d;
        for (int idyfwd=evtSrchBeg_DyFwd; idyfwd<=evtSrchEnd_DyFwd; idyfwd++) {	
      	  
        if (idyfwd == evtSrchBeg_DyFwd) {   //* also good for idyfwd == evtSrchBeg_DyFwd == evtSrchEnd_DyFwd   	
    	    if(evtFrameBeg_TimeCol > evtSrchBeg_TimeCol)
    	      begCol_d = evtFrameBeg_TimeCol;
    	    else 
    	      begCol_d = evtSrchBeg_TimeCol; 
    	} else {
    	    if(evtFrameBeg_TimeCol > InstrDep.firstTimeCol)
    	      begCol_d = evtFrameBeg_TimeCol;
    	    else
    	      begCol_d = InstrDep.firstTimeCol;
    	}
    	        
    	if (idyfwd < evtSrchEnd_DyFwd) {
    	    if(evtFrameEnd_TimeCol < InstrDep.lastTimeCol)
    	      endCol_d = evtFrameEnd_TimeCol;
    	    else 
    	      endCol_d = InstrDep.lastTimeCol;
    	} else {  	  //* also good for idyfwd == evtSrchBeg_DyFwd == evtSrchEnd_DyFwd
    	    if(evtFrameEnd_TimeCol < evtSrchEnd_TimeCol)
    	      endCol_d = evtFrameEnd_TimeCol;
    	    else 
    	      endCol_d = evtSrchEnd_TimeCol;
    	} 
      	                    		      
        for (int j=begCol_d; j<=endCol_d; j++) {  //* go across time
            prc_ij = InstrDep.prc[i + idyfwd][j];
      	    if ((ptsEnter <  0 && prc_ij <= prcThresh_i) || 
      		    (ptsEnter >= 0 && prc_ij >= prcThresh_i)) { 
      	    	            
      	    	 trds_entry.evtSrchBegDyIdx.add(i);
      	    	 trds_entry.evtSrchBegTimeCol.add(evtSrchBeg_TimeCol);
      	    	
      	    	 trds_entry.entry_dyidx.add(i + idyfwd);
      	    	 trds_entry.entry_dyfwd.add(idyfwd);
      	    	 trds_entry.entry_timecol.add(j);	 
      	    	 trds_entry.entry_prc.add(prc_ij);  //prcThresh_i
      	    	 
      	    	 blFoundEvent = true;
		         break;
      	     }        
      	  }  //*  for look across in time 
      	  if(blFoundEvent) break;
      }  //* for look fwd in days
      //* quite possible no event entry given cond dy
   }  //* i next cond dy
   
   calc_trades_exit();
   
  }
  
  /* 
   * For HiLo
   * Must return:
   *  Strategy.trdEntryDyIndex
   *  Strategy.trdEntryMinIndex
   *  Strategy.trdentry_prc
   */
  public void calcTradesEventIntradyEntryZ(String strZThresh) throws Exception{  //* given day evt occurred | enter at intrady evt, NOT time
    /* For now - this is for hilo only: 
     *  b > Ref + "5", 0, 1615, day/all
	 *  b > Ref + "2.0z"
     *  b < Ref - "1.5z"
	 */  
	int cmdStdPeriod = 40;  
    double zThresh = Double.parseDouble(strZThresh.substring(0,strZThresh.lastIndexOf("z")).trim()); 
    double prcRef_i;
    
    trds_entry = new Processor(session).run_entry_dy();
    
    if(InstrDep.maxDysBk < cmdStdPeriod+1) 
      InstrDep.maxDysBk = cmdStdPeriod+1;
    
    //* now need to calc: trds.dyIdx, trdsMinTimeCol
    //* cuz not every trdCondDyIndex will turn into actual trade   
    for (int i=session.InstrDep.maxDysBk; i<=session.endTstDateIndex-cmd_exit_timetarget_dyfwd; i++) {
    //for (int i=0; i<trds.conditionDy.length; i++) {
       if(trds_entry.conditionDy[i]!=1)
         continue;
        
	   prcRef_i = InstrDep.prc[i][session.entryfixed_timecol];
	
  	   String ret = searchEvtZ(evtFrameBeg_TimeCol, evtFrameEnd_TimeCol, 
                               evtSrchBeg_TimeCol, evtSrchEnd_TimeCol,
                               evtSrchBeg_DyFwd, evtSrchEnd_DyFwd, 
                               i, prcRef_i, zThresh, cmdStdPeriod);
	   if (ret.length()>0) {
	       String params[] = ret.split(",");
           int evtDy = Integer.parseInt(params[0]);	   
           int evtTimeCol = Integer.parseInt(params[1]);
           double evtPrc = Double.valueOf(params[2]);  //InstrDep.prc[exitFirstDayIndex][exitFirstTimeCol];  //entry_prc_t + cmdfdProfitTarget;
                      
	       trds_entry.evtSrchBegDyIdx.add(i);
  	       trds_entry.evtSrchBegTimeCol.add(evtSrchBeg_TimeCol);

	       trds_entry.entry_dyidx.add(evtDy); 
	       trds_entry.entry_dyfwd.add(0);
	       trds_entry.entry_timecol.add(evtTimeCol);	 
	       trds_entry.entry_prc.add(evtPrc);  
	   }
       //* quite possible no event entry given cond dy
    }  //* i next cond dy
   
    calc_trades_exit();
  }
  
  /* Used for Entry's AND Exit's
   * Searches for evt from specified i, evtSrchBeg_DyFwd, evtSrchBeg_TimeCol to evtSrchEnd_DyFwd, evtSrchEnd_TimeCol
   * and within that search time only within time brackets evtFrameBeg_TimeCol, evtFrameEnd_TimeCol   
   * return: "dy, timeCol, prc"
   */
  private String searchEvtZ(int evtFrameBeg_TimeCol, int evtFrameEnd_TimeCol, 
                            int evtSrchBeg_TimeCol, int evtSrchEnd_TimeCol,
                            int evtSrchBeg_DyFwd, int evtSrchEnd_DyFwd, 
                            int i, double prcRef_t, double zThresh, int stdPeriod) {
	  
	//int stdPeriod = 40;  
	double prc_ij;	 
	double prc_evt;
	   
	double X;
    double mu_i;
	double fdStd_i;
	double fdZscore_i;  
    
    if(i-stdPeriod-2 < session.begTstDateIndex)
      return "";
	
    X=0.0;
	mu_i=0.0;
    fdStd_i=0.0;
    fdZscore_i=0.0;
	for (int k=0; k<stdPeriod; k++) {
      X = InstrDep.prc[i-k-1][InstrDep.clsDyCol] - InstrDep.prc[i-k-2][InstrDep.clsDyCol];
	  mu_i += X;
	}  
	mu_i /= stdPeriod;
	for (int k=0; k<stdPeriod; k++) {
	  X = InstrDep.prc[i-k-1][InstrDep.clsDyCol] - InstrDep.prc[i-k-2][InstrDep.clsDyCol];
	  fdStd_i += Math.pow(X - mu_i,2);
	}  
	fdStd_i /= (stdPeriod-1);  //* unbiased
	fdStd_i = Math.sqrt(fdStd_i);
		
    //prcRef_t = InstrDep.prc[i][Strategy.timeRefCol]; 	
    int begCol_d;
    int endCol_d;
    for (int idyfwd=evtSrchBeg_DyFwd; idyfwd<=evtSrchEnd_DyFwd; idyfwd++) {	
      if(i+idyfwd > session.endTstDateIndex)
        return "";
      
      if (idyfwd == evtSrchBeg_DyFwd) {   //* also good for idyfwd == evtSrchBeg_DyFwd == evtSrchEnd_DyFwd   	
          if(evtFrameBeg_TimeCol > evtSrchBeg_TimeCol)
            begCol_d = evtFrameBeg_TimeCol;
          else 
            begCol_d = evtSrchBeg_TimeCol; 
      } else {
      	  if(evtFrameBeg_TimeCol > InstrDep.firstTimeCol)
      	    begCol_d = evtFrameBeg_TimeCol;
      	  else
      	    begCol_d = InstrDep.firstTimeCol;
      }
        
      if (idyfwd < evtSrchEnd_DyFwd) {
      	  if(evtFrameEnd_TimeCol < InstrDep.lastTimeCol)
      	    endCol_d = evtFrameEnd_TimeCol;
      	  else 
      		endCol_d = InstrDep.lastTimeCol;
      } else {  	  //* also good for idyfwd == evtSrchBeg_DyFwd == evtSrchEnd_DyFwd
      	  if(evtFrameEnd_TimeCol < evtSrchEnd_TimeCol)
            endCol_d = evtFrameEnd_TimeCol;
      	  else 
      		endCol_d = evtSrchEnd_TimeCol;
      } 
 		      
      for (int j=begCol_d; j<=endCol_d; j++) {  //* go across time
        prc_ij = InstrDep.prc[i + idyfwd][j];
        fdZscore_i = (prc_ij - prcRef_t - mu_i)/fdStd_i; 
        
 	    if ((zThresh <  0 && fdZscore_i <= zThresh) ||
 		    (zThresh >= 0 && fdZscore_i >= zThresh)) {
 	    	 
 	    	 //System.out.println(InstrDep.getYear(i)+"/"+InstrDep.getMonth(i)+"/"+InstrDep.getDay(i));
 	    	 //System.out.println(fdZscore_i + "><" + zThresh + " " + prc_ij + " - " + prcRef_t +" - " + mu_i + "/" +fdStd_i);
 	    	 
 	         prc_evt = prcRef_t + mu_i + (zThresh*fdStd_i);
 	         return (i + idyfwd) + "," + j + "," + prc_ij;
 	     }        
 	  }  //*  for look across in time 
    }  //* for look fwd in days
    
    //* quite possible no event entry given cond dy
    return "";
  }

  /* Used for Entry's AND Exit's
   * Searches for evt from day i, evtSrchBeg_DyFwd, evtSrchBeg_TimeCol -> evtSrchEnd_DyFwd, evtSrchEnd_TimeCol
   * and within that search time only within time brackets evtFrameBeg_TimeCol, evtFrameEnd_TimeCol   
   * return: "dy, timeCol, prc"
   */
  private String searchEvtP(int evtFrameBeg_TimeCol, int evtFrameEnd_TimeCol, 
                            int evtSrchBeg_TimeCol, int evtSrchEnd_TimeCol,
                            int evtSrchBeg_DyFwd, int evtSrchEnd_DyFwd, 
                            int i, double prcRef_t, double ptsTarget, boolean blLong) {
    //D System.out.println(i + " " + evtFrameBeg_TimeCol + " " + evtFrameEnd_TimeCol + " " + evtSrchBeg_TimeCol + " " + evtSrchEnd_TimeCol + " " + evtSrchBeg_DyFwd + " " + evtSrchEnd_DyFwd + 
	//	" " + prcRef_t + " " + ptsTarget + " " + blLong);
    double prc_ij;	 

    int begCol_d;
    int endCol_d;
    
    for (int idyfwd=evtSrchBeg_DyFwd; idyfwd<=evtSrchEnd_DyFwd; idyfwd++) {	
      if(i + idyfwd > session.endTstDateIndex)
        return "";
      
      if (idyfwd == evtSrchBeg_DyFwd) {   //* also good for idyfwd == evtSrchBeg_DyFwd == evtSrchEnd_DyFwd   	
          if(evtFrameBeg_TimeCol > evtSrchBeg_TimeCol)
            begCol_d = evtFrameBeg_TimeCol;
          else 
            begCol_d = evtSrchBeg_TimeCol; 
      } else {
      	  if(evtFrameBeg_TimeCol > InstrDep.firstTimeCol)
      	    begCol_d = evtFrameBeg_TimeCol;
      	  else
      	    begCol_d = InstrDep.firstTimeCol;
      }
      
      if (idyfwd < evtSrchEnd_DyFwd) {
      	  if(evtFrameEnd_TimeCol < InstrDep.lastTimeCol)
      	    endCol_d = evtFrameEnd_TimeCol;
      	  else 
      		endCol_d = InstrDep.lastTimeCol;
      } else {  	  //* also good for idyfwd == evtSrchBeg_DyFwd == evtSrchEnd_DyFwd
      	  if(evtFrameEnd_TimeCol < evtSrchEnd_TimeCol)
            endCol_d = evtFrameEnd_TimeCol;
      	  else 
      		endCol_d = evtSrchEnd_TimeCol;
      }          
      
      for (int j=begCol_d; j<=endCol_d; j++) {  //* go across time
        prc_ij = InstrDep.prc[i + idyfwd][j];
        
        /*  blLong: long profit, short stop
         * !blLong: short profit, long stop
         */
        if ((blLong && prc_ij >= prcRef_t + ptsTarget) ||
           (!blLong && prc_ij <= prcRef_t - ptsTarget)) {

            return (i + idyfwd) + "," + j + "," + prc_ij;
        }        
      }  //*  for look across in time 
    }  //* for look fwd in days

    //* quite possible no event entry given cond dy
    return "";
  }
  
  
}	

