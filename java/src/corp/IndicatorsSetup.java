package program;


public class IndicatorsSetup {
	
	public static void setupSpecs(Indicators IndicatorX, String strIndicatorKey) {
	  //Instr InstrX = Instr.getInstance(instrKey);

	  strIndicatorKey = strIndicatorKey.toLowerCase();
      IndicatorX.fnName = strIndicatorKey;

      IndicatorX.blImported = false;
      
	}  
		  
}
