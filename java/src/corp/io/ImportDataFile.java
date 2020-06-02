package program.io;

import program.Gui;
import program.Indicators;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.StringTokenizer;


public class ImportDataFile {
	
  //* return data:	
  //public int [][] dates;    //* [][0]: mth, [][1]: day, [][2]: yr, [][3]: dayOfWk
  //public Calendar[] cal;
  private Indicators objData;
	
  //* inputs:
  public String fileName;
  public String strDateFormat;
  public int colDate=0;
  public int colTime=0;
  public int numDataCols=0;
  public int rowStart;
  
  private ImportUtils importUtils;

  
  public ImportDataFile(String strKey) {
	importUtils = new ImportUtils();              
    objData = Indicators.getInstance(strKey);
  }
  	
  
  public void importFileToObjData() {
			 
    try { 

      File theFile = new File(fileName);  
      BufferedReader bufRdr = new BufferedReader(new FileReader(theFile));	
		
      //* Just get count of lines in file 
	  String strLine = "";
	  int maxRows=0;
	  for (int k=1; k<rowStart; k++) {
		strLine = bufRdr.readLine();  //* skip top line (header)
	  }  
	  while ((strLine = bufRdr.readLine()) !=null) {
		if (strLine.trim().length() == 0) {
			break;
		}
		if (strLine.indexOf("n/a") >= 0) {
			//* skip
		} else {
		   maxRows++;
		}
	  }
	  //* Now can set size of arrays
	  objData.data = new double[maxRows][4+numDataCols];
      objData.date = new Date[maxRows];
	  bufRdr.close();

	  //* Now populate arrays with dates from exclude files
	  DateFormat dfmDtMMddyy = new SimpleDateFormat("MM/dd/yy");
	  DateFormat dfmDtMMddyyyy = new SimpleDateFormat("MM/dd/yyyy");
	  String strTok;
	  int cntDelim=0;
	  int i = -1;  //!
	  int j;	

	  bufRdr = new BufferedReader(new FileReader(theFile));
	  for (int k=1; k<rowStart; k++) {
	    strLine = bufRdr.readLine();  //* skip top line (header)
	  }  
	  while ((strLine = bufRdr.readLine()) != null) {
	    StringTokenizer st = new StringTokenizer(strLine,"\t");
	    cntDelim = 0;
	    j = 0;
	    while (st.hasMoreTokens()) {  //* now go across
	      strTok = st.nextToken();	
	      strTok = strTok.trim();
	      if (cntDelim == 0) {
              importUtils.parseMtDyYr(strTok, strDateFormat);
		      importUtils.parseMtDyYr(strTok, strDateFormat);
		      i++;
		      objData.data[i][0] = importUtils.mt;
		      objData.data[i][1] = importUtils.dy;
		      objData.data[i][2] = importUtils.yr;
		      
		      if(strTok.length() > 6)
		        objData.date[i] = dfmDtMMddyyyy.parse(strTok);
		      else
		    	objData.date[i] = dfmDtMMddyy.parse(strTok);
		      //objData.cal[i] = new GregorianCalendar(importUtils.yr,importUtils.mt-1,importUtils.dy);
	          //objData.data[i][3] = objData.cal[i].get(Calendar.DAY_OF_WEEK)-1;
	          j = 3;
	      } else {	      	    	  
	    	  j++;
	    	  try {
		        objData.data[i][j] = Double.valueOf(strTok).doubleValue();
	          } catch(NumberFormatException nfe) {
		    	i--;  
		      }
	      }  	  
	      cntDelim++;
	    }  //* end horizontal while
	    
	  }   //* end vertical while, thus end of file
		    	    
	  bufRdr.close();
	  Gui.jtextArea.append("Finished importing " + fileName + "\n");
		    
	} catch (Exception e) {
		Gui.jtextArea.append("ERROR processing file " + fileName + "\n");
		Gui.jtextArea.append(e.toString() + "\n");
	}          
	      
  } //* end import fn
  
}
