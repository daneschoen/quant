package program;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;

public class ImportExclude {
	
  public Date[] dt;   
	
  public void importFile(int instrKey) {
		
    Instr InstrX = Instr.getInstance(instrKey);    		
	    	 
    try { 
      String inFile_Path = AGlobal.DATA_IN_DIR + InstrX.fileExcludeName;

      File inFile = new File(inFile_Path);  
      BufferedReader bufRdr = new BufferedReader(new FileReader(inFile));	
		
      //* Just get count of lines in file 
	  String strLine = "";
	  int totRows=0;
	  while ((strLine = bufRdr.readLine()) !=null)
		totRows++;  	
	  
	  //* Now can set size of arrays
	  dt = new Date[totRows];

	  //* Now populate arrays with dates from exclude files
	  DateFormat dfm = new SimpleDateFormat("MM/dd/yyyy");
	  int i = -1;  //!

	  //bufRdr = new BufferedReader(new FileReader(inFile));
	  bufRdr = new BufferedReader(new FileReader(new File(inFile_Path)));
	  while ((strLine = bufRdr.readLine()) !=null) {
		i++; 
		String[] strFields = strLine.trim().split(",");
		String strFieldDt = strFields[0];
		if (strFieldDt.length() < 10)
		  continue;		
	    try {
		  dt[i] = dfm.parse(strFieldDt);		
		} catch (ParseException e) {
		  e.printStackTrace();
	    }
	  }   //* end vertical while, thus end of file
		    	    
	  bufRdr.close();
	  //Gui.jtextArea.append("Finished importing " + InstrX.fileExcludeName + "\n");
		    
	} catch (Exception e) {
      //Gui.jtextArea.append("ERROR processing file " + InstrX.fileExcludeName + "\n");
	  //Gui.jtextArea.append(e.toString() + "\n");
	}          
	      
  } //* end import fn
  
}
