package program;

import java.util.ArrayList;
import java.util.Map;
import java.util.TreeMap;


public class Scenario_HiLo {

  public static boolean blDoHiLo = false;	
  public static String cmdstrSearchStartExitTime;
  public static String strSearchEndExitTime;
  
  private static String strUserCmdLine;
  
  private int cmdExitTime_DysFwd;
  private int cmdExitTime_MinCol;
  private String cmdstrExitTime;
  private int cmdRefTimeCol;
  private int evtBegFrameTimeCol, evtEndFrameTimeCol;
  private int evtBegTimeCol, evtEndTimeCol;
  private int evtBegDyFwd, evtEndDyFwd;
  private int cmdStdPeriod;

  private Instr InstrDep; 		  

	//* These are all +/-  
  private double[] ptsEnter;
  private double[] zThresh = new double[5];
  private double cmdPtsEnter;
  private double cmdZThresh;
  private boolean blZ;
  private String strLvlEvent;
  private final boolean blBuy=true;


  public ArrayList<Double> listHist = new ArrayList<Double>(); 
  
  public Scenario_HiLo() {
    InstrDep = Instr.getInstance(Strategy.iDependentInstr);
    
    ptsEnter = new double[InstrDep.hiloPtsArray.length];
    
    /*	
    ptsEnter[0] = 1.0;
    ptsEnter[1] = 2.0;
    ptsEnter[2] = 5.0;
    ptsEnter[3] = 7.5;
    ptsEnter[4] = 10.0;
    ptsEnter[5] = 12.5;
    ptsEnter[6] = 15.0;
    ptsEnter[7] = 0;     //* h1/l1
    ptsEnter[8] = 0;     //*   
    */
    for(int i=0; i<InstrDep.hiloPtsArray.length; i++)
      ptsEnter[i] = InstrDep.hiloPtsArray[i];
    	
    zThresh[0] = 0.25;
    zThresh[1] = 0.50;
    zThresh[2] = 0.75;
    zThresh[3] = 1.00;
    zThresh[4] = 1.25;
  }

  
  public static void displayDefault(){  
	Gui.jtxt_Scenarios.append("HiLo(E >= p@Ref + 5, 0, C, day)\n");   	  
  }
  
  
  public static void setCmd(String strTmp) throws Exception{  
    strUserCmdLine = strTmp;   	  
  }
  
  
  public void parseAndSetConditions() throws Exception{    
    //* Does not take strCmdLine - set in SetUserOptions  
	strUserCmdLine = strUserCmdLine.trim().toLowerCase();
    if (strUserCmdLine.indexOf("hilo") < 0) {        	 	        	 
        blDoHiLo = false;
    } else {
        blDoHiLo = true;
        
        cmdRefTimeCol = Strategy.timeRefCol;
  	     
        /* "E > Ref + 5, 0, 1615, day/all"
         * "E > h1, 0, 1615, day/all"
         * "E > h(p1@0230,p1@1615), 0, 1615, day/all"
         */
  	    //List<String> params; // = new ArrayList<String>();  
  	    //for (String param : strInnerArg.split(",")) params.add(param.trim());
  	    ArrayList<String>params = ParseUtils2.getParams(strUserCmdLine);
  	    String strIntradyEvent = params.get(0);	    
  	      		
  	    if (strIntradyEvent.indexOf(">=") >= 0) {
  	    	//blBuy=true;  //* for SysTrade
	  	    if (strIntradyEvent.indexOf("h1") > 0 ||
	  	    	strIntradyEvent.indexOf("h(p1@" + InstrDep.firstDyTimeStamp +",p1@" + InstrDep.clsTimeStamp +")") > 0 
	  	       ){ 
	  	        strLvlEvent = strIntradyEvent.substring(strIntradyEvent.indexOf(">=")+2).trim(); 
	  	    } else {	
  	    	    int t_Plus = strIntradyEvent.indexOf("+"); 
  	    	    if(t_Plus < 0) 
  	    	      throw new ExceptionHiLo("ERROR in HiLo - event condition");
  		        strLvlEvent = strIntradyEvent.substring(t_Plus+1).trim();
  		        //* E >= p@Ref + 5  or
  		        //* E >= p@16:15 + 0.75z
  	  	        if (strLvlEvent.lastIndexOf("z") > 0) {
  	  	    	    blZ = true;
  	  	    	    cmdZThresh = Double.parseDouble(strLvlEvent.substring(0,strLvlEvent.lastIndexOf("z")).trim()); 	    	
  	  	    	    boolean blFound=false;
  	  	    	    for (double fdZ:zThresh) {
  	  	    	      if (fdZ == cmdZThresh) {
  	  	    	         blFound = true;
  	  	    	         break;
  	  	    	      }
  	  	    	    }
  	  	            if(!blFound)
  	  	    	      throw new ExceptionHiLo("ERROR in HiLo - Z score does not exist");
  	  	        } else {  //* must be one of the ptsEnter array 
  	  	            cmdPtsEnter = Double.parseDouble(strLvlEvent);
  	  	  	        boolean blFound=false;
  	  	  	        for (double fdPts:ptsEnter) {
  	  	  	          if (fdPts == cmdPtsEnter) {
  	  	  	    	      blFound = true;
  	  	  	    	      break;
  	  	  	          }
  	  	  	        }  
  	  	  	        if(!blFound)
  	  	  	          throw new ExceptionHiLo("ERROR in HiLo - Price event to enter does not exist");  	  	        	
  	  	        }
  	  	    }  
	  	    
  	    } else if (strIntradyEvent.indexOf("<=") >= 0) {
  	    	//blBuy=false;  //* for SysTrade
	  	    if (strIntradyEvent.indexOf("l1") > 0 ||
	  	    	strIntradyEvent.indexOf("l(p1@" + InstrDep.firstDyTimeStamp +",p1@" + InstrDep.clsTimeStamp +")") > 0
	  	       ){ 
	  	    	strLvlEvent = strIntradyEvent.substring(strIntradyEvent.indexOf("<=")+2).trim(); 
	  	    } else {
  	    	    int t_Minus = strIntradyEvent.indexOf("-"); 
  	    	    if(t_Minus < 0)  
    	          throw new ExceptionHiLo("ERROR in HiLo - event condition");
  		        strLvlEvent = strIntradyEvent.substring(t_Minus+1).trim();
  	  	        if (strLvlEvent.lastIndexOf("z") > 0) {
  	  	    	    blZ = true;
  	  	    	    cmdZThresh = Double.parseDouble(strLvlEvent.substring(0,strLvlEvent.lastIndexOf("z")).trim());
  	  	    	    boolean blFound=false;
  	  	    	    for (double fdZ:zThresh) {
  	  	    	      if (fdZ == cmdZThresh) {
  	  	    	          blFound = true;
  	  	    	          break;
  	  	    	      }
  	  	    	    }
  	  	    	    if(!blFound)
  	  	    	      throw new ExceptionHiLo("ERROR in HiLo - Z score does not exist");  	  
  	  	            strLvlEvent = "-"+strLvlEvent;
  	  	  	    } else {  //* must be one of the ptsEnter array 
  	  	  	        cmdPtsEnter = Double.parseDouble(strLvlEvent);
  	  	  	  	    boolean blFound=false;
  	  	  	  	    for (double fdPts:ptsEnter) {
  	  	  	  	      if (fdPts == cmdPtsEnter) {
  	  	  	  	    	  blFound = true;
  	  	  	  	    	  break;
  	  	  	  	      }
  	  	  	  	    }
  	  	  	  	    if(!blFound)
  	  	  	  	      throw new ExceptionHiLo("ERROR in HiLo - Price event to enter does not exist"); 
  	  	  	        strLvlEvent = "-"+strLvlEvent;
  	  	  	    }
  	  	    }   
  	  	    
  	    } else {
  	    	throw new ExceptionHiLo("ERROR in HiLo - event condition");
  	    }
        
  	    //* "b > Ref + 5, '0', 1615, day/all"
        cmdExitTime_DysFwd = Integer.parseInt(params.get(1));
        
        //* "b > Ref + 5, 0, '1615', day/all"
        cmdstrExitTime = params.get(2);
        if (cmdstrExitTime.equals("o")) {
        	cmdExitTime_MinCol = InstrDep.opnDyCol;
        } else if (cmdstrExitTime.equals("c")) {
        	cmdExitTime_MinCol = InstrDep.clsDyCol;
        } else {
        	cmdExitTime_MinCol = InstrDep.getTimeCol(cmdstrExitTime);
            if(cmdExitTime_MinCol == -1)
              throw new ExceptionHiLo("ERROR in HiLo - incorrect hold time");  
        }
        cmdstrExitTime = cmdExitTime_DysFwd + " " + cmdstrExitTime;
        
        //* "b > Ref + 5, 0, 1615, 'day/all'"
        String cmdDayOrAll = params.get(3);
        if (cmdDayOrAll.equals("day")) {
        	evtBegFrameTimeCol = InstrDep.opnDyCol;
        	evtEndFrameTimeCol = InstrDep.clsDyCol;
        } else if (cmdDayOrAll.equals("all")) {
        	evtBegFrameTimeCol = InstrDep.firstTimeCol;
        	evtEndFrameTimeCol = InstrDep.lastTimeCol;
            if(evtBegFrameTimeCol == -1 || evtEndFrameTimeCol == -1)
              throw new ExceptionHiLo("ERROR in HiLo - incorrect time for day/all");  
        } else {
        	throw new ExceptionHiLo("ERROR in HiLo - must be 'day' or 'all' ");
        }	
        
        cmdStdPeriod = 40;
            
    }  //* if blDoHiLo

  }
  
  private void runSysTrade() throws Exception{
	  
	Mod_SysTrade.strEntryDyWindow = Gui.jtxt_CmdConditions.getText();  
	Mod_SysTrade.strEntryIntradyWindow = "";
	Mod_SysTrade.strExitDyWindow = Gui.jtxt_CmdExitDy.getText();;  
	Mod_SysTrade.strExitIntradyWindow = "";	
    Mod_SysTrade.blChk_Exit_Condition = false;  
	Mod_SysTrade.blChk_Exit_ProfitTarget = false;
	Mod_SysTrade.blChk_Exit_ProfitTargetZ = false;
	Mod_SysTrade.blChk_Exit_StopLoss = false;
	Mod_SysTrade.blChk_Exit_StopLossZ = false;
	Mod_SysTrade.blChk_Exit_TimeTargetRel = false;
	Mod_SysTrade.blChk_Exit_TimeTargetFix = true;
			
	Mod_SysTrade.cmdExitTimeTarget_DysFwd = cmdExitTime_DysFwd;
	Mod_SysTrade.cmdExitTimeTarget_Col = cmdExitTime_MinCol; 	
	Mod_SysTrade.cmdExitTimeTargetStr = cmdstrExitTime;
	Mod_SysTrade.cmdMaxOpenContracts = 9999999;
	
	Mod_SysTrade mod_SysTrade = new Mod_SysTrade();
	mod_SysTrade.evtBegFrameTimeCol = evtBegFrameTimeCol; 
	mod_SysTrade.evtEndFrameTimeCol = evtEndFrameTimeCol;
	mod_SysTrade.evtBegTimeCol = evtBegTimeCol; 
	mod_SysTrade.evtEndTimeCol = evtEndTimeCol;
	mod_SysTrade.evtBegDyFwd = evtBegDyFwd; 
	mod_SysTrade.evtEndDyFwd = evtEndDyFwd;
	mod_SysTrade.blClearScreen = false;
	
	mod_SysTrade.runForHiLo(strLvlEvent, blBuy, blZ);
  }
  
  public void calc() throws Exception{  
	if (blDoHiLo) {
      calcPts();
      calcZscore();
      runSysTrade();
	} 
  }
  
  public void calcPts() throws Exception{
    
    int cntN;
    double statsMu;
    double statsPpos;
    double statsSdev;
    double statsVar;
    double statsT;
    
    double prcRef;
    double prcCur;
    double prcExit;
    
	String prec = "%" + InstrDep.precStatsLblShow + "s";  
	String hdr;
	hdr = "------------------------------ HILO THRU " + cmdExitTime_DysFwd + " " + InstrDep.prcTime[cmdExitTime_MinCol] + "------------------------------"; 
	Gui.jtextArea.append(hdr + "\n");
	Gui.jtextArea.append("SCENARIO");
	Gui.jtextArea.append(String.format("%38s","N"));
	Gui.jtextArea.append(String.format(prec,"MU"));
	Gui.jtextArea.append(String.format(prec,"PPOS"));
	Gui.jtextArea.append(String.format(prec,"SDEV"));
	prec = "%" + (InstrDep.precStatsLblShow + 2) + "s";
	Gui.jtextArea.append(String.format(prec,"T"));
	Gui.jtextArea.append("\n");
	
    //InstrDep.firstDyHrTime = 9;
	//InstrDep.firstDyMinTime = 0;  ==> 0900    
    Strat_HighLow strat_Low = new Strat_HighLow("l(p1@" + InstrDep.firstDyTimeStamp + ",p1@" + InstrDep.clsTimeStamp + ")");
    Strat_HighLow strat_High = new Strat_HighLow("h(p1@" + InstrDep.firstDyTimeStamp + ",p1@" + InstrDep.clsTimeStamp + ")");
    strat_Low.InstrX = InstrDep;
    strat_High.InstrX = InstrDep;
    strat_Low.parseAndSetConditions();
    strat_High.parseAndSetConditions();	
    
	/* Search through prc's to see if below/above hits
	 * BUT set maximum time to search all the way to exit time and day, ie (3,1615) 
	 * and stop search once found first entry!
	 */
    evtBegDyFwd = 0;
    evtEndDyFwd = cmdExitTime_DysFwd;
    evtBegTimeCol = cmdRefTimeCol;
    evtEndTimeCol = cmdExitTime_MinCol;
    
    if(Strategy.maxDysBk == 0)
      Strategy.maxDysBk = 1;
	for (int gBlwAbv=0; gBlwAbv<2; gBlwAbv++) {  //* for below x nbr of pts, then above x nbr of pts
      hdr = "----------------------------------------------------------------------------";
	  Gui.jtextArea.append(hdr + "\n");
	  for (int g=0; g<ptsEnter.length; g++) {
        cntN = 0;
        statsMu = 0.0;
        statsPpos = 0.0;
        statsSdev = 0.0;
        statsVar = 0.0;
        statsT = 0.0;
        prcRef = 0.0;
        prcExit = 0.0;
        double[] pl = new double[Strategy.cntSuccess];
      
        for (int i=Strategy.begTstDateIndex+Strategy.maxDysBk; i<=Strategy.endTstDateIndex-cmdExitTime_DysFwd; i++) {		
      	  if (Strategy.prcSuccess[i]==1) {
      		  //* Set prcRef
      		  if (g == ptsEnter.length-2) {          //* yest DAY'S low / high
      			  if(gBlwAbv==0)
        		    prcRef = InstrDep.prc[i-1][InstrDep.loDyCol];
        		  else
        		    prcRef = InstrDep.prc[i-1][InstrDep.hiDyCol];
      		  } else if (g == ptsEnter.length-1) {   //* last 1 - yest 0230 low / high
          		  if(gBlwAbv==0) {
            	    prcRef = strat_Low.calcLow(i);
          		  } else {
            		prcRef = strat_High.calcHigh(i);
          		  }		
      		  } else {	  
      			  prcRef = InstrDep.prc[i][cmdRefTimeCol];
      		  }		
              
      		  /* From here on the following should be set and thus makes general:
      		   *  evtBegFrameTimeCol, evtEndFrameTimeCol
      		   *  evtBegDyFwd, evtEndDyFwd
      		   *  evtBegTimeCol, evtEndTimeCol
      		   */
      		  boolean blFound = false;
      		  int startCol;
      		  int endCol;
      	      for (int iDysFwd=evtBegDyFwd; iDysFwd<=evtEndDyFwd; iDysFwd++) {	
      	    	  
      		    if(iDysFwd == evtBegDyFwd) 
      		      startCol = evtBegTimeCol;
      		    else 
      		      startCol = evtBegFrameTimeCol;
      		    if(iDysFwd == evtEndDyFwd) 
      		      endCol = evtEndTimeCol;  //cmdExitTime_MinCol;
      		    else 
      		      endCol = evtEndFrameTimeCol;
      		      
      		    for (int jTimeCol=startCol; jTimeCol<=endCol; jTimeCol++) {  //* go across time
      		      prcCur = InstrDep.prc[i+iDysFwd][jTimeCol];
      		      if ((gBlwAbv == 0 && prcCur + ptsEnter[g] <= prcRef) ||
      		          (gBlwAbv == 1 && prcCur >= prcRef + ptsEnter[g])) { 
      		        	
      		    	   prcExit = InstrDep.prc[i+cmdExitTime_DysFwd][cmdExitTime_MinCol];
      		    	   if(gBlwAbv == 0) 
      		    	     pl[cntN] = prcExit - prcCur;  //(prcRef - ptsEnter[g]);  //* 1200 - (1150-10)
      		    	   else
      		    	     pl[cntN] = prcExit - prcCur;  //(prcRef + ptsEnter[g]);  //* 1200 - (1210+10)    		    	    
      		    	   statsMu += pl[cntN];          
		               if(pl[cntN] > 0) statsPpos++;      
		                
		               cntN++;
		               blFound = true;
		               break;
		           }  
      		    }  //*  for look across in time 
      		    if(blFound) break;
              }  //* for look fwd in days
		  }  //* if prcSuccess
        }  //* Strategy for i loop  

        /*
         * Calc all stats
         */
        statsMu /= cntN;
	    statsPpos /= cntN;
	    statsPpos *= 100.0;
	  
	    //* var_s = 1/(N-1)*Sum(x_i - mu)^2
	    //*       = ( N*Sum(x^2) - (Sum_x)^2 ) / N(N-1)
	    for(int i=0; i<cntN;i++) 
		  statsVar += ((pl[i] - statsMu)*(pl[i] - statsMu));
	    statsVar /= (cntN-1);  // unbiased
	    statsSdev = Math.sqrt(statsVar);
	    statsT = (statsMu/statsSdev)*Math.sqrt(cntN)*100;

	    /*
	     * Print out
	     */
        String strEnter="";
        if (g < ptsEnter.length-2) {
      	    if(gBlwAbv==0) 
      	      strEnter = "Enter <= p@" + InstrDep.prcTime[cmdRefTimeCol] + " - " + String.format("%4s", ptsEnter[g]) + "    ";  
      	    else 
      		  strEnter = "Enter >= p@" + InstrDep.prcTime[cmdRefTimeCol] + " + " + String.format("%4s", ptsEnter[g]) + "    ";        	
        } else if (g == ptsEnter.length-2) {
        	if(gBlwAbv == 0)
    	      strEnter = "Enter <= L1                ";
            else
        	  strEnter = "Enter >= H1                ";
        } else if (g == ptsEnter.length-1) {
        	if(gBlwAbv == 0)
    	      strEnter = "Enter <= L(p1@" + InstrDep.firstDyTimeStamp + ",p1@" + InstrDep.clsTimeStamp + ")";
            else
              strEnter = "Enter >= H(p1@" + InstrDep.firstDyTimeStamp + ",p1@" + InstrDep.clsTimeStamp + ")";        	
        }	
        strEnter += " TO " + cmdExitTime_DysFwd +" " + InstrDep.prcTime[cmdExitTime_MinCol] + "    ";
        Gui.jtextArea.append(strEnter);
        prec = "%" + InstrDep.precStatsShow + "f";
	    Gui.jtextArea.append(String.format("%4d",cntN));
	    Gui.jtextArea.append(String.format(prec,statsMu));
	    Gui.jtextArea.append(String.format(prec,statsPpos));
	    Gui.jtextArea.append(String.format(prec,statsSdev));
	    prec = "%" + (InstrDep.precStatsShow + 2.0) + "f";
	    Gui.jtextArea.append(String.format(prec,statsT));
	    Gui.jtextArea.append("\n");
      
      }  //* g loop
	}  //* gBlwAbv loop 
	Gui.jtextArea.append("\n\n");  

  }  //* calcPts method
  
  /*
   * b > prcRef + 1.5z(c1-c2,40)
   */
  public void calcZscore() throws Exception{
	
	/*
    Strat_Abstract strat_zscore = new Strat_Zscore();
	strat_zscore.nested = 1;
	strat_zscore.parseAndSetConditions("zscore(c1-c2,40)"); 
	strat_zscore.calc();
    int maxExprDysBk = strat_zscore.maxExprDysBk;
    for (int i=Strategy.begTstDateIndex+1; i<=Strategy.endTstDateIndex-cmdExitTime_DysFwd; i++) {
      System.out.println(strat_zscore.calcdExprFn[i]);   
    }
    */
    
	/* Normally the following run, but just take what was just run...
	Parser parser = new Parser();
    parser.runConditionEntryOnly();  //* gets back Strategy.trdCondDyIndex 
	*/  
	if(Strategy.maxDysBk < cmdStdPeriod+1) 
	  Strategy.maxDysBk = cmdStdPeriod+1; 
	  
    int cntN;
    double statsMu;
    double statsPpos;
    double statsSdev;
    double statsVar;
    double statsT;
    
    double prcRef;
    double prcCur;
    double prcExit;
    
	String prec = "%" + InstrDep.precStatsLblShow + "s";  
	String hdr;
	hdr = "------------------------------ HILO THRU " + cmdExitTime_DysFwd + " " + InstrDep.prcTime[cmdExitTime_MinCol] + "------------------------------"; 
	Gui.jtextArea.append(hdr + "\n");
	Gui.jtextArea.append("SCENARIO");
	Gui.jtextArea.append(String.format("%38s","N"));
	Gui.jtextArea.append(String.format(prec,"MU"));
	Gui.jtextArea.append(String.format(prec,"PPOS"));
	Gui.jtextArea.append(String.format(prec,"SDEV"));
	prec = "%" + (InstrDep.precStatsLblShow + 2) + "s";
	Gui.jtextArea.append(String.format(prec,"T"));
	Gui.jtextArea.append("\n");
	
    evtBegDyFwd = 0;
    evtEndDyFwd = cmdExitTime_DysFwd;
    evtBegTimeCol = cmdRefTimeCol;
    evtEndTimeCol = cmdExitTime_MinCol;	
    
	double X;
	double mu_i;
	double fdStd_i;
	double fdZscore_i;
	for (int gBlwAbv=0; gBlwAbv<2; gBlwAbv++) {  //* for below x nbr of zscores, then above x zscores
      hdr = "----------------------------------------------------------------------------";
	  Gui.jtextArea.append(hdr + "\n");
	  for (int g=0; g<zThresh.length; g++) {
        cntN = 0;
        statsMu = 0.0;
        statsPpos = 0.0;
        statsSdev = 0.0;
        statsVar = 0.0;
        statsT = 0.0;
        prcRef = 0.0;
        prcExit = 0.0;
        double[] pl = new double[Strategy.cntSuccess];
      
        //* +cmdStdPeriod+1 bec going back cmdStdPeriod for C1-C2
        for (int i=Strategy.begTstDateIndex+Strategy.maxDysBk; i<=Strategy.endTstDateIndex-cmdExitTime_DysFwd; i++) {
   
      	  if (Strategy.prcSuccess[i]==1) {    		
      		X=0.0;
      	    mu_i=0.0;
    	    fdStd_i=0.0;
    	    fdZscore_i=0.0;
      		for (int k=0; k<cmdStdPeriod; k++) {
      		  X = InstrDep.prc[i-k-1][InstrDep.clsDyCol] - InstrDep.prc[i-k-2][InstrDep.clsDyCol];
              //listHist.add(X);
              //System.out.println(X);
      		  mu_i += X;
      		}  
      		mu_i /= cmdStdPeriod;
      		for (int k=0; k<cmdStdPeriod; k++) {
      		  X = InstrDep.prc[i-k-1][InstrDep.clsDyCol] - InstrDep.prc[i-k-2][InstrDep.clsDyCol];
      		  //X = Math.abs(X);
      		  fdStd_i += Math.pow(X - mu_i,2);
      		}  
      		fdStd_i /= (cmdStdPeriod-1);  //* unbiased
      		fdStd_i = Math.sqrt(fdStd_i);
      		
      		/* Now, search through prc's to see if below/above hits
      		 * BUT set maximum time to search to exit time and day, ie (3,1620) 
      		 * AND stop search once found first entry!
      		 *
      		 * ex/ Ref: 1020, hilo(0, 1500) 
      		 * ex/ Ref: C, hilo(1, 1500)
      		 */      	
      	    prcRef = InstrDep.prc[i][cmdRefTimeCol];
      		
      		boolean blFound = false;
      	    int startCol;
      		int endCol;
    	    for (int iDysFwd=evtBegDyFwd; iDysFwd<=evtEndDyFwd; iDysFwd++) {	
    	    	
        		if(iDysFwd == evtBegDyFwd) 
        		  startCol = evtBegTimeCol;
        		else 
        		  startCol = evtBegFrameTimeCol;
        		if(iDysFwd == evtEndDyFwd) 
        		  endCol = evtEndTimeCol;  //cmdExitTime_MinCol;
        		else 
        		  endCol = evtEndFrameTimeCol;
      		  
      		    for (int jTimeCol=startCol; jTimeCol<=endCol; jTimeCol++) {  //* go across time
      		        prcCur = InstrDep.prc[i+iDysFwd][jTimeCol];
      	            //fdZscore_i = (prcCur - prcRef)/fdStd_i;  
      	            fdZscore_i = (prcCur - prcRef - mu_i)/fdStd_i;  
      	            //System.out.println(fdZscore_i);         
      		        if ((gBlwAbv == 0 && fdZscore_i <= -zThresh[g]) ||
      		    	    (gBlwAbv == 1 && fdZscore_i >= zThresh[g])) {	
            	        prcExit = InstrDep.prc[i+cmdExitTime_DysFwd][cmdExitTime_MinCol];
		                //pl[cntN] = prcExit - prcCur;
  		    	        if(gBlwAbv == 0) 
  		    	          pl[cntN] = prcExit - prcCur;  //(prcRef + mu_i - (zThresh[g]*fdStd_i));
    		    	    else
    		    	      pl[cntN] = prcExit - prcCur;  //(prcRef + mu_i + (zThresh[g]*fdStd_i));
		                statsMu += pl[cntN];	          
		                if(pl[cntN] > 0) statsPpos++;  
		                cntN++;
		                blFound = true;
		                break;
		            }  
      		    }  //*  for look across in time
      		    if(blFound) break;
            }  //* for look fwd in days
		  }  //* if prcSuccess
        }  //* Strategy for i loop  
 
        /*
         * Calc all stats
         */
        statsMu /= cntN;
	    statsPpos /= cntN;
	    statsPpos *= 100.0;
	  
	    //* var_s = 1/(N-1)*Sum(x_i - mu)^2
	    //*       = ( N*Sum(x^2) - (Sum_x)^2 ) / N(N-1)
	    for(int i=0; i<cntN; i++)
		  statsVar += ((pl[i] - statsMu)*(pl[i] - statsMu));
	    statsVar /= (cntN-1);  // unbiased
	    statsSdev = Math.sqrt(statsVar);
	    statsT = (statsMu/statsSdev)*Math.sqrt(cntN)*100;

	    /*
	     * Print out
         */
        String strEnter="";
  	    if(gBlwAbv==0) 	  
	      strEnter = "Enter <= p@" + InstrDep.prcTime[cmdRefTimeCol] + " - " + String.format("%3.2f", zThresh[g]) +"z " + "   TO " + cmdExitTime_DysFwd +" " + InstrDep.prcTime[cmdExitTime_MinCol] + "    ";
	    else
		  strEnter = "Enter >= p@" + InstrDep.prcTime[cmdRefTimeCol] + " + " + String.format("%3.2f", zThresh[g]) +"z " + "   TO " + cmdExitTime_DysFwd +" " + InstrDep.prcTime[cmdExitTime_MinCol] + "    ";
        Gui.jtextArea.append(strEnter);
        prec = "%" + InstrDep.precStatsShow + "f";
	    Gui.jtextArea.append(String.format("%4d",cntN));
	    Gui.jtextArea.append(String.format(prec,statsMu));
	    Gui.jtextArea.append(String.format(prec,statsPpos));
	    Gui.jtextArea.append(String.format(prec,statsSdev));
	    prec = "%" + (InstrDep.precStatsShow + 2.0) + "f";
	    Gui.jtextArea.append(String.format(prec,statsT));
	    Gui.jtextArea.append("\n");
        
      }  //* g loop
	}  //* gBlwAbv loop 
	Gui.jtextArea.append("\n");
	
    //hist(listHist);	
  }
  
  public void hist(ArrayList<Double>listX) {  
	  Double[] buckets = new Double[103];
	  buckets[0] = -1000.0;
	  buckets[1] = -50.0;
	  buckets[102] = 1000.0;
	  for (int i=2; i<102; i++) {
		buckets[i] = buckets[i-1] + 1; 
		System.out.println(i + " " + buckets[i]);
	  }	
	  
    Map<Double,Integer> m = new TreeMap<Double,Integer>();
    for (Double fd: listX) {
     	
      int i=0;	
      for (i=0; i<buckets.length; i++) 
        if (fd <= buckets[i]) break;	// -1.75 <= -1.70    0.6 <= 0.6   
      
      Integer freq = m.get(buckets[i]);	 	
      m.put(buckets[i], (freq == null) ? 1 : freq + 1);
    	
    }
    
    for (Double key: m.keySet()) {
    	System.out.println(key + "," + m.get(key));
    }
	  
  }
	
}

