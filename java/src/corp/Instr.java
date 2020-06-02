package program;

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.HashMap;
import java.util.Map;


public class Instr {	
	
  public int key;
  public String idName;
  
  public String fileDailyName;
  public String fileMinName;
  public int fileDailyStartRow;
  public int fileMinStartRow; 
  
  public String fileOut10MinName;
  public String fileOut5MinName;
  public String fileOut1MinName;
  
  public String fileDelim;
  public String fileDateFormat;
  public String fileTimeFormat;
  
  public int fileMinDateCol;
  public int fileMinTimeCol;
  public int fileMinOpnCol;
  public int fileMinHiCol;
  public int fileMinLoCol;
  public int fileMinClsCol;
  public int fileDailyDateCol;
  public int fileDailyOpnCol;
  public int fileDailyHiCol;
  public int fileDailyLoCol;
  public int fileDailyClsCol;
  
  public String fileHolName;
  public String fileExcludeName;
  public double dollarval;
  public double optimalFmult;
    
  public int precPrcLblShow;
  public double precPrcShow;
  public int precStatsLblShow;
  public double precStatsShow;
  public double mult;
  
  public String firstDyTimeStamp;
  public String opnTimeStamp;  
  public String clsTimeStamp;
  public String clsTimeStampFile;  //* used for cls of cls (instead of opn for all other times)
  public String clsTimeStampSkipFile;  //* FOR ALGORITHM USING OPN'S OF NEXT TIME
  public String begHiLoTimeStamp;
  public String endHiLoTimeStamp;
  
  public int minIncr;
  public int totTimeSteps;
  
  public int opnDyCol;
  public int clsDyCol;
  public int hiDyCol;  
  public int loDyCol;
  //public int hiDy2Col;  
  //public int loDy2Col;  
  //public int hi24Col;  
  //public int lo24Col;
  
  public int modCol;        //* modified col
  public int firstTimeCol;  //* should be 930 or 0000 or 0600
  public int lastTimeCol;   //* should be 1615 or 2355 or 2359
  public int lastHdrCol;    //* includes all hi,lo's
  public int lastCol;
  
  public int opnNtCol;      //* night session : but Sun, hol's different!
  public int opnNt2Col;
  
  public int begRawCol;         // first data time if rawraw format is needed
  public int endRawCol;         // last data time "
  public int maxPrcCol;         // last price col

  public double[] hiloPtsArray;   
  
  public int tstRow0;
  public int tstRowN;  
  
  public String[] prcTime;
  public double [][] prc;       // = new double[MaxRow][MaxCol];
                                //* mt, dy, yr, dwk, 0000, 0001, ..., 0930,..., 1615,..., 2359, hi, lo, hi0600, lo0600, mod
  public Date[] prcDate;        // = new Calendar[MaxRow];
  public int maxDysBk;

  //public MappedByteBuffer mapPrices;
  
  
  public boolean blImported;
  
  /* Multiton pattern is similar to the Singleton, which allows only one instance of a class to be created, 
   * but expands on the Singleton concept to manage a map of named instances as key/value pairs. Rather than
   * have a single instance per application (e.g. the java.lang.Runtime object in the Java programming language) 
   * the Multiton pattern instead ensures a single instance per key. 
   * 
   * While it may appear that the Multiton is no more than a simple hash table with synchronized access there 
   * are two important distinctions. First, the multiton does not allow clients to add mappings. Secondly, 
   * the multiton never returns a null or empty reference; instead, it creates and stores a Multiton instance on 
   * the first request with the associated key. Subsequent requests with the same key return the original 
   * instance. A hash table is merely an implementation detail and not the only possible approach. The pattern 
   * simplifies retrieval of shared objects in an application. Since the object pool is created only once, being 
   * a member associated with the class (instead of the instance), the Multiton retains its flat behavior rather 
   * than evolving into a tree structure. The Multiton is unique in that it provides centralized access to a 
   * single directory (i.e. all keys are in the same namespace, per se) of Multitons, where each Multiton 
   * instance in the pool may exist having its own state. In this manner, the pattern advocates indexed storage 
   * of essential objects for the system (such as would be provided by an LDAP system, for example). However, a 
   * Multiton is limited to wide use by a single system rather than a myriad of distributed systems. 
   */
  
  /*
     Eager initializtion
    - The instance is not constructed until the class is used.
    - There is no need to synchronize the getInstance() method, meaning all threads will see the same instance and no (expensive) locking is required.
    - The final keyword means that the instance cannot be redefined, ensuring that one (and only one) instance ever exists.
   
    public class Singleton {
	   private static final Singleton _instance = new Singleton();
	   
	   private Singleton() {}

	   public static Singleton getInstance() {
	      return _instance;
	   }
    }
  
    Singleton singleton = Singleton.getInstance();
  
  */
  
  private static final Map<Integer, Instr> instances = new HashMap<Integer, Instr>();
  
  
  private Instr() {  //* also acceptable: protected, {default}
    /* NO explicit implementation */}
  
  
  public static Instr getInstance(Integer iKey) {
      synchronized (instances) {
          Instr instance = (Instr) instances.get(iKey);  // cast not needed I think

          if (instance == null) {
          //if ((instance = instances.get(key)) == null) {
              instance = new Instr();
              instances.put(iKey, instance);
              InstrSpecs.setupSpecs(instance, iKey);
          }
          return instance;
      }
  }  
  
  private SimpleDateFormat sdfDtime = new SimpleDateFormat("MM/dd/yyyy HH:mm");
  private SimpleDateFormat sdfMM = new SimpleDateFormat("MM");
  private SimpleDateFormat sdfdd = new SimpleDateFormat("dd");
  private SimpleDateFormat sdfyyyy = new SimpleDateFormat("yyyy");   
  
  int getWeekday(int iDayIndex) {
	Calendar cal_i = new GregorianCalendar();
	cal_i.setTime(this.prcDate[iDayIndex]);
	return cal_i.get(Calendar.DAY_OF_WEEK)-1;  //* sun: 1 => 0
  }
  
  int getWeek(int iDayIndex) {
	Calendar cal_i = new GregorianCalendar();
	cal_i.setTime(this.prcDate[iDayIndex]);
	return cal_i.get(Calendar.WEEK_OF_MONTH);  
  }
  
  String getYear(int iDayIndex) {
    return sdfyyyy.format(this.prcDate[iDayIndex].getTime());
  }  
  
  String getMonth(int iDayIndex) {
	return sdfMM.format(this.prcDate[iDayIndex].getTime());
  }
  
  String getDay(int iDayIndex) {
	return sdfdd.format(this.prcDate[iDayIndex].getTime());
  }    
  
  int getTimeCol(String strTime) {
	//* 1:25 125 0125 01:25 c o
	if (strTime.equals("c")) {
		return this.clsDyCol;
	} else if (strTime.equals("o")) {
		return this.opnDyCol;
	} else if (strTime.contains(":") && strTime.length() < 5) { 
      strTime = "0" + strTime;	            
    } else if (!strTime.contains(":") && strTime.length() < 4) { 
        strTime = "0" + strTime;	  
        strTime = strTime.substring(0,2) + ":" + strTime.substring(2);
    } else if (!strTime.contains(":") && strTime.length() == 4) {
    	strTime = strTime.substring(0,2) + ":" + strTime.substring(2);
    }
    
    int jTimeCol = firstTimeCol;
    while(jTimeCol <= lastTimeCol && !strTime.equals(prcTime[jTimeCol])) 
      jTimeCol++;
    
    if (jTimeCol > lastTimeCol)
      return -1;
    else
      return jTimeCol;
  }
  
}

