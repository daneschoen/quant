package program;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import com.sun.xml.internal.ws.util.StringUtils;


public class UnitTest_getparams {
  
  
  public static void main (String[] args) {
	  ArrayList<String> res;
	  String str_cmd;
	  
	  try{
		Session session = new Session("es",
			                          "12/24/2000", "07/04/2015","0", "500", 
			                          "1015",
			                          "ENTRY: not hol(0)\n streak(c>c1) \n EXIT: \n exit(1615)",
			                          "SetNumObs(20) \n SetViewTimes(120, 6, 2, 10) \n SetViewStartTime(0000)" 
				                       );
	    str_cmd = "enter(0,1615)";	
	    System.out.println(str_cmd);
	    int[] dyfwd_timecol = session.getIntradyFixed(str_cmd);
	    System.out.println(dyfwd_timecol);
	  } catch(Exception e){
		System.out.println("?: " + e.getMessage());  
	  }	  
	  try{
		str_cmd = "exit(1, 0130)";  
		Session session = new Session("es",
                "12/24/2000", "07/04/2015","0", "500", 
                "1015",
                "ENTRY: not hol(0)\n streak(c>c1) \n EXIT: exit(1615)",
                "SetNumObs(20) \n SetViewTimes(120, 6, 2, 10) \n SetViewStartTime(0000)" 
                 );
        System.out.println(str_cmd);
        int[] dyfwd_timecol = session.getIntradyFixed(str_cmd);
        System.out.println(dyfwd_timecol);
	  } catch(Exception e){
		System.out.println("?: " + e.getMessage());  
	  }	  
	  try{
	    str_cmd = "enter(1615)";
		Session session = new Session("es",
                "12/24/2000", "07/04/2015","0", "500", 
                "1015",
                "ENTRY: not hol(0)\n streak(c>c1) \n EXIT: exit(1615)",
                "SetNumObs(20) \n SetViewTimes(120, 6, 2, 10) \n SetViewStartTime(0000)" 
                 );
        System.out.println(str_cmd);
        int[] dyfwd_timecol = session.getIntradyFixed(str_cmd);
        System.out.println(dyfwd_timecol);
	  } catch(Exception e){
		System.out.println("Works: " + e.getMessage());  
	  }	  
	  try{
	    str_cmd = "enter(0,1615,3)";	  
		Session session = new Session("es",
                "12/24/2000", "07/04/2015","0", "500", 
                "1015",
                "ENTRY: not hol(0)\n streak(c>c1) \n EXIT: exit(1615)",
                "SetNumObs(20) \n SetViewTimes(120, 6, 2, 10) \n SetViewStartTime(0000)" 
                 );
        System.out.println(str_cmd);
        int[] dyfwd_timecol = session.getIntradyFixed(str_cmd);
        System.out.println(dyfwd_timecol);
	  } catch(Exception e){
		System.out.println("Works: " + e.getMessage());  
	  }	  	  
	  System.out.println("");

	  try{
		str_cmd = "enter(1015)";  
		//* OK:  res = ParseUtils2.getParams("enter(1615)");  
		System.out.println(str_cmd);
	    res = ParseUtils2.getParams(str_cmd);
	    System.out.println(res.size() + " : " + res);
	  } catch(Exception e){
		System.out.println(e.getMessage());  
	  }
	  
	  try{
		str_cmd = "boo(foo(0,1615))";  
		//* OK:  res = ParseUtils2.getParams("enter(1615)");  
		System.out.println(str_cmd);
	    res = ParseUtils2.getParams(str_cmd);
	    System.out.println(res.size() + " : " + res);
	  } catch(Exception e){
		System.out.println(e.getMessage());  
	  }
	  try{
		str_cmd = "foo(cow(1615), second)";
		System.out.println(str_cmd);
		res = ParseUtils2.getParams(str_cmd);
		System.out.println(res.size() + " : " + res);
		System.out.println();    
	  } catch(Exception e){
		System.out.println(e.getMessage());  
	  }
	  try{
		str_cmd = "zow(0300";
		System.out.println(str_cmd);
		res = ParseUtils2.getParams(str_cmd);
		System.out.println(res.size() + " : " + res);
	  } catch(Exception e){
		System.out.println("Works: " + e.getMessage());  
	  }	  
	  try{
		str_cmd = "foo(cow( now(0,1615), c2),f2)";
		System.out.println(str_cmd);
		res = ParseUtils2.getParams(str_cmd);
		System.out.println(res.size() + " : " + res);
	  } catch(Exception e){
		System.out.println(e.getMessage());  
	  }
	  try{
		str_cmd = "foo(cownow(0,1615), c2),f2)";
		//str_cmd = "foo(cow( now(0,1615), c2,f2)";
		System.out.println(str_cmd);
		res = ParseUtils2.getParams(str_cmd);
		System.out.println(res.size() + " : " + res);
	  } catch(Exception e){
		System.out.println("Works: " + e.getMessage());  
	  }
	  
	  str_cmd = "1.75z";
	  double fod = Double.parseDouble(str_cmd.substring(0,str_cmd.indexOf("z")).trim());
	  System.out.println(fod);
	  
	  List<String []> arr_orig = new ArrayList<String[]>();  
	  arr_orig.add(new String[]{"not","well","maybe"});
	  arr_orig.add(new String[]{"def", "noway", "norway"});
	  for (String [] s:arr_orig)
	    System.out.println(s[0] +  s[1] +  s[2]);
	  List<String []> arr_cp = new ArrayList<String[]>(arr_orig);
	  for (String [] ss:arr_cp)
		System.out.println(ss[0] +  ss[1] +  ss[2]);
	  
	  double[] plUnrealCum_long = new double[3];
	  plUnrealCum_long[0] = 3.14;
	  plUnrealCum_long[1] = 21;
	  plUnrealCum_long[2] = -6.22;
	  System.out.println("DATA:" + Arrays.toString(plUnrealCum_long));
	  double[] goo = new double[3];
	  //goo = plUnrealCum_long;
	  //System.arraycopy( src, 0, dest, 0, src.length );
	  //System.arraycopy( plUnrealCum_long, 0, goo, 0, plUnrealCum_long.length );
	  goo = Arrays.copyOf(plUnrealCum_long, 5);
	  goo[2] = 911;
	  System.out.println(plUnrealCum_long[2]);
	  
	  double[][] series;
	  series = new double[2][3];
	  series[0][2] = 10.0;
	  //series[1] = plUnrealCum_long;
	  //System.arraycopy( plUnrealCum_long, 0, series[1], 0, plUnrealCum_long.length );
	  series[1] = Arrays.copyOf(plUnrealCum_long, plUnrealCum_long.length);
	  System.out.println(Arrays.deepToString(series));
	  String[][] ss = new String[2][3];
	  String mt = "09", dy="19", yr="2015";
	  ss[0][0] =  "'" + mt + "/" + dy + "/" + yr + "'"; //"'09/19/1999'";
	  ss[0][1] = "3.14";
	  ss[1][0] = "'07/04/2015'";
	  ss[1][1] = "6.22";
					  
	  System.out.println(Arrays.deepToString(ss));
	  
	  double[] g = new double[3];
	  double[] g2;
	  double[] g3;
	  g[0] = 3.14; g[1] = 6.22; g[2] = 8; 
      g2 = g;
      g[0] = -9.9;
      g3 = g;
	  for (int i=0; i<g.length; i++){
	    System.out.println(g2[i]);
	  }
	  for (int i=0; i<g.length; i++){
		    System.out.println(g3[i]);
	  }
	  
	  
	  
  }
  
}
