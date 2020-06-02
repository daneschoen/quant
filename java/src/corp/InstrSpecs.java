package program;

//* Called by Gui just to populate dropdowns
//* Called by Instr to setup
//* Called by Strategy_Compare
//* Called by StrategyApp

public class InstrSpecs {
  
  public final static int TOT_INSTRS = 7;   //* MUST UPDATE THIS W NEW INSTR'S !
  public static String idNames[] = new String[TOT_INSTRS];
	
  
  public static void initialize() {		
	/* 
	 * MUST UPDATE: 
	 * - EconSetup.java w following! AND TOT_INSTRS!:  
	 * - Python globals.py: ['es','da','us','ty','ec','cl','nk']
	 */
    idNames[0] = "ES";
	idNames[1] = "DA";
	idNames[2] = "US";   //* 30 year ZB
	idNames[3] = "TY";   //* 10 year note ZN 
	idNames[4] = "EC";
	idNames[5] = "CL";
	idNames[6] = "NK";
	//identifiers[x] = "GC";	bund
  }
	
  
  public static void setupSpecs(Instr InstrX, int instrKey) {
	String sym;
	
    switch (instrKey) {   
    
	 case 0:
	  /* CST! but program runs in EST!
	   * 
	   * Sun: 17:00 - 16:15
	   * M-F: 16:45 - 15:15
	   * M-F: 17:00 - 15:15, 15:30 - 16:15 
	   * trading halt from 3:15 p.m. – 3:30 p.m.
	   */		 
	  InstrX.key = instrKey;
	  InstrX.idName = idNames[instrKey];
	  
	  InstrX.fileMinName = "esdata1min24hr.asc";
	  //InstrX.fileDailyName = "esdatadaily.asc";
	  InstrX.fileHolName = "holes.txt";
      InstrX.fileExcludeName = "excludees.txt";
      InstrX.fileOut10MinName = "esdata10col.csv";
      InstrX.fileOut5MinName = "esdata5col.csv";
      InstrX.fileOut1MinName = "esdata1col.csv";
      
	  InstrX.fileDelim = AGlobal.DELIM_TICK;
	  InstrX.fileDateFormat = AGlobal.DATE_FORMAT_TICK;
	  InstrX.fileTimeFormat = AGlobal.TIME_FORMAT_TICK;
	  
	  //InstrX.fileDailyStartRow = 1;  
      InstrX.fileMinStartRow = 1;
	  InstrX.fileMinDateCol = 0;
	  InstrX.fileMinTimeCol = 1;
	  InstrX.fileMinOpnCol = 2;
	  InstrX.fileMinHiCol = 3;
	  InstrX.fileMinLoCol = 4;
	  InstrX.fileMinClsCol = 5;
	  /*
	  InstrX.fileDailyDateCol = 0;
	  InstrX.fileDailyOpnCol = 1;
	  InstrX.fileDailyHiCol = 2;
	  InstrX.fileDailyLoCol = 3;
	  InstrX.fileDailyClsCol = 4;
	  */        
	  InstrX.precPrcLblShow = 8;
      InstrX.precPrcShow =  8.2;     
	  InstrX.precStatsLblShow = 8;   
	  InstrX.precStatsShow = 8.2;    
	  
	  //* Instrument specific
	  InstrX.mult = 1;             
	  InstrX.dollarval = 250;      //* $ for 1 WHOLE point
	  InstrX.optimalFmult = 50;
	  	  
	  /*
	   * Change these for changes in times to import into program
	   */
	  InstrX.opnTimeStamp = "0930";
      InstrX.clsTimeStamp = "1615";
      InstrX.firstDyTimeStamp = "0000";
      InstrX.clsTimeStampFile = InstrX.clsTimeStamp.substring(0,2) + ":" + InstrX.clsTimeStamp.substring(2);
      InstrX.clsTimeStampSkipFile = "16:16";
      InstrX.begHiLoTimeStamp = InstrX.firstDyTimeStamp;
      InstrX.endHiLoTimeStamp = InstrX.clsTimeStamp;
      
      InstrX.minIncr = 1;
	  InstrX.opnDyCol = 571-1;          //* 5min: 115-1    1min: 571-1; 
	  InstrX.clsDyCol = 976-1;          //* 5min: 196-1    1min: 976-1
	  InstrX.firstTimeCol = 0;
	  InstrX.lastTimeCol = 1440-1;      //* 5min: 288-1    1min: 1440-1 <= 60*24
		  
	  InstrX.hiDyCol = InstrX.lastTimeCol + 1;       
	  InstrX.loDyCol = InstrX.lastTimeCol + 2;
	  InstrX.modCol = InstrX.lastTimeCol + 3;  //* 0: none, 1: late open, 2: early cls, 3: both
	  InstrX.lastHdrCol = InstrX.loDyCol;   
	  InstrX.lastCol = InstrX.modCol;
	  InstrX.totTimeSteps = InstrX.lastTimeCol - InstrX.firstTimeCol + 1; // 42 for day, 124
	     
	  InstrX.hiloPtsArray = new double[9];
	  InstrX.hiloPtsArray[0] = 2.0;
	  InstrX.hiloPtsArray[1] = 5.0;
	  InstrX.hiloPtsArray[2] = 7.0;
	  InstrX.hiloPtsArray[3] = 10.0;
	  InstrX.hiloPtsArray[4] = 12.0;
	  InstrX.hiloPtsArray[5] = 15.0;
	  InstrX.hiloPtsArray[6] = 20.0;
	  InstrX.hiloPtsArray[7] = 0;     //* h1/l1
	  InstrX.hiloPtsArray[8] = 0;     //*   
	  
	  InstrX.blImported = false;
	  break;

	  
	 case 1:
	  /* dax 0900 - 1745 CET 	
	   * Frankfurt +2   NYC -4
	   */
	  InstrX.key = instrKey;
	  InstrX.idName = idNames[instrKey];
	  
	  InstrX.fileMinName = "dadata1min24hr.asc";
	  InstrX.fileHolName = "holda.txt";
      InstrX.fileExcludeName = "excludeda.txt";
      InstrX.fileOut10MinName = "dadata10col.csv";
      InstrX.fileOut5MinName = "dadata5col.csv";
      InstrX.fileOut1MinName = "dadata1col.csv";
      
	  InstrX.fileDelim = AGlobal.DELIM_TICK;
	  InstrX.fileDateFormat = AGlobal.DATE_FORMAT_TICK;
	  InstrX.fileTimeFormat = AGlobal.TIME_FORMAT_TICK;
	  
      InstrX.fileMinStartRow = 1;
	   
	  InstrX.fileMinDateCol = 0;
	  InstrX.fileMinTimeCol = 1;
	  InstrX.fileMinOpnCol = 2;
	  InstrX.fileMinHiCol = 3;
	  InstrX.fileMinLoCol = 4;
	  InstrX.fileMinClsCol = 5;
	  
	  InstrX.precPrcLblShow = 8;
      InstrX.precPrcShow =  8.2;     
	  InstrX.precStatsLblShow = 8;   
	  InstrX.precStatsShow = 8.2;    
	  
	  //* Instrument specific
	  InstrX.mult = 1;             
	  InstrX.dollarval = 250;      //* $ for 1 WHOLE point
	  InstrX.optimalFmult = 25;
	  	  
	  /*
	   * Change these for changes in times to import into program
	   */
	  InstrX.opnTimeStamp = "0300";
      InstrX.clsTimeStamp = "1600";	  
	  InstrX.firstDyTimeStamp = "0000"; //* ? 0300
      InstrX.clsTimeStampFile = InstrX.clsTimeStamp.substring(0,2) + ":" + InstrX.clsTimeStamp.substring(2);
      InstrX.clsTimeStampSkipFile = "16:01";
      InstrX.begHiLoTimeStamp = InstrX.firstDyTimeStamp;
      InstrX.endHiLoTimeStamp = InstrX.clsTimeStamp;

      InstrX.minIncr = 1;
	  InstrX.opnDyCol = 181-1;        
	  InstrX.clsDyCol = 961-1;          //* 5min: 196-1    1min: 976-1
	  InstrX.firstTimeCol = 0;
	  InstrX.lastTimeCol = 1440-1;      //* 5min: 288-1    1min: 1440-1; 
	  
	  InstrX.hiDyCol = InstrX.lastTimeCol + 1;       
	  InstrX.loDyCol = InstrX.lastTimeCol + 2;
	  InstrX.modCol = InstrX.lastTimeCol + 3;  //* 0: none, 1: late open, 2: early cls, 3: both
	  InstrX.lastHdrCol = InstrX.loDyCol;   
	  InstrX.lastCol = InstrX.modCol;
	  InstrX.totTimeSteps = InstrX.lastTimeCol - InstrX.firstTimeCol + 1; 

	  InstrX.hiloPtsArray = new double[9];
	  InstrX.hiloPtsArray[0] = 25.0;
	  InstrX.hiloPtsArray[1] = 50.0;
	  InstrX.hiloPtsArray[2] = 75.0;
	  InstrX.hiloPtsArray[3] = 100.0;
	  InstrX.hiloPtsArray[4] = 125.0;
	  InstrX.hiloPtsArray[5] = 175.0;
	  InstrX.hiloPtsArray[6] = 200.0;
	  InstrX.hiloPtsArray[7] = 0;
	  InstrX.hiloPtsArray[8] = 0;	  
	  
	  InstrX.blImported = false;
	  break;

	  
     case 2:
	  /* US, 30 year 
	   * FV: $100,000
	   * Min fluc: 1/64 = 0.015625
	   *           1/32 per 100 pts => $31.25 per contract
	   *           = 0.03125
	   * $1000 = 1 pt out of 100 pts
	   * SUN - FRI: 5:00 p.m. - 4:00 p.m
	   * 
	   */ 
	  InstrX.key = instrKey;
	  InstrX.idName = idNames[instrKey];
			  
	  InstrX.fileMinName = "usdata1min24hr.asc";
	  InstrX.fileOut10MinName = "usdata10col.csv";
	  InstrX.fileOut5MinName = "usdata5col.csv";
	  InstrX.fileOut1MinName = "usdata1col.csv";
	  
	  InstrX.fileHolName = "holus.txt";
	  InstrX.fileExcludeName = "excludeus.txt";
	  
	  InstrX.fileMinStartRow = 1;
	  InstrX.fileDelim = AGlobal.DELIM_TICK;
	  InstrX.fileDateFormat = AGlobal.DATE_FORMAT_TICK;
	  InstrX.fileTimeFormat = AGlobal.TIME_FORMAT_TICK;
	  InstrX.fileMinDateCol = 0;
	  InstrX.fileMinTimeCol = 1;
	  InstrX.fileMinOpnCol = 2;
	  InstrX.fileMinHiCol = 3;
	  InstrX.fileMinLoCol = 4;
	  InstrX.fileMinClsCol = 5;
	  InstrX.fileDailyDateCol = 0;
	  InstrX.fileDailyOpnCol = 1;
	  InstrX.fileDailyHiCol = 2;
	  InstrX.fileDailyLoCol = 3;
	  InstrX.fileDailyClsCol = 4;	
    
	  InstrX.precPrcLblShow = 7;   //"%7s";   //* "%7s";    "%10s";
	  InstrX.precPrcShow = 7.0;    //"%7.0f";    //* "%7.0f";  "%10.4f";
	  InstrX.precStatsLblShow = 7;   
	  InstrX.precStatsShow = 7.0;  //7.2;    
	  
	  InstrX.mult = 100.0;
	  InstrX.dollarval = 1000;  // for 1 WHOLE point
	  InstrX.optimalFmult = 10;

	  //* open prc is opn of 0825
	  InstrX.opnTimeStamp = "0800";
      InstrX.clsTimeStamp = "1700";	  
	  InstrX.firstDyTimeStamp = "0000";
	  InstrX.clsTimeStampFile = InstrX.clsTimeStamp.substring(0,2) + ":" + InstrX.clsTimeStamp.substring(2);
	  InstrX.clsTimeStampSkipFile = "17:01";
      InstrX.begHiLoTimeStamp = InstrX.firstDyTimeStamp;
      InstrX.endHiLoTimeStamp = InstrX.clsTimeStamp;
	  
	  InstrX.minIncr = 1;
      InstrX.opnDyCol = 481-1;	
      InstrX.clsDyCol = 1021-1;
	  InstrX.firstTimeCol = 0;
	  InstrX.lastTimeCol = 1440-1;
	  
	  InstrX.hiDyCol = InstrX.lastTimeCol + 1;              
	  InstrX.loDyCol = InstrX.lastTimeCol + 2;          
	  InstrX.modCol = InstrX.lastTimeCol + 3;
	  InstrX.lastHdrCol = InstrX.loDyCol;  
	  InstrX.lastCol = InstrX.modCol;        
	  InstrX.totTimeSteps = InstrX.lastTimeCol - InstrX.firstTimeCol + 1; 

	  InstrX.hiloPtsArray = new double[9];
	  InstrX.hiloPtsArray[0] = 25.0;
	  InstrX.hiloPtsArray[1] = 50.0;
	  InstrX.hiloPtsArray[2] = 75.0;
	  InstrX.hiloPtsArray[3] = 100.0;
	  InstrX.hiloPtsArray[4] = 125.0;
	  InstrX.hiloPtsArray[5] = 150.0;
	  InstrX.hiloPtsArray[6] = 175.0;
	  InstrX.hiloPtsArray[7] = 0;     //* h1/l1
	  InstrX.hiloPtsArray[8] = 0;     //*   
	  
      InstrX.blImported = false;
	  break;

	  
     case 3:
	  /* TY, ZN, 10 year 
	   * FV: $100,000
	   * Min fluc: 1/64 = 0.015625
	   *           1/32 per 100 pts => $31.25 per contract
	   *           = 0.03125
	   * $1000 = 1 pt out of 100 pts
	   * SUN - FRI: 5:00 p.m. - 4:00 p.m
	   * 
	   */ 
	  InstrX.key = instrKey;
	  InstrX.idName = idNames[instrKey];  //* ty
	  
	  sym = InstrX.idName.toLowerCase();	  
	  InstrX.fileMinName = sym + "data1min24hr.asc";
	  InstrX.fileOut10MinName = sym + "data10col.csv";
	  InstrX.fileOut5MinName = sym + "data5col.csv";
	  InstrX.fileOut1MinName = sym + "data1col.csv";
	  InstrX.fileHolName = "hol" + sym + ".txt";
	  InstrX.fileExcludeName = "exclude" + sym + ".txt";
	  
	  InstrX.fileMinStartRow = 1;
	  InstrX.fileDelim = AGlobal.DELIM_TICK;
	  InstrX.fileDateFormat = AGlobal.DATE_FORMAT_TICK;
	  InstrX.fileTimeFormat = AGlobal.TIME_FORMAT_TICK;
	  InstrX.fileMinDateCol = 0;
	  InstrX.fileMinTimeCol = 1;
	  InstrX.fileMinOpnCol = 2;
	  InstrX.fileMinHiCol = 3;
	  InstrX.fileMinLoCol = 4;
	  InstrX.fileMinClsCol = 5;
	  InstrX.fileDailyDateCol = 0;
	  InstrX.fileDailyOpnCol = 1;
	  InstrX.fileDailyHiCol = 2;
	  InstrX.fileDailyLoCol = 3;
	  InstrX.fileDailyClsCol = 4;	
    
	  InstrX.precPrcLblShow = 7;   //"%7s";   //* "%7s";    "%10s";
	  InstrX.precPrcShow = 7.0;    //"%7.0f";    //* "%7.0f";  "%10.4f";
	  InstrX.precStatsLblShow = 7;   
	  InstrX.precStatsShow = 7.0;  //7.2;    
	  
	  InstrX.mult = 100.0;
	  InstrX.dollarval = 1000;  // for 1 WHOLE point
	  InstrX.optimalFmult = 10;

	  //* open prc is opn of 0825
	  InstrX.opnTimeStamp = "0800";
      InstrX.clsTimeStamp = "1700";	  
	  InstrX.firstDyTimeStamp = "0000";
	  InstrX.clsTimeStampFile = InstrX.clsTimeStamp.substring(0,2) + ":" + InstrX.clsTimeStamp.substring(2);
	  InstrX.clsTimeStampSkipFile = "17:01";
      InstrX.begHiLoTimeStamp = InstrX.firstDyTimeStamp;
      InstrX.endHiLoTimeStamp = InstrX.clsTimeStamp;
	  
	  InstrX.minIncr = 1;
      InstrX.opnDyCol = 481-1;	
      InstrX.clsDyCol = 1021-1;
	  InstrX.firstTimeCol = 0;
	  InstrX.lastTimeCol = 1440-1;
	  
	  InstrX.hiDyCol = InstrX.lastTimeCol + 1;              
	  InstrX.loDyCol = InstrX.lastTimeCol + 2;          
	  InstrX.modCol = InstrX.lastTimeCol + 3;
	  InstrX.lastHdrCol = InstrX.loDyCol;  
	  InstrX.lastCol = InstrX.modCol;        
	  InstrX.totTimeSteps = InstrX.lastTimeCol - InstrX.firstTimeCol + 1; 

	  InstrX.hiloPtsArray = new double[9];
	  InstrX.hiloPtsArray[0] = 25.0;
	  InstrX.hiloPtsArray[1] = 50.0;
	  InstrX.hiloPtsArray[2] = 75.0;
	  InstrX.hiloPtsArray[3] = 100.0;
	  InstrX.hiloPtsArray[4] = 125.0;
	  InstrX.hiloPtsArray[5] = 150.0;
	  InstrX.hiloPtsArray[6] = 175.0;
	  InstrX.hiloPtsArray[7] = 0;     //* h1/l1
	  InstrX.hiloPtsArray[8] = 0;     //*   
	  
      InstrX.blImported = false;
	  break;
			  
	  
    case 4:
	  /* FV: EUR 125,000 per contract
	   * Min fluc: 1pt = $.0001/EUR => 12.50 per contract
       */
  	  InstrX.key = instrKey;
	  InstrX.idName = idNames[instrKey];
			  
	  InstrX.fileMinName = "ecdata1min24hr.asc";
	  InstrX.fileOut10MinName = "ecdata10col.csv";
	  InstrX.fileOut5MinName = "ecdata5col.csv";
	  InstrX.fileOut1MinName = "ecdata1col.csv";
	  
	  InstrX.fileHolName = "holec.txt";
	  InstrX.fileExcludeName = "excludeec.txt";
	  
	  InstrX.fileMinStartRow = 1;
	  InstrX.fileDelim = AGlobal.DELIM_TICK;
	  InstrX.fileDateFormat = AGlobal.DATE_FORMAT_TICK;
	  InstrX.fileTimeFormat = AGlobal.TIME_FORMAT_TICK;
	  InstrX.fileMinDateCol = 0;
	  InstrX.fileMinTimeCol = 1;
	  InstrX.fileMinOpnCol = 2;
	  InstrX.fileMinHiCol = 3;
	  InstrX.fileMinLoCol = 4;
	  InstrX.fileMinClsCol = 5;
	  InstrX.fileDailyDateCol = 0;
	  InstrX.fileDailyOpnCol = 1;
	  InstrX.fileDailyHiCol = 2;
	  InstrX.fileDailyLoCol = 3;
	  InstrX.fileDailyClsCol = 4;
		    
	  InstrX.precPrcLblShow = 7;    //"%7s";   //* "%7s";    "%10s";
	  InstrX.precPrcShow = 7.0;     //"%7.0f";    //* "%7.0f";  "%10.4f";
	  InstrX.precStatsLblShow = 7;   
	  InstrX.precStatsShow = 7.0;   //7.2;
	  
	  InstrX.mult = 10000.0;
	  InstrX.dollarval = 125000;    // for 1 WHOLE point
	  InstrX.optimalFmult = 12.5;   
	  
	  InstrX.minIncr = 1;
	  InstrX.opnTimeStamp = "0800";
      InstrX.clsTimeStamp = "1700";	  
	  InstrX.firstDyTimeStamp = "0000";
	  InstrX.clsTimeStampFile = InstrX.clsTimeStamp.substring(0,2) + ":" + InstrX.clsTimeStamp.substring(2);	  
	  InstrX.clsTimeStampSkipFile = "17:01";
      InstrX.begHiLoTimeStamp = InstrX.firstDyTimeStamp;
      InstrX.endHiLoTimeStamp = InstrX.clsTimeStamp;
	  
      InstrX.opnDyCol = 481-1;	
      InstrX.clsDyCol = 1021-1;
	  InstrX.firstTimeCol = 0;
	  InstrX.lastTimeCol = 1440-1;
	  
	  InstrX.hiDyCol = InstrX.lastTimeCol + 1;              
	  InstrX.loDyCol = InstrX.lastTimeCol + 2;          
	  InstrX.modCol = InstrX.lastTimeCol + 3;
	  InstrX.lastHdrCol = InstrX.loDyCol;  
	  InstrX.lastCol = InstrX.modCol;        
	  InstrX.totTimeSteps = InstrX.lastTimeCol - InstrX.firstTimeCol + 1; // 42 for day, 124

	  InstrX.hiloPtsArray = new double[9];
	  InstrX.hiloPtsArray[0] = 15.0;
	  InstrX.hiloPtsArray[1] = 30.0;
	  InstrX.hiloPtsArray[2] = 50.0;
	  InstrX.hiloPtsArray[3] = 75.0;
	  InstrX.hiloPtsArray[4] = 100.0;
	  InstrX.hiloPtsArray[5] = 125.0;
	  InstrX.hiloPtsArray[6] = 150.0;
	  InstrX.hiloPtsArray[7] = 0;     //* h1/l1
	  InstrX.hiloPtsArray[8] = 0;     //*   
	  
      InstrX.blImported = false;
	  break;	
    	
	  
    case 5:  // CL
      InstrX.key = instrKey;
      InstrX.idName = idNames[instrKey];
    			  
      //* All file stuff should change according to vendor...
      InstrX.fileMinName = "cldata1min24hr.asc";
      InstrX.fileHolName = "holcl.txt";
      InstrX.fileExcludeName = "excludecl.txt";      
      InstrX.fileOut10MinName = "cldata10col.csv";
      InstrX.fileOut5MinName = "cldata5col.csv";
      InstrX.fileOut1MinName = "cldata1col.csv";
      
      InstrX.fileMinStartRow = 1;
      InstrX.fileDelim = AGlobal.DELIM_TICK;
      InstrX.fileDateFormat = AGlobal.DATE_FORMAT_TICK;
      InstrX.fileTimeFormat = AGlobal.TIME_FORMAT_TICK;
      InstrX.fileMinDateCol = 0;
      InstrX.fileMinTimeCol = 1;
      InstrX.fileMinOpnCol = 2;
      InstrX.fileMinHiCol = 3;
      InstrX.fileMinLoCol = 4;
      InstrX.fileMinClsCol = 5;
      InstrX.fileDailyDateCol = 0;
      InstrX.fileDailyOpnCol = 1;
      InstrX.fileDailyHiCol = 2;
      InstrX.fileDailyLoCol = 3;
      InstrX.fileDailyClsCol = 4;
    		    	  
      InstrX.precPrcLblShow = 7;   //"%7s";   //* "%7s";    "%10s";
      InstrX.precPrcShow = 7.0;    //"%7.0f";    //* "%7.0f";  "%10.4f";
      InstrX.precStatsLblShow = 7;   
      InstrX.precStatsShow = 7.0;  //7.2;    
      
      InstrX.mult = 100.0;
      InstrX.dollarval = 125000;   // for 1 WHOLE point
      InstrX.optimalFmult = 5;     // emini
    	  
	  InstrX.opnTimeStamp = "0800";
      InstrX.clsTimeStamp = "1615";	  
	  InstrX.firstDyTimeStamp = "0000";
	  InstrX.clsTimeStampFile = InstrX.clsTimeStamp.substring(0,2) + ":" + InstrX.clsTimeStamp.substring(2);      
	  InstrX.clsTimeStampSkipFile = "16:16";
      InstrX.begHiLoTimeStamp = InstrX.firstDyTimeStamp;
      InstrX.endHiLoTimeStamp = InstrX.clsTimeStamp;
	  
	  InstrX.minIncr = 1;
	  InstrX.opnDyCol = 481-1;          //* 5min: 115-1    1min: 571-1; 
	  InstrX.clsDyCol = 976-1;          //* 5min: 196-1    1min: 976-1
	  InstrX.firstTimeCol = 0;
	  InstrX.lastTimeCol = 1440-1;      //* 5min: 288-1    1min: 1440-1; 
	  
	  InstrX.hiDyCol = InstrX.lastTimeCol + 1;              
      InstrX.loDyCol = InstrX.lastTimeCol + 2;          
      InstrX.modCol = InstrX.lastTimeCol + 3;
      InstrX.lastHdrCol = InstrX.loDyCol;  
      InstrX.lastCol = InstrX.modCol;        
      InstrX.totTimeSteps = InstrX.lastTimeCol - InstrX.firstTimeCol + 1; 

	  InstrX.hiloPtsArray = new double[9];
	  InstrX.hiloPtsArray[0] = 20.0;
	  InstrX.hiloPtsArray[1] = 50.0;
	  InstrX.hiloPtsArray[2] = 75.0;
	  InstrX.hiloPtsArray[3] = 100.0;
	  InstrX.hiloPtsArray[4] = 125.0;
	  InstrX.hiloPtsArray[5] = 150.0;
	  InstrX.hiloPtsArray[6] = 175.0;
	  InstrX.hiloPtsArray[7] = 0;     //* h1/l1
	  InstrX.hiloPtsArray[8] = 0;     //*   
      
      InstrX.blImported = false;
      break;	
      
	 case 6:
	  /* NK 225  X? 0900 - 1745 CET 	
	   *    X? Frankfurt +2   NYC -4
	   */
	  InstrX.key = instrKey;
	  InstrX.idName = idNames[instrKey];
	  sym = InstrX.idName.toLowerCase();
	  InstrX.fileMinName = sym + "data1min24hr.asc";
	  InstrX.fileHolName = "hol" + sym +".txt";
      InstrX.fileExcludeName = "exclude" + sym + ".txt";
      InstrX.fileOut10MinName = sym + "data10col.csv";
      InstrX.fileOut5MinName = sym + "data5col.csv";
      InstrX.fileOut1MinName = sym + "data1col.csv";
      
	  InstrX.fileDelim = AGlobal.DELIM_TICK;
	  InstrX.fileDateFormat = AGlobal.DATE_FORMAT_TICK;
	  InstrX.fileTimeFormat = AGlobal.TIME_FORMAT_TICK;
	  
      InstrX.fileMinStartRow = 1;
	   
	  InstrX.fileMinDateCol = 0;
	  InstrX.fileMinTimeCol = 1;
	  InstrX.fileMinOpnCol = 2;
	  InstrX.fileMinHiCol = 3;
	  InstrX.fileMinLoCol = 4;
	  InstrX.fileMinClsCol = 5;
	  
	  InstrX.precPrcLblShow = 8;
      InstrX.precPrcShow =  8.2;     
	  InstrX.precStatsLblShow = 8;   
	  InstrX.precStatsShow = 8.2;    
	  
	  //* Instrument specific
	  InstrX.mult = 1;             
	  InstrX.dollarval = 250;      //* $ for 1 WHOLE point
	  InstrX.optimalFmult = 25;
	  	  
	  /*
	   * Change these for changes in times to import into program
	   */
	  InstrX.opnTimeStamp = "2000";
      InstrX.clsTimeStamp = "0200";	  
	  InstrX.firstDyTimeStamp = "0000"; //* ? 0300
      InstrX.clsTimeStampFile = InstrX.clsTimeStamp.substring(0,2) + ":" + InstrX.clsTimeStamp.substring(2);
      InstrX.clsTimeStampSkipFile = "02:01";
      InstrX.begHiLoTimeStamp = InstrX.firstDyTimeStamp;
      InstrX.endHiLoTimeStamp = InstrX.clsTimeStamp;

      InstrX.minIncr = 1;
	  InstrX.opnDyCol = 1201-1;        
	  InstrX.clsDyCol = 121-1;          
	  InstrX.firstTimeCol = 0;
	  InstrX.lastTimeCol = 1440-1;      //* 5min: 288-1    1min: 1440-1; 
	  
	  InstrX.hiDyCol = InstrX.lastTimeCol + 1;       
	  InstrX.loDyCol = InstrX.lastTimeCol + 2;
	  InstrX.modCol = InstrX.lastTimeCol + 3;  //* 0: none, 1: late open, 2: early cls, 3: both
	  InstrX.lastHdrCol = InstrX.loDyCol;   
	  InstrX.lastCol = InstrX.modCol;
	  InstrX.totTimeSteps = InstrX.lastTimeCol - InstrX.firstTimeCol + 1; 

	  InstrX.hiloPtsArray = new double[9];
	  InstrX.hiloPtsArray[0] = 40.0;
	  InstrX.hiloPtsArray[1] = 75.0;
	  InstrX.hiloPtsArray[2] = 125.0;
	  InstrX.hiloPtsArray[3] = 250.0;
	  InstrX.hiloPtsArray[4] = 325.0;
	  InstrX.hiloPtsArray[5] = 400.0;
	  InstrX.hiloPtsArray[6] = 500.0;
	  InstrX.hiloPtsArray[7] = 0;
	  InstrX.hiloPtsArray[8] = 0;	  
	  
	  InstrX.blImported = false;
	  break;
	        
			  
	  }  	  

	}  
		  
}
