package program;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;


public class ImportEcon { 
	  
  public static void importFile(String strKeyEcon) {
		    		
    Econ EconX = Econ.getInstance(strKeyEcon);    	 

	try { 
	  String inFile_Path = AGlobal.DATA_IN_DIR + EconX.fileName;
	  File inFile = new File(inFile_Path);  
	  BufferedReader bufRdr = new BufferedReader(new FileReader(inFile));	
	    
	  String strLine = "";
	  int totRows=0;
	  while((strLine = bufRdr.readLine()) !=null)
	    totRows++;  	
	  EconX.dt = new Date[totRows];

	  /*
	  String strTmp;
	  int i = -1;  //!
	  int yr=0, dy=0, mt=0;	
	  bufRdr = new BufferedReader(new FileReader(theFile));
	  while ((strLine = bufRdr.readLine()) !=null) {
        strTmp = strLine.trim();
	    //* Parse out the date: "01/02/1996"		
	    mt = Integer.valueOf(strTmp.substring(0,2)).intValue();
	    dy = Integer.valueOf(strTmp.substring(3,5)).intValue();
	    if (strTmp.length() > 9) {
	      yr = Integer.valueOf(strTmp.substring(6,10)).intValue(); 	  
	    } else {
	       yr = Integer.valueOf(strTmp.substring(6,8)).intValue();
	       if (yr<40)  // "00, 01, 06"
		      yr += 2000;  
		   else
		      yr += 1900;  // 86,96,99    
	    }          
	    i++;
		EconX.cal[i] = new GregorianCalendar(yr,mt-1,dy,0,0,0);
		//EconX.dates[i][3] = EconX.cal[i].get(Calendar.DAY_OF_WEEK)-1;
	  }
	  bufRdr.close();
      */
	
	  DateFormat dfm = new SimpleDateFormat("MM/dd/yyyy");
	  int d=-1;
	  bufRdr = new BufferedReader(new FileReader(new File(inFile_Path)));
	  //bufRdr = new BufferedReader(new FileReader(inFile));
	  while ((strLine = bufRdr.readLine()) !=null) {
		d++;
		String[] strFields = strLine.trim().split(",");
		String strFieldDt = strFields[0];
		if (strFieldDt.length() < 10)
		  continue;
		try {
		  EconX.dt[d] = dfm.parse(strFieldDt);		
		} catch (ParseException e) {
		  e.printStackTrace();
	    }
	  }
	   	    
	  bufRdr.close();
	  
	  //>Gui.jtextArea.append("Finished importing " + EconX.fileName + "\n");
	    
	} catch (Exception e) {
		//System.err.println("Error processing file " + EconX.fileName);
		//System.err.println(e.toString());
		//>Gui.jtextArea.append("ERROR processing file " + EconX.fileName + "\n");
		//>Gui.jtextArea.append(e.toString() + "\n");
    }          
      
  } // end import fn
		
}

