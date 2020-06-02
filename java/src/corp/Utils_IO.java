package program;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;


public class Utils_IO {

	
  public static String arrstr_to_string(String[] lst_str){
	String strlst="[]";  
    if (lst_str.length > 0){
	    strlst="['" + lst_str[0] + "'";
	    for (int x=1;x<lst_str.length; x++){
	    	strlst += ",'" + lst_str[x] + "'";
	    }
	    strlst += "]";
	}
	return strlst;
  }
  
  public static double[] getSeriesDep(Session session){
    double[] series = new double[session.endDateIndex - session.begTstDateIndex +1];
      
    
    return series;
  }
  
  
  public static void outputData(Session session, String data_csv) { 	
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
	String outPathFileName = AGlobal.DATA_DIR + "obs_" + session.username + ".csv";
	
	try {
	  /*		
	  FileWriter fstream = new FileWriter("output.txt");
	  BufferedWriter out = new BufferedWriter(new FileWriter(File_Results));
	  out.write("blah");
	  */
      BufferedWriter out = new BufferedWriter(new FileWriter(outPathFileName));
	  
	  out.write(data_csv);  
		   
	  out.close();
	} catch (IOException e) {
	  ///Gui.jtextArea.append(e.toString() + "\n\n");
	}
			  
  }
  
}
