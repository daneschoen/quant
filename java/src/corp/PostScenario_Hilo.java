package program;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;


public class PostScenario_Hilo {
	
  public String cmdstrSearchStartExitTime;
  public String strSearchEndExitTime;
  
  private String strUserCmdLine;
  
  private int cmdExitTime_DysFwd;
  private int cmdExitTime_MinCol;
  private String cmdstrExitTime;
  private int cmdRefTimeCol;
  private int evtFrameBegTimeCol, evtFrameEndTimeCol;
  private int evtSrchBegTimeCol, evtSrchEndTimeCol;
  private int evtSrchBegDyFwd, evtSrchEndDyFwd;
  private int cmdStdPeriod;

  //* These are all +/-  
  private double[] ptsEnter;
  private double[] zThresh = new double[5];
  private double cmdPtsEnter;
  private double cmdZThresh;
  private boolean blZ=false;
  private String strLvlEvent;
  private final boolean blBuy=true;

  private ParseUtils2 parseUtils;
  
  private Session session;
  private Instr InstrDep;
  private Trades trds;
  
  public ArrayList<Double> listHist = new ArrayList<Double>(); 

  public String strView="";
  
  
  public PostScenario_Hilo(Session session, Trades trds) {
	this.session = session;
	InstrDep = session.InstrDep;
	
	this.trds = trds;
	
	parseUtils = new ParseUtils2(session);
	
	/*
    ptsEnter = new double[InstrDep.hiloPtsArray.length];
    for(int i=0; i<InstrDep.hiloPtsArray.length; i++)
      ptsEnter[i] = InstrDep.hiloPtsArray[i];  
    */  
    ptsEnter = Arrays.copyOf(InstrDep.hiloPtsArray, InstrDep.hiloPtsArray.length);
    
    zThresh[0] = 0.25;
    zThresh[1] = 0.50;
    zThresh[2] = 0.75;
    zThresh[3] = 1.00;
    zThresh[4] = 1.25;
  }
  
  /***
   * HiLo(E >= p@Ref + 5, 0, C, day)
   * 
   * "E > Ref + 5, 0, 1615, day/all"
   * "E > h1, 0, 1615, day/all"
   * "E > h(p1@0230,p1@1615), 0, 1615, day/all"
   */
  public void parseAndSetConditions() throws Exception{    
	  
	String[] strCmdLines = parseUtils.getArrCmd(session.str_postscenario);
	for (String strCmd: strCmdLines) {		
	  if (strCmd.indexOf("hilo") == 0) {
		  strUserCmdLine = strCmd;
		  session.str_postscenario_hilo = strUserCmdLine;
	      break;
	  }
	}
    
    cmdRefTimeCol = session.entryfixed_timecol;
  	         
  	//List<String> params; // = new ArrayList<String>();  
  	//for (String param : strInnerArg.split(",")) params.add(param.trim());
  	ArrayList<String>params = parseUtils.getParams(strUserCmdLine);
  	String strIntradyEvent = params.get(0);	    
  	    
  	if (strIntradyEvent.indexOf(">=") >= 0) {
  	    //blBuy=true;  //* for SysTrade
	  	if (strIntradyEvent.indexOf("h1") > 0 ||
	  	    strIntradyEvent.indexOf("h(p1@" + InstrDep.firstDyTimeStamp +", p1@" + InstrDep.clsTimeStamp +")") > 0 
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
  	            if(!blFound && session.USERTYPE == 0)
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
  	  	        if(!blFound && session.USERTYPE == 0)
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
  	  	    	    if(!blFound && session.USERTYPE == 0)
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
  	  	  	  	    if(!blFound && session.USERTYPE == 0)
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
        	evtFrameBegTimeCol = InstrDep.opnDyCol;
        	evtFrameEndTimeCol = InstrDep.clsDyCol;
        } else if (cmdDayOrAll.equals("all")) {
        	evtFrameBegTimeCol = InstrDep.firstTimeCol;
        	evtFrameEndTimeCol = InstrDep.lastTimeCol;
            if(evtFrameBegTimeCol == -1 || evtFrameEndTimeCol == -1)
              throw new ExceptionHiLo("ERROR in HiLo - incorrect time for day/all");  
        } else {
        	throw new ExceptionHiLo("ERROR in HiLo - must be 'day' or 'all' ");
        }	
        
    cmdStdPeriod = 40;
    
  }
  
  
  public void calc() throws Exception{  
	  
	/* hilo(e >= p@ref + 5, 3, c, day)  3 c 3 975  5  
	strView = session.str_postscenario_hilo;  
    strView += cmdstrExitTime + " " + cmdExitTime_DysFwd + " "  + cmdExitTime_MinCol  +  " " +  " " + strLvlEvent; 
    strView += "CHART_DATA_LONG:\n [['07/04/2010', 3.14], ['12/25/2015', 6.22]]";
    */
	strView = calcPts();
    strView += calcZscore();
    strView += runSysTrade();   //* CONTAINS CHART_DATA_LONG !
  }
  
  public String calcPts() throws Exception{
    
    int cntN;
    double statsMu;
    double statsPpos;
    double statsSdev;
    double statsVar;
    double statsT;
    
    double prcRef;
    double prcCur;
    double prcExit;
    
    StringBuilder strb = new StringBuilder();  
    
	String prec = "%" + InstrDep.precStatsLblShow + "s";  
	String hdr;
	hdr = "------------------------------ HILO THRU " + cmdExitTime_DysFwd + " " + InstrDep.prcTime[cmdExitTime_MinCol] + "------------------------------"; 
	strb.append(hdr + "\n");
	strb.append("SCENARIO");
	strb.append(String.format("%38s","N"));
	strb.append(String.format(prec,"MU"));
	strb.append(String.format(prec,"PPOS"));
	strb.append(String.format(prec,"SDEV"));
	prec = "%" + (InstrDep.precStatsLblShow + 2) + "s";
	strb.append(String.format(prec,"T"));
	strb.append("\n");
	
    //InstrDep.firstDyHrTime = 9;
	//InstrDep.firstDyMinTime = 0;  ==> 0900    
	Strat_HighLow strat_Low = new Strat_HighLow(InstrDep, "l(p1@" + InstrDep.firstDyTimeStamp + ",p1@" + InstrDep.clsTimeStamp + ")", session);
    Strat_HighLow strat_High = new Strat_HighLow(InstrDep, "h(p1@" + InstrDep.firstDyTimeStamp + ",p1@" + InstrDep.clsTimeStamp + ")", session);
    strat_Low.parseAndSetConditions();
    strat_High.parseAndSetConditions();	
    
	/* Search through prc's to see if below/above hits
	 * BUT set maximum time to search all the way to exit time and day, ie (3,1615) 
	 * and stop search once found first entry!
	 */
    evtSrchBegDyFwd = 0;
    evtSrchEndDyFwd = cmdExitTime_DysFwd;
    evtSrchBegTimeCol = cmdRefTimeCol;
    evtSrchEndTimeCol = cmdExitTime_MinCol;
    
	for (int gBlwAbv=0; gBlwAbv<2; gBlwAbv++) {  //* for below x nbr of pts, then above x nbr of pts
      hdr = "----------------------------------------------------------------------------";
	  strb.append(hdr + "\n");
	  for (int g=0; g<ptsEnter.length; g++) {
        cntN = 0;
        statsMu = 0.0;
        statsPpos = 0.0;
        statsSdev = 0.0;
        statsVar = 0.0;
        statsT = 0.0;
        prcRef = 0.0;
        prcExit = 0.0;
        double[] pl = new double[trds.entry_dyidx.size()];
        
        for (int i=InstrDep.maxDysBk; i<=session.endTstDateIndex-cmdExitTime_DysFwd; i++) {		
      	  if (trds.conditionDy[i]==1) {
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
      		   *  evtFrameBegTimeCol, evtFrameEndTimeCol
      		   *  evtSrchBegDyFwd, evtSrchEndDyFwd
      		   *  evtSrchBegTimeCol, evtSrchEndTimeCol
      		   */
      		  boolean blFound = false;
      		  int startCol;
      		  int endCol;
      	      for (int iDysFwd=evtSrchBegDyFwd; iDysFwd<=evtSrchEndDyFwd; iDysFwd++) {	
      	    	  
      		    if(iDysFwd == evtSrchBegDyFwd) 
      		      startCol = evtSrchBegTimeCol;
      		    else 
      		      startCol = evtFrameBegTimeCol;
      		    if(iDysFwd == evtSrchEndDyFwd) 
      		      endCol = evtSrchEndTimeCol;  //cmdExitTime_MinCol;
      		    else 
      		      endCol = evtFrameEndTimeCol;

      		    
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
        strb.append(strEnter);
        prec = "%" + InstrDep.precStatsShow + "f";
	    strb.append(String.format("%4d",cntN));
	    strb.append(String.format(prec,statsMu));
	    strb.append(String.format(prec,statsPpos));
	    strb.append(String.format(prec,statsSdev));
	    prec = "%" + (InstrDep.precStatsShow + 2.0) + "f";
	    strb.append(String.format(prec,statsT));
	    strb.append("\n");
      
      }  //* g loop
	}  //* gBlwAbv loop 
	
	strb.append("\n\n");  
    return strb.toString();
    
  }  //* calcPts method
  
  /***
   * b > prcRef + 1.5z(c1-c2,40)
   */
  public String calcZscore() throws Exception{
	
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
	if(InstrDep.maxDysBk < cmdStdPeriod+1) 
	  InstrDep.maxDysBk = cmdStdPeriod+1; 
	  
    int cntN;
    double statsMu;
    double statsPpos;
    double statsSdev;
    double statsVar;
    double statsT;
    
    double prcRef;
    double prcCur;
    double prcExit;
    
    StringBuilder strb = new StringBuilder();  
    
	String prec = "%" + InstrDep.precStatsLblShow + "s";  
	String hdr;
	hdr = "------------------------------ HILO THRU " + cmdExitTime_DysFwd + " " + InstrDep.prcTime[cmdExitTime_MinCol] + "------------------------------"; 
	strb.append(hdr + "\n");
	strb.append("SCENARIO");
	strb.append(String.format("%38s","N"));
	strb.append(String.format(prec,"MU"));
	strb.append(String.format(prec,"PPOS"));
	strb.append(String.format(prec,"SDEV"));
	prec = "%" + (InstrDep.precStatsLblShow + 2) + "s";
	strb.append(String.format(prec,"T"));
	strb.append("\n");
	
    evtSrchBegDyFwd = 0;
    evtSrchEndDyFwd = cmdExitTime_DysFwd;
    evtSrchBegTimeCol = cmdRefTimeCol;
    evtSrchEndTimeCol = cmdExitTime_MinCol;	
    
	double X;
	double mu_i;
	double fdStd_i;
	double fdZscore_i;
	for (int gBlwAbv=0; gBlwAbv<2; gBlwAbv++) {  //* for below x nbr of zscores, then above x zscores
      hdr = "----------------------------------------------------------------------------";
	  strb.append(hdr + "\n");
	  for (int g=0; g<zThresh.length; g++) {
        cntN = 0;
        statsMu = 0.0;
        statsPpos = 0.0;
        statsSdev = 0.0;
        statsVar = 0.0;
        statsT = 0.0;
        prcRef = 0.0;
        prcExit = 0.0;
        double[] pl = new double[trds.entry_dyidx.size()];
      
        //* +cmdStdPeriod+1 bec going back cmdStdPeriod for C1-C2
        for (int i=InstrDep.maxDysBk; i<=session.endTstDateIndex-cmdExitTime_DysFwd; i++) {
   
      	  if (trds.conditionDy[i]==1) {    		
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
    	    for (int iDysFwd=evtSrchBegDyFwd; iDysFwd<=evtSrchEndDyFwd; iDysFwd++) {	
    	    	
        		if(iDysFwd == evtSrchBegDyFwd) 
        		  startCol = evtSrchBegTimeCol;
        		else 
        		  startCol = evtFrameBegTimeCol;
        		if(iDysFwd == evtSrchEndDyFwd) 
        		  endCol = evtSrchEndTimeCol;  //cmdExitTime_MinCol;
        		else 
        		  endCol = evtFrameEndTimeCol;
      		  
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
        strb.append(strEnter);
        prec = "%" + InstrDep.precStatsShow + "f";
	    strb.append(String.format("%4d",cntN));
	    strb.append(String.format(prec,statsMu));
	    strb.append(String.format(prec,statsPpos));
	    strb.append(String.format(prec,statsSdev));
	    prec = "%" + (InstrDep.precStatsShow + 2.0) + "f";
	    strb.append(String.format(prec,statsT));
	    strb.append("\n");
        
      }  //* g loop
	}  //* gBlwAbv loop 
	strb.append("\n");
	return strb.toString();
    //hist(listHist);	
  }
  
  
  public void histX(ArrayList<Double>listX) {  
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
    	System.out.println(key + " : + : " + m.get(key));
    }
	  
  }
  
  
  private String runSysTrade() throws Exception{
	Mod_SysTrade mod_systrade = new Mod_SysTrade(session);
    //* All the set up fr ServerApi for systrade - for this need to do here 
	mod_systrade.cmd_maxopencontract = 99999999;
	mod_systrade.cmd_bl_exit_timetarget_fix=true;
	mod_systrade.cmd_bl_exit_timetarget_rel=false;
	mod_systrade.cmd_exit_timetarget_dyfwd = cmdExitTime_DysFwd;
	mod_systrade.cmd_exit_timetarget_timecol = cmdExitTime_MinCol; 
	mod_systrade.cmd_str_exit_timetarget = cmdstrExitTime;
	
    mod_systrade.init();
	
	/* o > c1 
	 * HiLo(E >= p@Ref + 5, 0, C, day) 
	 *   means search upto +0 c, exit +0 c from entry date!
	 * 
	 * c > c1 + 20
	 * HiLo(E >= p@Ref + 5, 1, C, day) 
	 *   means search upto +1 c, exit +0 c from entry date OR +1 c fix!
	 */
	
    mod_systrade.evtFrameBeg_TimeCol = evtFrameBegTimeCol; 
    mod_systrade.evtFrameEnd_TimeCol = evtFrameEndTimeCol;
    mod_systrade.evtSrchBeg_DyFwd = evtSrchBegDyFwd; 
    mod_systrade.evtSrchEnd_DyFwd = evtSrchEndDyFwd;
    mod_systrade.evtSrchBeg_TimeCol = evtSrchBegTimeCol; 
    mod_systrade.evtSrchEnd_TimeCol = evtSrchEndTimeCol;
    
	mod_systrade.runForHiLo(strLvlEvent, blBuy, blZ);
	return mod_systrade.strView;   //* CONTAINS CHART_DATA_LONG !
  }  
	
}
