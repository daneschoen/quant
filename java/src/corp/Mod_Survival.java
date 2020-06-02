package program;

import java.util.Hashtable;
import java.text.SimpleDateFormat;
import java.util.Date;

public class Mod_Survival {
  
  //* These get set from Gui, thus static	  
  public int CmdiExitDysFwd;
  public String CmdstrExitTime = "";
  public int CmdiExitCol;
  public String CmdstrWait0ExitTime = "";
  public int CmdiWait0ExitCol;
  
  private double[] plUnreal;
  private Hashtable<Integer, Integer[]> trades;
  private int totTrades;                                  
  
  private static final int TOT_WAIT = 14;
  //* 1-10, 11-15, 16-20, 21-25, >25 are 
  private int parWaitTime;
  private int parExitType;
  
  private Session session;
  private Instr InstrDep;
  
  public String strView="";
  
  
  public Mod_Survival(Session session) {
	this.session = session;
	InstrDep = session.InstrDep;
  }
  
  
  public void runAndConstructView() throws Exception{
		  
	try {
	  plUnreal = new double[InstrDep.prc.length];
	  trades = new Hashtable<Integer, Integer[]>();  
	  parExitType = 0;  
	  strView = constructHeader();
	  for (int t=0; t<TOT_WAIT; t++) {
		parWaitTime = t+1;  
	    calc();
	    strView += constructStats();
	  }
	  plUnreal = new double[InstrDep.prc.length];
	  trades = new Hashtable<Integer, Integer[]>();  
	  parExitType = 1;  //* ie wait = 0
	  for (int t=0; t<TOT_WAIT; t++) {
		parWaitTime = t+1;  
	    calc();
	    strView += constructStats();
	  }
	  
	} catch(Exception e) {	  
	  strView = "ERROR - Survival - runAndConstructView: " + e.toString();
	}
	
  }
  
  
  private String constructHeader() {
	StringBuilder strb = new StringBuilder();  
	
	strb.append("Survival\n");
	SimpleDateFormat sdfDtime = new SimpleDateFormat("MM/dd/yyyy HH:mm:ss");
	String strText = sdfDtime.format(new Date());
	strb.append("Ran at " + strText + "\n");
	strText = "Calculation results for " + InstrDep.idName + 
      " from " + sdfDtime.format(InstrDep.prcDate[session.begTstDateIndex].getTime()) +
	  " to " + sdfDtime.format(InstrDep.prcDate[session.endTstDateIndex].getTime());
	strb.append(strText + "\n");
	strText = "Reference time at " + InstrDep.prcDate[session.entryfixed_timecol];
	strb.append(strText + "\n\n");
	strb.append("Entry Conditions:\n");  
	for(String[] strCmds: session.arrCmdEntryDy)
      if(strCmds[1] == "not")
        strb.append("not " + strCmds[0] + "\n");
      else
    	strb.append(strCmds[0] + "\n"); 
	strb.append("\n");	
    
    return strb.toString();
  }
  
  
  private String constructStats() {
    double totPl = 0;
	double muPl = 0; //* totPts/trade
	double stdev = 0;
	double totHoldPer = 0;
	double avgHoldPer = 0;
	double maxHoldPer = 0;
	double minHoldPer = Double.MAX_VALUE;
	double maxDrawDn = 0;
	double maxDrawUp = 0;
	double maxPl = -Double.MAX_VALUE;
	double minPl = Double.MAX_VALUE;
	double ppos=0;
	double statT;
	int iEnterIndex;
	int iExitIndex;
	int jEnterTimeCol;
	int jExitTimeCol;
	double prcEnterAt;
	double prcExitAt;
	double[] plTrades = new double[totTrades+1];  //* NOTE: Index starts from 1!
	
	StringBuilder strb = new StringBuilder();

	//* Now calc PL - realized and unrealized - and stats 
	double holdPer = 0;
    for (int t=1; t<=totTrades; t++) {
      Integer[] tradeInfo = trades.get(t);
      iEnterIndex = tradeInfo[0];
      jEnterTimeCol = tradeInfo[1];
      iExitIndex = tradeInfo[2];
      jExitTimeCol = tradeInfo[3];
      
      prcEnterAt = InstrDep.prc[iEnterIndex][jEnterTimeCol];
      prcExitAt = InstrDep.prc[iExitIndex][jExitTimeCol];
      
      //* PL (realized) PER TRADE!
      totPl += (prcExitAt - prcEnterAt);
      plTrades[t] = prcExitAt - prcEnterAt;
      
      //* Holding periods - duration
      holdPer = (iExitIndex - iEnterIndex - 1); 
      holdPer += (((InstrDep.clsDyCol-jEnterTimeCol+1.0) + (jExitTimeCol-InstrDep.opnDyCol))/(InstrDep.clsDyCol-InstrDep.opnDyCol+1.0));     
      if (holdPer > maxHoldPer) {
    	  maxHoldPer = holdPer;  
      }
      if (holdPer < minHoldPer) {
    	  minHoldPer = holdPer;  
      }
      totHoldPer += holdPer;
      
    }

    //* Unrealized PL
    for (int i=session.begTstDateIndex; i<=session.endTstDateIndex; i++) {
    	
      for (int t=1; t<=totTrades; t++) {
        Integer[] tradeInfo = trades.get(t);
        iEnterIndex = tradeInfo[0];
        jEnterTimeCol = tradeInfo[1];
        iExitIndex = tradeInfo[2];
        jExitTimeCol = tradeInfo[3];
        
        if (iExitIndex == i) {
            prcEnterAt = InstrDep.prc[iEnterIndex][jEnterTimeCol];
            prcExitAt = InstrDep.prc[iExitIndex][jExitTimeCol];
            plUnreal[iExitIndex] += (prcExitAt - prcEnterAt);    
        }
      }
      
      if (i > session.begTstDateIndex) {
          plUnreal[i] += plUnreal[i-1];	  
      }
      
    }

	//for (int i=Strategy.begTstDateIndex; i<=Strategy.endTstDateIndex; i++) {    
	//	System.out.println(plUnreal[i]);
	//}
    
    avgHoldPer = totHoldPer/totTrades;
    
    muPl = totPl/totTrades;
    
    //* stdev
	for (int t=1; t<=totTrades; t++) {
	  stdev += Math.pow((plTrades[t] - muPl),2);
    }
	stdev /= (totTrades-1);  //* unbiased
    stdev = Math.sqrt(stdev);
    statT = (muPl/stdev)*Math.sqrt(totTrades)*100;
    
    //* max and min pl, ppos
	for (int t=1; t<=totTrades; t++) {
	  if (plTrades[t] > maxPl) {
		  maxPl = plTrades[t];  
	  }
	  if (plTrades[t] < minPl) {
		  minPl = plTrades[t];  
	  }	  
	  
	  if (plTrades[t] > 0) {
		  ppos = ppos + 1.0;
	  }
    }
	ppos /= totTrades;
	ppos *= 100.0;
    
    //* maxDrawDn and maxDrawUp
    double plDn;
    double plUp;
    for (int i=session.begTstDateIndex; i<=session.endTstDateIndex; i++) {
      for (int k=i+1; k<=session.endTstDateIndex; k++) {
    	if (plUnreal[k] < plUnreal[i]) {
            plDn = plUnreal[i] - plUnreal[k];
            if (plDn > maxDrawDn) {
        	    maxDrawDn = plDn;
            }
    	} else {
    	    break;	
    	}
      }
      //* now got biggest drop having returned to local peak level
      for (int k=i+1; k<=session.endTstDateIndex; k++) {
      	if (plUnreal[k] > plUnreal[i]) {
            plUp = plUnreal[k] - plUnreal[i];
            if (plUp > maxDrawUp) {
          	    maxDrawUp = plUp;
            }
      	} else {
      	    break;	
      	}
      }
      //* now got biggest peak having returned to local valley level
    }
    
    //* Now the stats results
    //* header first
	strb.append("\n");  
	if (parWaitTime==1) {
        if (parExitType==0) {
        	strb.append("Time Exit: " + CmdiExitDysFwd + " " + CmdstrExitTime + "\n");
        	strb.append(String.format("%5s","Wait"));
        	strb.append(String.format("%10s","N"));
        	strb.append(String.format("%10s","Max"));
        	strb.append(String.format("%10s","Min"));
        	strb.append(String.format("%10s","Mu"));
        	strb.append(String.format("%10s","Ppos"));
        	strb.append(String.format("%10s","Sdev"));
        	strb.append(String.format("%10s","T"));
        	strb.append("\n");
        } else if (parExitType==1) {
        	strb.append("\nTime Exit: WAIT=0 " + CmdstrWait0ExitTime + "\n");
        	strb.append(String.format("%5s","Wait"));
        	strb.append(String.format("%10s","N"));
        	strb.append(String.format("%10s","Max"));
        	strb.append(String.format("%10s","Min"));
        	strb.append(String.format("%10s","Mu"));
        	strb.append(String.format("%10s","Ppos"));
        	strb.append(String.format("%10s","Sdev"));
        	strb.append(String.format("%10s","T"));
        	strb.append(String.format("%10s","Avg Dur"));
        	strb.append("\n");
        }
	}  
    if (parWaitTime==11) {
    	strb.append(String.format("%5s", "11-15"));  
    } else if (parWaitTime==12) {
    	strb.append(String.format("%5s", "16-20"));
    } else if (parWaitTime==13) {
    	strb.append(String.format("%5s", "21-25"));
    } else if (parWaitTime==14) {
    	strb.append(String.format("%5s", ">25"));    	
    } else {	
    	strb.append(String.format("%5d", parWaitTime));
    } 
    
    //* Now the stats results
    strb.append(String.format("%10d", totTrades));
    if (totTrades > 0) {
    	strb.append(String.format("%10.2f", maxPl));
    	strb.append(String.format("%10.2f", minPl));
    	strb.append(String.format("%10.2f", muPl));
    	strb.append(String.format("%10.2f", ppos));
    	strb.append(String.format("%10.2f", stdev));
    	strb.append(String.format("%10.2f", statT));
        if (parExitType==1) {
        	strb.append(String.format("%10.2f", avgHoldPer));
        }	    
    }
    
    return strb.toString();
  }  //* method: calc and display stats
  
  
  public void calc() throws Exception{  

    Trades trds = new Processor(session).run_entry_dy();
        	                 
    int enterCol = session.entryfixed_timecol;
    int cntTrades = 0;
    Integer[] tradeInfo;
    for (int i=session.begTstDateIndex; i<=session.endTstDateIndex; i++) {
       	  	
      if (trds.conditionDy[i] != 1) {
          boolean blOccured = false;
          int cntM = 0;
          int n = 1;
          while (i-n >= session.begTstDateIndex && !blOccured) {
    	    if (trds.conditionDy[i-n] != 1) {			  
    		    cntM++;
    		    n++;
    	    } else {
    		    blOccured = true;
    	    }
          }  
      
          if ((parWaitTime <= 10 && cntM+1 == parWaitTime) ||
              (parWaitTime == 11 && cntM+1 >= 11 && cntM+1 <= 15)  ||
              (parWaitTime == 12 && cntM+1 >= 16 && cntM+1 <= 20)  ||
              (parWaitTime == 13 && cntM+1 >= 21 && cntM+1 <= 25)  ||
              (parWaitTime == 14 && cntM+1 > 25)) {
    	      if (parExitType == 0) {  //* exit dysfwd 
    		    if (i+CmdiExitDysFwd <= session.endTstDateIndex) {
    	            cntTrades++;
    		        tradeInfo = new Integer[4];
    		        tradeInfo[0] = i;
    		        tradeInfo[1] = enterCol;
    		        tradeInfo[2] = i+CmdiExitDysFwd;
    		        tradeInfo[3] = CmdiExitCol;
    			    trades.put(cntTrades, tradeInfo);  //* note index starts from 1! 
    	        }  
    	      } else if (parExitType == 1) { //* exit when WAIT=0
    	          for (int k=i+1; k<=session.endTstDateIndex; k++) {
      		        if (trds.conditionDy[k] == 1) {
      	                cntTrades++;
      		            tradeInfo = new Integer[4];
      		            tradeInfo[0] = i;
      		            tradeInfo[1] = enterCol;
      		            tradeInfo[2] = k;
      		            tradeInfo[3] = CmdiWait0ExitCol;
      			        trades.put(cntTrades, tradeInfo);  //* note index starts from 1! 
      		    	    break;
      		        }
      	          }  
    	      }  //* if parExitType
          }  //* if wait=1,2,3, ...	      
      }  //* if entered             	  	  	  
    }  //* i for loop
   
    totTrades = cntTrades;
  }  //* calc method
	
}	

