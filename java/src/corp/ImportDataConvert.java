package program;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.text.DateFormat;
import java.text.Format;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;


public class ImportDataConvert {
	
  /* The raw-raw data straight out of file: 
   * read and convert into InstrX.prices[][] in the col format 
   * 
   * Needs to have imported holXY, excludeXY files first!
   * 
   * First 01h00:  < 1998  ?
   * First 24 hr:    07/01/2003
   * First sun data: 07/06/2003 
   */    
  
  private Econ econHolDates;
  private ImportExclude excludeDatesX;
  private Instr InstrX;
  
  private BufferedReader bufRdrMin;
  
  private ArrayList<Date> dtsUniqueLst;
  private String[] timeStampShifted;
  ///private String[][] timeStampShifted_DA;
  //private String[][] daDlsDtStr;
  
  private Calendar cal_i = new GregorianCalendar();
  
  
  public ImportDataConvert() {
  }
  
  /*
  public static void main(String[] args) throws Exception {
	  new ImportDataConvert().go(0);
  }
  */
  public void go(int instrKey) throws Exception{
	InstrX = Instr.getInstance(instrKey);  
	
	//Gui.jtextArea.append("Checking hol file for " + InstrX.fileDailyName + "...\n");
	//Gui.jtextArea.append("Checking exclude file for " + InstrX.fileDailyName + "...\n");  		  
			
	String strInstrSuffix = InstrSpecs.idNames[instrKey].toLowerCase();
	String strEconKey = "hol" + strInstrSuffix;   //* holus	
	econHolDates = Econ.getInstance(strEconKey);  
	
	// need to make this singleton and import static ?
	excludeDatesX = new ImportExclude();
	excludeDatesX.importFile(instrKey);
	
	String inFile_Path = AGlobal.DATA_IN_DIR + InstrX.fileMinName;
	File inFile;
	inFile = new File(inFile_Path);    
	bufRdrMin = new BufferedReader(new FileReader(inFile));
	
	setTimeStampsAndArrayDepths_24();
	
    //if(instrKey == 1)
	//  setTimeStampsAndArrayDepths_DA();
	         
    //* reset to start of file - actual prices
	bufRdrMin = new BufferedReader(new FileReader(new File(inFile_Path)));
	//if (instrKey==1)
	//  remplieMin_DA();
	//else
	remplieMin_24();
	
	//* Scrub prices
	scrubPrices_24();
	
	//* Output files
	outputNewRawFile_Xmin(1);
	outputNewRawFile_Xmin(5);
    outputNewRawFile_Xmin(10);
	
	bufRdrMin.close();	
  }
  
  
  private void setTimeStampsAndArrayDepths_24() throws Exception{
			 
    /* 0) First get nbr of rows 
	 * But in 24 version use min file for unique dates vs daily file in old version
	 */ 
	dtsUniqueLst = new ArrayList<Date>();   
	DateFormat dfmDt = new SimpleDateFormat("MM/dd/yyyy");
	int totUniqueRowDates=0;
	String strLine=null;
	Date dtPrevLine = dfmDt.parse("12/25/1900");
	Date dtCurLine;
	
	if(InstrX.fileMinStartRow == 1)   //* Header (skip)
	  strLine = bufRdrMin.readLine();	  
	
	while ((strLine = bufRdrMin.readLine()) !=null) {		  
	  String[] strFields = strLine.split(",");  
	  dtCurLine = dfmDt.parse(strFields[InstrX.fileMinDateCol]);     
	  if (!dtCurLine.equals(dtPrevLine) && !skipExcludeDates_24(dtCurLine)) {	          
	      totUniqueRowDates++;
	      dtsUniqueLst.add(dtCurLine);
	  }  
	  dtPrevLine = dtCurLine;
	}
	
	//* Now can set the array depths    
	InstrX.prc = new double [totUniqueRowDates][InstrX.lastCol+1];  //* +1 bec these are indexes!
	InstrX.prcDate = new Date[totUniqueRowDates];
	InstrX.prcTime = new String[InstrX.lastCol+1];
		
    /* 
     * 1) Now fill in just daily dates from MIN file, not daily file! 
	 */ 	
	int i=0;
	for (Date dt:dtsUniqueLst) {
	    InstrX.prcDate[i] = dt;
	    i++;
	}    
	
    /* 
	 * 2) Set up header - need this for searching p@ AND import here!
	 */
	int firstDyHrTime = Integer.parseInt(InstrX.firstDyTimeStamp.substring(0,2));
	int firstDyMinTime = Integer.parseInt(InstrX.firstDyTimeStamp.substring(2));
	Calendar timeStamp = new GregorianCalendar(2006,0,1, firstDyHrTime, firstDyMinTime,0);
	Format sdfHHmm = new SimpleDateFormat("HH:mm");
	String strTime; 
	for (int j=0; j<InstrX.totTimeSteps; j++) {  
		 strTime = sdfHHmm.format(timeStamp.getTime());
		 InstrX.prcTime[InstrX.firstTimeCol+j] = strTime;
		 timeStamp.add(Calendar.MINUTE, InstrX.minIncr);
	}
	
    /* 
	 * 3) time shift array
	 *
     * 0230 -> open of 0231
	 * 0235 -> open of 0236
	 * ...
	 * 0600 -> open of 0601
	 * 0605 -> open of 0606
	 * ...
     * 0930 -> open of 0931
	 * 1615 -> cls  of 1615
	 *
	 * eg 06:00 -> -5+1 -> 05:56 + 5 = 06:01
	 */ 
	timeStampShifted = new String[InstrX.lastTimeCol+1];
	timeStamp = new GregorianCalendar(2006,0,1, firstDyHrTime,firstDyMinTime,0);
	timeStamp.add(Calendar.MINUTE, -InstrX.minIncr+1);
	for (int j=0; j<InstrX.totTimeSteps; j++) {  
		timeStamp.add(Calendar.MINUTE, InstrX.minIncr);	
		strTime = sdfHHmm.format(timeStamp.getTime());
		timeStampShifted[j] = strTime;  
		//D System.out.println(timeStampShifted[j]);
	}
	InstrX.prcTime[InstrX.hiDyCol] = "HIGH";
	InstrX.prcTime[InstrX.loDyCol] = "LOW";
	//InstrX.prcTime[InstrX.hi24hCol] = "HIGH24h";
	//InstrX.prcTime[InstrX.lo24hCol] = "LOW24h";   
  }     
  
  /*
  private void setTimeStampsAndArrayDepths_DA() throws Exception{		
	int firstDyHrTime = Integer.parseInt(InstrX.firstDyTimeStamp.substring(0,2));
	int firstDyMinTime = Integer.parseInt(InstrX.firstDyTimeStamp.substring(2));	  
	Calendar timeStamp = new GregorianCalendar(2006,0,1, firstDyHrTime, firstDyMinTime,0);
	Format sdfHHmm = new SimpleDateFormat("HH:mm");
	String strTime; 
	
    //* Time shifts now
	timeStampShifted_DA = new String[InstrX.lastTimeCol+1][3];
	
	timeStamp = new GregorianCalendar(2006,0,1, firstDyHrTime,firstDyMinTime,0);
	timeStamp.add(Calendar.MINUTE, -InstrX.minIncr+1);
	for (int j=0; j<InstrX.totTimeSteps; j++) {  
        timeStamp.add(Calendar.MINUTE, InstrX.minIncr);	
	    strTime = sdfHHmm.format(timeStamp.getTime());
		timeStampShifted_DA[j][0] = strTime;  
	}

	timeStamp = new GregorianCalendar(2006,0,1, firstDyHrTime - 1,firstDyMinTime,0);
	timeStamp.add(Calendar.MINUTE, -InstrX.minIncr+1);	
	for (int j=0; j<InstrX.totTimeSteps; j++) {  
        timeStamp.add(Calendar.MINUTE, InstrX.minIncr);	
	    strTime = sdfHHmm.format(timeStamp.getTime());
		timeStampShifted_DA[j][1] = strTime;  
	}

	timeStamp = new GregorianCalendar(2006,0,1, firstDyHrTime + 1,firstDyMinTime,0);
	timeStamp.add(Calendar.MINUTE, -InstrX.minIncr+1);	
	for (int j=0; j<InstrX.totTimeSteps; j++) {  
        timeStamp.add(Calendar.MINUTE, InstrX.minIncr);	
	    strTime = sdfHHmm.format(timeStamp.getTime());
		timeStampShifted_DA[j][2] = strTime;  
	}		
  } 
  */
  
  private boolean skipExcludeDates_24(Date dt) {
    int h = 0;
    /*
	while (h < econHolDates.dt.length) {
	    if(econHolDates.dt[h].equals(dt))	  
		  return true;
	    h++;	
	}
	*/
    
	h=0;
	while (h < excludeDatesX.dt.length) {
	    if(excludeDatesX.dt[h].equals(dt))
		  return true;	     
		h++;		  
	}
	         
	cal_i.setTime(dt);
	if(cal_i.get(Calendar.DAY_OF_WEEK)-1 == 0 || cal_i.get(Calendar.DAY_OF_WEEK)-1 == 6)  //* sun: 1 => 0
	//if(cal_i.get(Calendar.DAY_OF_WEEK)-1 == 6)  
	  return true;
		    
	return false;        
  }    
  
  
  private void remplieMin_24() throws Exception{
	/******************************************************** 
	 * Now the price data 
	 * For every same date / totTimeSteps : put into each row 
	 * 00:00:00, 00:01:00, 00:02:00, ..., 23:59:00
	 *
	 * For es for ex:
	 * 0000 <= opn of 0001 file prc - next day! 
	 * 0930 <= opn of 0931 file prc 
	 * 0935 <= opn of 0936 file prc
	 * 1610 <= opn of 1611 file prc
	 * * 1614 <= opn of 1615 file prc
	 * * 1615 <= cls of 1615 file prc
	 * *                1616 
	 * 1616 <= opn of 1617 file prc
	 * 1620 <= opn of 1621 file prc
	 * 2355 <= opn of 2356 file prc
	 * * 2359 <= opn of 0000 file prc - next day!
	 ********************************************************/
	  
	DateFormat dfmDt = new SimpleDateFormat("MM/dd/yyyy");
	Date dtCurLine;
	Date dtPrevLine;
	String[] strFields;
	String strLine=null;	
	int j=InstrX.firstTimeCol;
	int i = -1;  //*!
	//double _hi_dy=-1.0, _lo_dy=9999999999.9;
	
	dtPrevLine = dfmDt.parse("12/25/1900");
	if(InstrX.fileMinStartRow == 1)
	  strLine = bufRdrMin.readLine();  //* skip top line (header) 
	
	while ((strLine = bufRdrMin.readLine()) !=null) {
	  strFields = strLine.split(",");  	
	  dtCurLine = dfmDt.parse(strFields[InstrX.fileMinDateCol]);
	  
	  if(skipExcludeDates_24(dtCurLine)) {
		  dtPrevLine = dtCurLine;  
	      continue;	  
	  }  
	  
	  if (!dtCurLine.equals(dtPrevLine)) {   //* new day, next day	          
          i++;
          //_hi_dy=-1.0; _lo_dy=9999999999.9;
          InstrX.prc[i][InstrX.hiDyCol] = -1.0;
          InstrX.prc[i][InstrX.loDyCol] = 9999999.9;
          if(!InstrX.prcDate[i].equals(dtCurLine))
            throw new ExceptionImport("Error - Importing: Min file date problems found: " + 
                		                   InstrX.prcDate[i] + " " + dtCurLine);	  
	  }
	  
	  dtPrevLine = dtCurLine;
	  String strCurTimeStamp = strFields[InstrX.fileMinTimeCol].substring(0,5).trim();
	  int intCurTimeStamp = Integer.parseInt(strCurTimeStamp.substring(0,2) + strCurTimeStamp.substring(3,5));
	  
	  if (strCurTimeStamp.equals(InstrX.clsTimeStampFile)) {    //* 1615
	      j = InstrX.clsDyCol;
		  InstrX.prc[i][j] = Double.valueOf(strFields[InstrX.fileMinClsCol]);
		  InstrX.prc[i][j] *= InstrX.mult;
		  
		  //* hi, lo calculations
		  //Integer x = Integer.valueOf(str);
		  if (intCurTimeStamp >= Integer.parseInt(InstrX.begHiLoTimeStamp) && intCurTimeStamp <= Integer.parseInt(InstrX.endHiLoTimeStamp)){  
			  if(InstrX.prc[i][j] > InstrX.prc[i][InstrX.hiDyCol])
				InstrX.prc[i][InstrX.hiDyCol] = InstrX.prc[i][j];
			  if(InstrX.prc[i][j] < InstrX.prc[i][InstrX.loDyCol] && InstrX.prc[i][j] > 0.0)
			    InstrX.prc[i][InstrX.loDyCol] = InstrX.prc[i][j];		  		  
		  }		  
		  
		  //* Have to take care of 1614 price, which is OPN of this time 1615
	      j = InstrX.clsDyCol - 1;
		  InstrX.prc[i][j] = Double.valueOf(strFields[InstrX.fileMinOpnCol]);
		  InstrX.prc[i][j] *= InstrX.mult;		 

		  //* hi, lo calculations
		  if (intCurTimeStamp >= Integer.parseInt(InstrX.begHiLoTimeStamp) && intCurTimeStamp <= Integer.parseInt(InstrX.endHiLoTimeStamp)){  
			  if(InstrX.prc[i][j] > InstrX.prc[i][InstrX.hiDyCol])
				InstrX.prc[i][InstrX.hiDyCol] = InstrX.prc[i][j];
			  if(InstrX.prc[i][j] < InstrX.prc[i][InstrX.loDyCol] && InstrX.prc[i][j] > 0.0)
			    InstrX.prc[i][InstrX.loDyCol] = InstrX.prc[i][j];		  		  
		  }		  
		  		                  		      
	  } else if (strCurTimeStamp.equals(InstrX.clsTimeStampSkipFile)) {       //* 16:16
		
	  } else if (strCurTimeStamp.equals("00:00")) {       //* taken care of by 00:01
	    	  
	  } else if (strCurTimeStamp.equals("23:59")) {       //* for last trade of day use cls, to avoid using  
	      j = InstrX.lastTimeCol;                         //* 00:00 of next day
		  InstrX.prc[i][j] = Double.valueOf(strFields[InstrX.fileMinClsCol])*InstrX.mult;

		  //* hi, lo calculations
		  if (intCurTimeStamp >= Integer.parseInt(InstrX.begHiLoTimeStamp) && intCurTimeStamp <= Integer.parseInt(InstrX.endHiLoTimeStamp)){  
			  if(InstrX.prc[i][j] > InstrX.prc[i][InstrX.hiDyCol])
				InstrX.prc[i][InstrX.hiDyCol] = InstrX.prc[i][j];
			  if(InstrX.prc[i][j] < InstrX.prc[i][InstrX.loDyCol] && InstrX.prc[i][j] > 0.0)
			    InstrX.prc[i][InstrX.loDyCol] = InstrX.prc[i][j];		  		  
		  }		  		  
	  } else {  //* other than cls time take opn bar for all times including open time
           //j = InstrX.firstTimeCol;	
		   j=1;   //*** !
	       //while(j<=InstrX.lastTimeCol && !strCurTimeStamp.equals(timeStampShifted[j]))
           while(j<=InstrX.lastTimeCol && !strCurTimeStamp.equals(InstrX.prcTime[j]))
		     j++;	        
	       //if (j<=InstrX.lastTimeCol && strCurTimeStamp.equals(timeStampShifted[j])) {
	       if (j<=InstrX.lastTimeCol && strCurTimeStamp.equals(InstrX.prcTime[j])) {
	    	   j = j - 1;
	           InstrX.prc[i][j] = Double.valueOf(strFields[InstrX.fileMinOpnCol]);
			   InstrX.prc[i][j] *= InstrX.mult;
               //D System.out.println(+ i + " " + j + " " + strCurTimeStamp + " " + Double.valueOf(strFields[InstrX.fileMinOpnCol]));
			   
			  //* hi, lo calculations
			  if (intCurTimeStamp >= Integer.parseInt(InstrX.begHiLoTimeStamp) && intCurTimeStamp <= Integer.parseInt(InstrX.endHiLoTimeStamp)){  
				  if(InstrX.prc[i][j] > InstrX.prc[i][InstrX.hiDyCol])
					InstrX.prc[i][InstrX.hiDyCol] = InstrX.prc[i][j];
				  if(InstrX.prc[i][j] < InstrX.prc[i][InstrX.loDyCol] && InstrX.prc[i][j] > 0.0)
				    InstrX.prc[i][InstrX.loDyCol] = InstrX.prc[i][j];		  		  
			  }		  
			   
	       }
	  }
	
	} // end vertical while, thus end of file
	    	    
	// Gui.jtextArea.append("Finished importing minute file: " + InstrX.fileMinName + "\n");
  } // end import min
  
  
  /*
  public void remplieMin_DA() throws Exception{
	   
	DateFormat dfmDt = new SimpleDateFormat("MM/dd/yyyy");
	Date dtCurLine;
	Date dtPrevLine;
	String[] strFields;
	String strLine=null;	
	int j=InstrX.firstTimeCol;
	int i = -1;  //*!	
		
	daDlsDtStr = getDaDlsDts();
	
	dtPrevLine = dfmDt.parse("12/25/1900");
	if(InstrX.fileMinStartRow == 1)
      strLine = bufRdrMin.readLine();  //* skip top line (header) 
	
	while ((strLine = bufRdrMin.readLine()) !=null) {
	  strFields = strLine.split(",");  	
	  dtCurLine = dfmDt.parse(strFields[InstrX.fileMinDateCol]);
		
	  //* Skip holidays AND exclude file routine - that may be in tick file
	  if (skipExcludeDates_24(dtCurLine)) {
		  dtPrevLine = dtCurLine;  
		  continue;	  
	  }  	  
	  
	  //* new day, next day
	  if (!dtCurLine.equals(dtPrevLine)) {   	          
		  i++;
          InstrX.prc[i][InstrX.hiDyCol] = -1.0;
          InstrX.prc[i][InstrX.loDyCol] = 9999999.9;   
	      if(!InstrX.prcDate[i].equals(dtCurLine))
	        throw new ExceptionImport("Error - Importing: Min file date problems found: " + 
	          InstrX.prcDate[i] + " " + dtCurLine);   	  
	  }
	  
	  dtPrevLine = dtCurLine;
	  String strCurTimeStamp = strFields[InstrX.fileMinTimeCol].substring(0,5).trim();
		  
	  String clsTimeStamp = InstrX.clsTimeStampFile;  //* 16:00
	  int dlsOffsetCol = 0;
	  if (getDaDlsOffset(dtCurLine) == -1) {
		  clsTimeStamp = "15:00";
		  dlsOffsetCol = 1;	  
	  } else if(getDaDlsOffset(dtCurLine) == 1) {
		  clsTimeStamp = "17:00";
		  dlsOffsetCol = 2;
	  }
			  
      if (strCurTimeStamp.equals(clsTimeStamp)) {   //* 1500, 1600, 1700
	      j = InstrX.clsDyCol;
		  InstrX.prc[i][j] = Double.valueOf(strFields[InstrX.fileMinClsCol])*InstrX.mult;
	      //D System.out.println(dtCurLine + " " + i + " " + j + " " + strCurTimeStamp + " " + Double.valueOf(strFields[InstrX.fileMinClsCol]));
      } else if (strCurTimeStamp.equals(InstrX.clsTimeStampSkipFile)) {       //* 16:16
    	  
	  } else if (strCurTimeStamp.equals("00:00")) {       //* taken care of by 00:01
			
	  } else if (strCurTimeStamp.equals("23:59")) {       //* for last trade of day use cls, to avoid using  
		  j = InstrX.clsDyCol;                            //* 00:00 of next day
		  InstrX.prc[i][j] = Double.valueOf(strFields[InstrX.fileMinClsCol])*InstrX.mult;
      } else {  //* other than cls time take opn bar for all times including open time
	      j = InstrX.firstTimeCol;
		  while(j<=InstrX.lastTimeCol && !strCurTimeStamp.equals(timeStampShifted_DA[j][dlsOffsetCol]))
		    j++;	         
		  if (j<=InstrX.lastTimeCol && strCurTimeStamp.equals(timeStampShifted_DA[j][dlsOffsetCol])) {   
		      InstrX.prc[i][j] = Double.valueOf(strFields[InstrX.fileMinOpnCol])*InstrX.mult;
	          //D System.out.println(+ i + " " + j + " " + strCurTimeStamp + " " + Double.valueOf(strFields[InstrX.fileMinOpnCol]));			      
	      }
	  }
	  		
	  //* hi, lo calculations
	  //Integer x = Integer.valueOf(str);
	  int intCurTimeStamp = Integer.parseInt(strCurTimeStamp.substring(0,2) + strCurTimeStamp.substring(3,5));
      if (intCurTimeStamp >= Integer.parseInt(InstrX.begHiLoTimeStamp) && intCurTimeStamp <= Integer.parseInt(InstrX.endHiLoTimeStamp)){
		  if(InstrX.prc[i][j] > InstrX.prc[i][InstrX.hiDyCol])
	        InstrX.prc[i][InstrX.hiDyCol] = InstrX.prc[i][j];
		  if(InstrX.prc[i][j] < InstrX.prc[i][InstrX.loDyCol])
		    InstrX.prc[i][InstrX.loDyCol] = InstrX.prc[i][j];		  		  
      }		
	  
    } // end vertical while, thus end of file
			    	    
	    //Gui.jtextArea.append("Finished importing minute file: " + InstrX.fileMinName + "\n");
  } // end import min
  */
  
  /*
  private String[][] getDaDlsDts() throws Exception {
    String daDlsDts[][] = {
	    {"03/27/2000", "03/31/2000", "-1"},
	    {"03/26/2001", "03/30/2001", "-1"},
	    {"04/01/2002", "04/05/2002", "-1"}, 
	    {"03/31/2003", "04/04/2003", "-1"}, 
	    {"03/29/2004", "04/02/2004", "-1"}, 
	    {"03/29/2005", "04/01/2005", "-1"}, 
	    {"03/27/2006", "03/31/2006", "-1"},
	    {"03/12/2007", "03/23/2007", "1"},
	    {"10/29/2007", "11/02/2007", "1"}, 
	    {"03/10/2008", "03/28/2008", "1"},
	    {"10/27/2008", "10/31/2008", "1"},
	    {"03/09/2009", "03/27/2009", "1"},
	    {"10/26/2009", "10/30/2009", "1"},
	    {"03/15/2010", "03/26/2010", "1"},
	    {"11/01/2010", "11/05/2010", "1"}  
      };
    return daDlsDts;	  
  }
  */
  
  /* 11/01/2010, 11/05/2010 : means EU DST ends 10/31, USA DST ends 11/07 0200
   * 10/29 fri: 0300 EST = 0900 EU 
   * 11/01 mon: 0300 EST = 0800 EU
   *            0300 => 0200
   *            0400 => 0300
   *            1700 => 1600 
   * 
   * 03/15/2009, 03/26/2009  
   *             
   *
   */
  /*
  private int getDaDlsOffset(Date dt) throws Exception {
	   
	DateFormat dfmDt = new SimpleDateFormat("MM/dd/yyyy");
	Date dtDlsBeg_d;
    Date dtDlsEnd_d;
	  			 		  
    for (int d=0; d<daDlsDtStr.length; d++) {
      dtDlsBeg_d = dfmDt.parse(daDlsDtStr[d][0]);
      dtDlsEnd_d = dfmDt.parse(daDlsDtStr[d][1]);
       
      if ((dt.equals(dtDlsBeg_d) ||
           dt.after(dtDlsBeg_d)) &&
          (dt.equals(dtDlsEnd_d) ||
           dt.before(dtDlsEnd_d))) {
          return Integer.parseInt(daDlsDtStr[d][2]);      
      }
    }
    return 0;
  }
  */

  public void scrubPrices_24() throws Exception {
    //* Fill fwd ONLY 	  
	  
	double lastGoodPrc = 0.0;
	for (int i=0; i<InstrX.prc.length; i++) {
	  /*	
	  if (InstrX.prc[i][InstrX.opnDyCol] == 0) {
          System.out.println(">"+InstrX.getMonth(i)+"/"+InstrX.getDay(i)+"/"+InstrX.getYear(i));		  
	  }
	  */	
      //* late open - eg 1100, 0601, etc 	
	  /*	
	  if (InstrX.prc[i][InstrX.firstTimeCol] == 0) {		  
		  //* find what time is first tick of day
		  int jLateOpn=0;
		  for (int j=InstrX.firstTimeCol; j<=InstrX.clsDyCol; j++) {
		      if (InstrX.prc[i][j] != 0) {	  
		    	  jLateOpn=j;
		    	  break;
		      }
		  }
          System.out.println("Fill bkwd - late opn - " + InstrX.getMonth(i)+"/"+InstrX.getDay(i)+"/"+InstrX.getYear(i)+" : "+InstrX.prcTime[jLateOpn]);
	      for(int j=jLateOpn-1; j>=InstrX.firstTimeCol; j--)
		    if(InstrX.prc[i][j]==0)  
			  InstrX.prc[i][j] = InstrX.prc[i][j+1];		
	  }
	  */
   	  //* early close
	  for (int j=0; j<=InstrX.lastTimeCol; j++) {	
	    if (InstrX.prc[i][j] == 0) {
	    	InstrX.prc[i][j] = lastGoodPrc;
		    // D System.out.println("Fill fwd - " + InstrX.getMonth(i)+"/"+InstrX.getDay(i)+"/"+InstrX.getYear(i)+" : "+InstrX.prcTime[j]);
	    }
	    lastGoodPrc = InstrX.prc[i][j];
      }
	  
    }
	
	//Gui.jtextArea.append("Finished Scrubbing\n");
  }
  
  
  //* Old way of scrubbing when used just day session prices 
  public void scrubPrices_Fwd_Bkd() throws Exception {
	
	for (int i=0; i<InstrX.prc.length; i++) {
	  /*	
	  if (InstrX.prc[i][InstrX.opnDyCol] == 0) {
          System.out.println(">"+InstrX.getMonth(i)+"/"+InstrX.getDay(i)+"/"+InstrX.getYear(i));		  
	  }
	  */	
      //* late open - eg 1100, 0601, etc 	
	  if (InstrX.prc[i][InstrX.firstTimeCol] == 0) {		  
		  //* find what time is first tick of day
		  int jLateOpn=0;
		  for (int j=InstrX.firstTimeCol; j<=InstrX.clsDyCol; j++) {
		      if (InstrX.prc[i][j] != 0) {	  
		    	  jLateOpn=j;
		    	  break;
		      }
		  }
          //D System.out.println(InstrX.getMonth(i)+"/"+InstrX.getDay(i)+"/"+InstrX.getYear(i)+" : "+InstrX.prcTime[jLateOpn]);
	      for(int j=jLateOpn-1; j>=InstrX.firstTimeCol; j--)
		    if(InstrX.prc[i][j]==0)  
			  InstrX.prc[i][j] = InstrX.prc[i][j+1];		
	  }
	  
   	  //* early close
	  if (InstrX.prc[i][InstrX.clsDyCol] == 0) {
		  //* find what time is early cls
		  int jEarlyCls=0;
		  for (int j=InstrX.clsDyCol-1; j>=InstrX.firstTimeCol; j--) {
		      if (InstrX.prc[i][j]!=0) {
		    	  jEarlyCls=j;
		    	  break;
		      }
		  }
	      for (int j=jEarlyCls+1; j<=InstrX.clsDyCol; j++) {
		    if(InstrX.prc[i][j]==0)
			  InstrX.prc[i][j] = InstrX.prc[i][j-1];		
	      }  
      }
	  
    }
	
	//Gui.jtextArea.append("Finished Scrubbing\n");
  }  
  
  
  public void outputNewRawFile_Xmin(int Xmin) {  
        
	  String outFile_Path = AGlobal.DATA_OUT_DIR;
	  if (Xmin==10){
		  outFile_Path += InstrX.fileOut10MinName;  
	  } else if (Xmin==5){
		  outFile_Path += InstrX.fileOut5MinName;
	  } else if (Xmin==1){
		  outFile_Path += InstrX.fileOut1MinName;
	  }
	  
	  /*
		FileOutputStream fs;
		DataOutputStream os;
		try {
		  File file = new File("C:\\MyFile.txt");
		  fs = new FileOutputStream(file);
		  os = new DataOutputStream(fs);
		  os.writeInt(2333);
		  os.writechars("msg");
		  
		} catch (IOException e) {
		  e.printStackTrace();
		}
		 
	  */
		
      try {
	    /*		
	    FileWriter fstream = new FileWriter("output.txt");
	    BufferedWriter out = new BufferedWriter(new FileWriter(File_Results));
	    out.write("blah");
	    */
				
		BufferedWriter out = new BufferedWriter(new FileWriter(outFile_Path));
		  
		//* Header - times of prices
	    String strLine = "";
		int i=0,j=0;
	    strLine = "M,D,Y,W";
	    for (j=InstrX.firstTimeCol; j<=InstrX.lastTimeCol; j++) {
	    	if(j % Xmin == 0)
	    	  strLine += "," + String.valueOf(InstrX.prcTime[j]);
	    }	
	    //* Header - hi, lo
		for(j=InstrX.lastTimeCol+1; j<=InstrX.lastHdrCol; j++)
		  strLine += "," + String.valueOf(InstrX.prcTime[j]);
		strLine += "\n";
		out.write(strLine);  
	      
		//* Body - prices and hi, lo
		strLine = "";    
		Calendar cal_i = new GregorianCalendar();
		SimpleDateFormat sdfMM = new SimpleDateFormat("MM");
		SimpleDateFormat sdfdd = new SimpleDateFormat("dd");
		SimpleDateFormat sdfyyyy = new SimpleDateFormat("yyyy");
		for (i=0; i<InstrX.prc.length; i++) {
			  //* Date fields M, D, Y, W  
			  strLine = "" + Integer.valueOf(sdfMM.format(InstrX.prcDate[i]));
			  strLine += "," + Integer.valueOf(sdfdd.format(InstrX.prcDate[i]));
			  strLine += "," + Integer.valueOf(sdfyyyy.format(InstrX.prcDate[i]));
		      
			  cal_i.setTime(InstrX.prcDate[i]);
			  strLine += "," + (cal_i.get(Calendar.DAY_OF_WEEK)-1);
			  
			  //* Now Prices
			  for(j=InstrX.firstTimeCol; j<=InstrX.lastTimeCol; j++)
				  if(j % Xmin == 0)
			        strLine += "," + String.valueOf(InstrX.prc[i][j]);
			  //* hi, lo
			  for(j=InstrX.lastTimeCol+1; j<=InstrX.lastHdrCol; j++)
			    strLine += "," + String.valueOf(InstrX.prc[i][j]);		  
			  strLine += "\n";
			  out.write(strLine);  
			  strLine = "";
	    }
			  
		out.close();
	    //Gui.jtextArea.append("Finished exporting formatted raw file\n");
	  } catch (IOException e) {
		   
		//Gui.jtextArea.append("ERROR creating formatted raw file \n");
		//Gui.jtextArea.append(e.toString() + "\n\n");
      }
	  
  }  //* Method: outputNewRawFile 		
  
  
}


