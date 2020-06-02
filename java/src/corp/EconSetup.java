package program;


public class EconSetup {
	
	public final static int TOT_ECON = 16;
	public static String name[] = new String[TOT_ECON];
	public static String fileName[] = new String[TOT_ECON];
	
	public static void initialize() {	
	  //* Called by StrategyApp in order for GUI Import btn to know which to import
	  //* these are the key names (in str)	
      name[0] = "holes";
      name[1] = "holda";
      name[2] = "holus";
      name[3] = "holty";
      name[4] = "holec";
      name[5] = "holcl";
      name[6] = "holnk";
      
	  name[7] =  "econemp";
	  name[8] =  "econfomc";
	  name[9] =  "econexp";
	  name[10] = "econnonq";
	  name[11] = "econquar";
	  name[12] = "econppi";
	  name[13] = "econcpi";
	  name[14] = "econlead";
	  name[15] = "econgdp";	
	}
	
	public static void setupSpecs(Econ EconX, String strEconNameKey) {
	  //Instr InstrX = Instr.getInstance(instrKey);

	  strEconNameKey = strEconNameKey.trim();
	  strEconNameKey = strEconNameKey.toLowerCase();
	  for (int k=0; k<TOT_ECON; k++) {
        if (name[k].equalsIgnoreCase(strEconNameKey)) {
            EconX.name = name[k];
            EconX.fileName = name[k] + ".txt";
            break;
        }
	  }

      EconX.blImported = false;
      
	  //Calendar dates = new GregorianCalendar();
	  //dates.set(2006, 0, 15);
	  //Calendar[] dates = new GregorianCalendar[MaxRow];
	  //Calendar[] dates = new Calendar[MaxRow];
	}  
		  
}
