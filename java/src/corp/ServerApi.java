package program;

import java.util.Arrays;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;

import java.util.Iterator;
import java.util.List;
import java.util.Set;
import java.util.concurrent.Executors;
//java.util.concurrent.Executor
import java.util.concurrent.ExecutorService;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.Headers;
import com.sun.net.httpserver.HttpServer;


/* wget -q -O - "$@" _ 
 * http://localhost:8007/test
 * http://localhost:8007/api_get?hello=word&foo=bar
 * http://localhost:8007/api/import
 * http://localhost:8007/api/import?instr=es
 * http://localhost:8007/api/import?instr=es---da---cl
 * 
 * Using built in http server com.sun.net.httpserver
 * That FAQ concerns the sun.* package (such as sun.misc.BASE64Encoder) for internal usage by the Oracle JRE (which would thus kill your application when you run it on a different JRE), not the com.sun.* package. Sun/Oracle also just develop software on top of the Java SE API themselves like as every other company such as Apache and so on. Using com.sun.* classes is only discouraged (but not forbidden) when it concerns an implementation of a certain Java API, such as GlassFish (Java EE impl), Mojarra (JSF impl), Jersey (JAX-RS impl), etc.
 */


public class ServerApi {

    public final static int PORT = 8007;
    
    /* When adding endpoints:
     * ---------------------
     * - add HERE with public final static String ...
     * - add_endpoints() and add Handler_xyz()
     */
    public final static String API_TEST = "/test";
    
    public final static String API_INSTR_INFO = "/api/instr_info";
    public final static String API_KAKTEBYAZOVUT = "/api/kaktebyazovut";
    
    public final static String API_IMPORT = "/api/import";
    public final static String API_CALC = "/api/calc";
    //public final static String API_MODULE_HILO = "/api/module/hilo";
    //public final static String API_MODULE_RECPROF = "/api/module/recprof";
    public final static String API_MODULE_SURVIVAL = "/api/module/survival";
    public final static String API_MODULE_SYSTRADE = "/api/module/systrade";
    public final static String API_MODULE_EQUITYCURVE = "/api/module/equitycurve";
    public final static String API_MODULE_REGRESSION = "/api/module/regression";


    public static void main(String[] args) throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress(PORT), 0);

        ExecutorService  executor;
        executor = Executors.newFixedThreadPool(20);

        server.createContext(API_TEST, new Handler_test());
        server = add_endpoints(server);

        init_app();

        /*
        --------------------------------------------------------
        ServerImpl, the default executor is just "run" the task:

        private static class DefaultExecutor implements Executor {
             public void execute (Runnable task) {
                 task.run();
             }
        }
         
        you must provide a real executor for your httpServer:

        server.setExecutor(java.util.concurrent.Executors.newCachedThreadPool());  
        - Careful, this is a non-limited Executor
        - Creates a thread pool that creates new threads as needed, 
          but will reuse previously constructed threads when they are available.
        - doesn’t put tasks into a queue  
        vs
        Executors.newFixedThreadPool(20) 
        - creates exactly this many threads and reuses
        - when the pool is saturated, new tasks will get added to a queue without a limit on size. Good for CPU intensive tasks.
        - 
        --------------------------------------------------------
         */
         
         //server.setExecutor(null); 
         //server.setExecutor(Executors.newCachedThreadPool());
         server.setExecutor(executor);
         server.start();
        
        System.out.println("Started server: http://localhost:" + PORT + "/api/...");
    }


    public static HttpServer add_endpoints(HttpServer server){
    	server.createContext(API_INSTR_INFO, new Handler_instr_info());
    	server.createContext(API_KAKTEBYAZOVUT, new Handler_kaktebyazovut());
    	
        server.createContext(API_IMPORT, new Handler_import());
        server.createContext(API_CALC, new Handler_calc());
        //server.createContext(API_MODULE_HILO, new Handler_hilo());
        //server.createContext(API_MODULE_RECPROF, new Handler_recprof());
        server.createContext(API_MODULE_SURVIVAL, new Handler_survival());
        server.createContext(API_MODULE_SYSTRADE, new Handler_systrade());
        server.createContext(API_MODULE_EQUITYCURVE, new Handler_equitycurve());
        server.createContext(API_MODULE_REGRESSION, new Handler_regression());
        
        return server;
    }
    
    
    public static void init_app(){
	    InstrSpecs.initialize();
	    EconSetup.initialize();
    }
    
    
    /* ============================================================================
     * Helper functions for httpserver
     * ============================================================================
     */
    /**
     * returns the url parameters in a map
     * @param query
     * @return map
     */
    public static Map<String, String> queryToMap(String query){
      Map<String, String> mapResult = new HashMap<String, String>();
      for (String param : query.split("&")) {
          String pair[] = param.split("=");
          if (pair.length>1) {
              mapResult.put(pair[0], pair[1]);
          }else{
              mapResult.put(pair[0], "");
          }
      }
      return mapResult;
    }
    
    static void send_response(HttpExchange h, int response_code, String response) throws IOException{
        h.sendResponseHeaders(response_code, response.length());  //* response.getBytes().length
        OutputStream os = h.getResponseBody();
        os.write(response.getBytes());
        os.close();
    }
    
   /* ============================================================================
    * HttpHandler's for endpoints
    * ============================================================================
    */
    
    class MyHandler implements HttpHandler {
    	  public void handle(HttpExchange exchange) throws IOException {
    	    String requestMethod = exchange.getRequestMethod();
    	    if (requestMethod.equalsIgnoreCase("GET")) {
    	      Headers responseHeaders = exchange.getResponseHeaders();
    	      responseHeaders.set("Content-Type", "text/plain");
    	      exchange.sendResponseHeaders(200, 0);

    	      OutputStream responseBody = exchange.getResponseBody();
    	      Headers requestHeaders = exchange.getRequestHeaders();
    	      Set<String> keySet = requestHeaders.keySet();
    	      Iterator<String> iter = keySet.iterator();
    	      while (iter.hasNext()) {
    	        String key = iter.next();
    	        List values = requestHeaders.get(key);
    	        String s = key + " = " + values.toString() + "\n";
    	        responseBody.write(s.getBytes());
    	      }
    	      responseBody.close();
    	    }
    	  }
    }
    
    static class Handler_test implements HttpHandler {
        @Override
        public void handle(HttpExchange h) throws IOException {
            String response = "ok - sanity check: Java server is working\n";
            System.out.println("begin");
            // SimpleHttpServer2.sendResponse(h, 200, response.toString());

            send_response(h, 200, response);
            /*
            h.sendResponseHeaders(200, response.length());  //* response.getBytes().length
            OutputStream os = h.getResponseBody();
            os.write(response.getBytes());
            os.close();
            */
        }
    }
    
    //* http://localhost:8007/api/instr_info?instr=da
    static class Handler_instr_info implements HttpHandler {
        @Override
        public void handle(HttpExchange h) throws IOException {
            String response = "ERROR - BEGIN SERVICE API";
            int response_code = 500;
            
            String getparams = h.getRequestURI().getQuery();
            if (getparams == null){
            	response = "ERROR - Invalid params: missing/incorrect instrument symbol";
            	response_code = 400;
            	send_response(h, response_code, response);
            	return;
            }	
            
            Map <String,String>mpParams = queryToMap(getparams);
            String strInstrDep = mpParams.get("instr");      
            
            try{
              Instr InstrX = Instr.getInstance(Arrays.asList(InstrSpecs.idNames).indexOf(strInstrDep.toUpperCase()));
              response = InstrX.idName + " " + InstrX.key + "\n";
              response += InstrX.blImported  + "\n";
              if (!InstrX.blImported){
            	  send_response(h, 200, response);        
              }
              for (int d=0; d<3; d++){
                  //for(int j=0; j<1440; j++)
                  for (int j=0; j<10; j++){	
            	      response +=  InstrX.prcDate[d] + "   " + InstrX.prcTime[j] + " : " + InstrX.prc[d][j] + "\n" ;
                  } 	
                  for (int j=1440-10; j<1440; j++){	
            	      response +=  InstrX.prcDate[d] + "   " + InstrX.prcTime[j] + " : " + InstrX.prc[d][j] + "\n" ;
                  } 	
              }
              
              for (int d=InstrX.prc.length-3; d<InstrX.prc.length; d++){
                  for (int j=0; j<10; j++){	
                  	response +=  InstrX.prcDate[d] + "   " + InstrX.prcTime[j] + " : " + InstrX.prc[d][j] + "\n" ;
                    } 	
                  for (int j=1440-10; j<1440; j++){	
                	  response +=  InstrX.prcDate[d] + "   " + InstrX.prcTime[j] + " : " + InstrX.prc[d][j] + "\n" ;
                  } 	
              }
	        } catch(Exception e) {	  
			  response = "ERROR - instr_info: " + e.getMessage();
			  response_code = 400;
	        }  
            
            response_code = 200;
            send_response(h, response_code, response);                    	            
        }
    }

    //* http://localhost:8007/api/kaktebyazovut
    static class Handler_kaktebyazovut implements HttpHandler {
        @Override
        public void handle(HttpExchange h) throws IOException {
            String response_str = "ERROR - BEGIN SERVICE API";
            int response_code = 500;
                        
            try{
              response_str = "Build: " + AGlobal.strVER;
              //response_str += "\nUSER: " + new Session().USERTYPE; 		  
	        } catch(Exception e) {	  
			  response_str = "ERROR - user_info: " + e.getMessage();
			  response_code = 400;
	        }  
            
            response_code = 200;
            send_response(h, response_code, response_str);                    	            
        }
    }
    
        
    //* http://localhost:8007/api/import?instr=es---us
    static class Handler_import implements HttpHandler {
        @Override
        public void handle(HttpExchange h) throws IOException {
            
            String response;
            String ret_status;
            String[] arrInstrs = null;   //* represents ALL, len==0 represents nothing checked
            String getparams = h.getRequestURI().getQuery();
            if (getparams != null){
              Map <String,String>mpParams = queryToMap(getparams);
              /*
              StringBuilder sbResponse = new StringBuilder(); 
              sbResponse.append("<html><body>");
              sbResponse.append("hello : " + parms.get("hello") + "<br/>");
              sbResponse.append("foo : " + parms.get("foo") + "<br/>");
              sbResponse.append("</body></html>");
              response = sbResponse.toString();
              */
              String strInstrs = mpParams.get("instr");
        	  arrInstrs = strInstrs.split(AGlobal.INSTRS_SEP);
        	  
        	  /* test
        	  strInstrs = "";
        	  for (String instr: arrInstrs){
        	    System.out.println(instr);
        	    strInstrs += "/" + instr;
        	  }
              response = strInstrs;
              */
        	  
            }

            /* put in python
        	SimpleDateFormat sdf = new SimpleDateFormat("MM/dd/yyyy HH:mm:ss");
        	String strText = sdf.format(new Date());
        	jtextArea.setText("Importing at " + strText + "\n\n");
        	*/  
            
            //* Must import econ bef dep bec prices need to be scrubbed of hol's
            ret_status = importEcon();      
            if (ret_status == "ok"){
                ret_status = importDependent(arrInstrs);
            }
            
            response = ret_status;
            h.sendResponseHeaders(200, response.length());
            OutputStream os = h.getResponseBody();
            os.write(response.getBytes());
            os.close();
                    	
        }
    }
    
    public static String importEcon() {
	    //jtextArea.append("Importing economic data...\n");
    	Econ EconX=null;
		try {  
	      for (int k=0; k<EconSetup.TOT_ECON; k++) {
	          EconX = Econ.getInstance(EconSetup.name[k]);
	  	      ImportEcon.importFile(EconX.name);
	  	      EconX.blImported = true;
	      } 
		} catch (Exception e) {
		  //e.printStackTrace();
		  return "ERROR - Importing econ file: " + EconX.name;
		}  
		
	    return "ok";
    }
    
    public static String importDependent(String[] arrInstrs) {
    	      	  
      	ImportDataConvert importDataConvert = new ImportDataConvert();
      	
      	if (arrInstrs==null) {
      	    for (int r=0; r<InstrSpecs.TOT_INSTRS; r++) {
      	    	Instr InstrX = Instr.getInstance(r);  
      	        try {
      	    	  //* jtextArea.append("Importing instrument: " + InstrSpecs.idNames[r] + "\n");
      	          
      	    	  importDataConvert.go(r);
      	    	  /*
      	    	  importDataConvert.importFile(r); 	
      	    	  importDataConvert.scrubPrices(r); 	    	
      	    	  importDataConvert.outputNewRawFile(r);
      	    	  */
                  InstrX.blImported = true;
      	        } catch (Exception e) {
      	          InstrX.blImported = false;
      	          return "ERROR - Importing instrument: " + InstrSpecs.idNames[r];
      		    }
      	    }  
            //* refreshDrpTstDates();
            //* refreshDrpTimeStamps();
            return "ok";     	
            
      	} else {
      		for (String instr:arrInstrs) {  
      		    int instr_index = java.util.Arrays.asList(InstrSpecs.idNames).indexOf(instr.toUpperCase());
      		    Instr InstrX = Instr.getInstance(instr_index);
	      	    try {	 	  
	      	      importDataConvert.go(instr_index);              
	              InstrX.blImported = true;
	              //* refreshDrpTstDates();
	              //* refreshDrpTimeStamps();	            
	    	    } catch (Exception e) {
	    	      InstrX.blImported = false;  
	    	      return "ERROR - Importing instrument: " + instr;
	    	    }   
      		}
      		return "ok";
        }  
    }
    
    
    static class Handler_calc implements HttpHandler {
        @Override
        public void handle(HttpExchange h) throws IOException {
            String response = "ERROR - Handler calc";
            int response_code = 500;
            
            String getparams = h.getRequestURI().getQuery();
            if (getparams == null){
            	response = "ERROR - Handler calc: Invalid params";
            	response_code = 400;
            	send_response(h, response_code, response);
            	return;
            }	
            
            Map <String,String>mpParams = queryToMap(getparams);
            String strInstrDep = mpParams.get("InstrDep");
            String strDtBeg = mpParams.get("dt_beg");
            String strDtEnd = mpParams.get("dt_end");
            String strDtBegIndx = mpParams.get("dt_beg_indx");
            String strDtEndIndx = mpParams.get("dt_end_indx");            
            String strTimeEnter = mpParams.get("timeEnter");
            String strCondition = mpParams.get("condition");
            String strViewOption = mpParams.get("viewoption");
            String str_postscenario = mpParams.get("postscenario");
            String str_bl_postscenario_hilo = mpParams.get("bl_postscenario_hilo");
            String str_bl_postfilter_recprof = mpParams.get("bl_postfilter_recprof");
            String username = mpParams.get("username");
            
            //* Validation
            if (strCondition == null || strCondition == ""){   
                send_response(h, 400, "ERROR - Missing conditions");
        	    return;
            }
            if (strViewOption == null || strViewOption == ""){   
                send_response(h, 400, "ERROR - Missing view options");
          	    return;
            }
            
            //* Following only works bec each pattern are mutually exclusive:
            strCondition = strCondition.replace("___"," ").replace("__eq","=");
            strViewOption = strViewOption.replace("___"," ").replace("__eq","=");
            str_postscenario = str_postscenario.replace("___"," ").replace("__eq","=");
            
            /* wrong sol:
            "abc" and replacements = {{"a"}{"b"},{"b"}{"c"}} you should expect "bcc" on output but you will get "ccc"
            String[][] replacements = {{"call me", "cm"}, 
                    {"as soon as possible", "asap"}};

				//loop over the array and replace
				String strOutput = inString;
				for(String[] replacement: replacements) {
				strOutput = strOutput.replace(replacement[0], replacement[1]);
				}
            */
            /*
            Map<String,String> tokens = new HashMap<String,String>();
            tokens.put("cat", "Garfield");
            tokens.put("beverage", "coffee");

            String template = "%cat% really needs some %beverage%.";

            // Create pattern of the format "%(cat|beverage)%"
            String patternString = "%(" + StringUtils.join(tokens.keySet(), "|") + ")%";
            Pattern pattern = Pattern.compile(patternString);
            Matcher matcher = pattern.matcher(template);

            StringBuffer sb = new StringBuffer();
            while(matcher.find()) {
                matcher.appendReplacement(sb, tokens.get(matcher.group(1)));
            }
            matcher.appendTail(sb);

            System.out.println(sb.toString());
            */
            
            /* DEBUG:
            response = strDepInstr + ">>>" + strCondition + ">>>" + strDtBeg + ">>>" + strDtEnd + ">>>" + strDtBegIndx + ">>>" + strDtEndIndx  + ">>>" + strTimeEnter + ">>>" + strViewOptions;
            response_code = 200;
            */
               
    		try {   
    	      Processor processor = new Processor(
    	        strInstrDep, 
    	        strDtBeg, strDtEnd, strDtBegIndx, strDtEndIndx, 
    	        strTimeEnter, 
    	        strCondition,
    	        strViewOption,
    	        str_postscenario,
    	        str_bl_postscenario_hilo,
    	        str_bl_postfilter_recprof,
    	        username
    	      ); 	      
    	      
              processor.run_all();     
              response = processor.strView_statistics;
              
              if (response.startsWith("ERROR")){
            	 response_code = 400;
              } else if (response.startsWith("ERROR")){
                 response_code = 500;
              } else {   
                 response_code = 200;
              }   
              
	        } catch(Exception e) {	  
			  response = "ERROR - Processor.go: Running of Strategy failed: " + e.getMessage();
			  response_code = 400;
	        }  
            
    		send_response(h, response_code, response);    		
        }
    }
    
    /*
    static class Handler_hilo implements HttpHandler {
        @Override
        public void handle(HttpExchange h) throws IOException {
            String response = "Placeholder for hilo";
            h.sendResponseHeaders(200, response.length());
            OutputStream os = h.getResponseBody();
            os.write(response.getBytes());
            os.close();
        }
    }
    
    static class Handler_recprof implements HttpHandler {
        @Override
        public void handle(HttpExchange h) throws IOException {
            String response = "Placeholder for recprof";
            h.sendResponseHeaders(200, response.length());
            OutputStream os = h.getResponseBody();
            os.write(response.getBytes());
            os.close();
        }
    }
    */
    
    static class Handler_survival implements HttpHandler {
        @Override
        public void handle(HttpExchange h) throws IOException {
            String response = "ERROR - internal error";
            int response_code = 500;
            
            String getparams = h.getRequestURI().getQuery();
            if (getparams == null){
            	response = "ERROR - Invalid params";
            	response_code = 400;
            	send_response(h, response_code, response);
            	return;
            }	
            
            Map <String,String>mpParams = queryToMap(getparams);
            String str_feature = mpParams.get("feature");
            //String str_viewoption = mpParams.get("viewoption");
            String str_InstrDep = mpParams.get("instr_dep");
            String str_dt_beg = mpParams.get("dt_beg");
            String str_dt_end = mpParams.get("dt_end");
            String str_dt_beg_indx = mpParams.get("dt_beg_indx");
            String str_dt_end_indx = mpParams.get("dt_end_indx");            
            String str_entry_time = mpParams.get("entry_time");
            
            String str_mod_timetarget_day = mpParams.get("mod_timetarget_day");
            String str_mod_timetarget_time = mpParams.get("mod_timetarget_time");
            String str_mod_wait_time = mpParams.get("mod_wait_time");
            
            String username = mpParams.get("username");
            
            //* Validation
            if (str_feature == null || str_feature == ""){   
                send_response(h, 400, "ERROR - Missing conditions");
        	    return;
            }
            /*
            if (str_viewoption == null || str_viewoption == ""){   
                send_response(h, 400, "ERROR - Missing view options");
          	    return;
            }
            */
            str_feature = str_feature.replace("___"," ").replace("__eq","=");
            //strViewOptions = strViewOptions.replace("___"," ").replace("__eq","=");
            
    	    try {   
    	      //* D
    	      //response = str_mod_timetarget_day + " => " + str_mod_timetarget_time + " => " + str_mod_wait_time;	
    	      
    	      Session session = new Session(
    	        str_InstrDep,
    	      	str_dt_beg, str_dt_end, str_dt_beg_indx, str_dt_end_indx,
    	      	str_entry_time, 
    	      	str_feature,
    	      	username
    	      );
    	      
    	      Mod_Survival survival = new Mod_Survival(session);
    	      
    	      survival.CmdiExitDysFwd = Integer.parseInt(str_mod_timetarget_day);
  	          survival.CmdiExitCol = session.InstrDep.getTimeCol(str_mod_timetarget_time);
  	          survival.CmdstrExitTime = session.InstrDep.prcTime[survival.CmdiExitCol];   
  	          survival.CmdiWait0ExitCol = session.InstrDep.getTimeCol(str_mod_wait_time);
  	          survival.CmdstrWait0ExitTime = session.InstrDep.prcTime[survival.CmdiWait0ExitCol];    
  	          
  	          survival.runAndConstructView();  	           
              response = survival.strView;
                
	          if (response.startsWith("ERROR")){
	            response_code = 400;
	          } else if (response.startsWith("ERROR")){
	             response_code = 500;
	          } else {   
	             response_code = 200;
	          }   
                
  	        } catch(Exception e) {	  
  			  response = "ERROR - API - Mod_Survival: " + e.getMessage();
  			  response_code = 400;
  	        }  
              
      		send_response(h, response_code, response);   
        }
    }
    
    static class Handler_systrade implements HttpHandler {
        @Override
        public void handle(HttpExchange h) throws IOException {
            String response = "ERROR - internal error";
            int response_code = 500;
            
            String getparams = h.getRequestURI().getQuery();
            if (getparams == null){
            	response = "ERROR - Invalid params";
            	response_code = 400;
            	send_response(h, response_code, response);
            	return;
            }
            
            Map <String,String>mpParams = queryToMap(getparams);
            String str_InstrDep = mpParams.get("instr_dep");
            String str_dt_beg = mpParams.get("dt_beg");
            String str_dt_end = mpParams.get("dt_end");
            String str_dt_beg_indx = mpParams.get("dt_beg_indx");
            String str_dt_end_indx = mpParams.get("dt_end_indx");            
            String str_entry_time = mpParams.get("entry_time");
            String str_feature = mpParams.get("feature");
            //String str_viewoption = mpParams.get("viewoption");
            String str_mod_maxopencontract = mpParams.get("mod_maxopencontract");
            String str_mod_bl_exit_feature = mpParams.get("mod_bl_exit_feature");
            //String str_mod_exit_feature_fixed_dyfwd_time = mpParams.get("mod_exit_feature_fixed_dyfwd_time");
            String str_mod_bl_profittarget = mpParams.get("mod_bl_profittarget");
            String str_mod_profittarget = mpParams.get("mod_profittarget");
            String str_mod_bl_stoploss = mpParams.get("mod_bl_stoploss");
            String str_mod_stoploss = mpParams.get("mod_stoploss");
            //// remove this! ?
            String str_mod_bl_timetarget = mpParams.get("mod_bl_timetarget");
            String str_mod_timetarget_day = mpParams.get("mod_timetarget_day");
            String str_mod_timetarget_time = mpParams.get("mod_timetarget_time");
            
            String str_postscenario = mpParams.get("postscenario");
            String str_bl_postfilter_recprof = mpParams.get("bl_postfilter_recprof");
            String username = mpParams.get("username");

            //* Validation
            if (str_feature == null || str_feature == ""){   
                send_response(h, 400, "ERROR - Missing conditions");
        	    return;
            }
            
            str_feature = str_feature.replace("___"," ").replace("__eq","=");
            str_postscenario = str_postscenario.replace("___"," ").replace("__eq","=");
            
    	    try {
    	      
    	      /* D
    	      response = str_mod_maxopencontract + " => " + str_mod_bl_exit_feature + " => " 
    	      + str_mod_bl_profittarget + " => " + str_mod_profittarget + " => " 
    	      + str_mod_bl_stoploss  + " => " + str_mod_stoploss  + " => " 
    	      + str_mod_bl_timetarget + " => " + str_mod_timetarget_day + " => " + str_mod_timetarget_time;
    	      */
    	      
      	      Session session = new Session(
      	        str_InstrDep,
      	      	str_dt_beg, str_dt_end, str_dt_beg_indx, str_dt_end_indx,
      	      	str_entry_time, 
      	      	str_feature,
      	      	username
      	      );
      	      
      	      session.bl_postfilter_recprof = false;
      		  if (str_bl_postfilter_recprof.equals("true")){
      		      session.bl_postfilter_recprof = true;
      		      session.str_postscenario = str_postscenario;
      		  }  
      	      
      	      
      	      Mod_SysTrade mod_systrade = new Mod_SysTrade(session);
      	      mod_systrade.init();
      	      
      	      mod_systrade.cmd_maxopencontract = Integer.parseInt(str_mod_maxopencontract); 
      	      mod_systrade.cmd_bl_exit_feature_fixed=false;
      	      mod_systrade.cmd_bl_exit_feature_event=false;
        	  if (str_mod_bl_exit_feature.equals("true")){
        		  if (session.bl_exit_event){
        			  
        		  }
        		  if (session.bl_exit_fixed){
        		    mod_systrade.cmd_bl_exit_feature_fixed = true;
        		    mod_systrade.cmd_exit_feature_fixed_dyfwd = session.exitfixed_dyfwd;
        		    mod_systrade.cmd_exit_feature_fixed_timecol = session.exitfixed_timecol;
        		    mod_systrade.cmd_exit_feature_fixed_timestr = session.InstrDep.prcTime[mod_systrade.cmd_exit_feature_fixed_timecol]; 
        	  
        		  }     	          
        	  }
        	  
        	  mod_systrade.cmd_bl_exit_profittarget_p=false;
      	      mod_systrade.cmd_bl_exit_profittarget_z=false;
        	  if (str_mod_bl_profittarget.equals("true")){
        		  if (str_mod_profittarget.substring(str_mod_profittarget.length() - 1).equals("z")){
        		    mod_systrade.cmd_bl_exit_profittarget_z = true;
        		    mod_systrade.cmd_fd_exit_profittarget_z = Double.parseDouble(str_mod_profittarget.substring(0, str_mod_profittarget.indexOf("z")).trim());
        		  } else {
        			mod_systrade.cmd_bl_exit_profittarget_p = true;  
        			mod_systrade.cmd_fd_exit_profittarget_p = Double.parseDouble(str_mod_profittarget.trim());
        		  }		
        	  }   
        	  
        	  mod_systrade.cmd_bl_exit_stoploss_p=false;
      	      mod_systrade.cmd_bl_exit_stoploss_z=false;
        	  if (str_mod_bl_stoploss.equals("true")){
        		  if (str_mod_stoploss.substring(str_mod_stoploss.length() - 1).equals("z")){
        		    mod_systrade.cmd_bl_exit_stoploss_z = true;
        		    mod_systrade.cmd_fd_exit_stoploss_z = Double.parseDouble(str_mod_stoploss.substring(0, str_mod_stoploss.indexOf("z")).trim());
        		  } else {
        			mod_systrade.cmd_bl_exit_stoploss_p = true;  
        			mod_systrade.cmd_fd_exit_stoploss_p = Double.parseDouble(str_mod_stoploss.trim());
        		  }		
        	  }   
        	  
        	  if (str_mod_bl_timetarget.equals("true")){
        		  mod_systrade.cmd_bl_exit_timetarget_rel=true;
        		  mod_systrade.cmd_exit_timetarget_dyfwd = Integer.parseInt(str_mod_timetarget_day);
        		  mod_systrade.cmd_exit_timetarget_timecol = session.InstrDep.getTimeCol(str_mod_timetarget_time);
        		  mod_systrade.cmd_str_exit_timetarget = session.InstrDep.prcTime[mod_systrade.cmd_exit_timetarget_timecol]; 
        	  }   
        	  
      	      mod_systrade.run_constructView();  	           
              response = mod_systrade.strView;
      	                      
	          if (response.startsWith("ERROR")){
	            response_code = 400;
	          } else if (response.startsWith("ERROR")){
	             response_code = 500;
	          } else {   
	             response_code = 200;
	          }   
                
  	        } catch(Exception e) {	  
  			  response = "ERROR - Mod_SysTrade: " + e.getMessage();
  			  response_code = 400;
  	        }  
              
      		send_response(h, response_code, response);   

        }
    }
    
    
    static class Handler_equitycurve implements HttpHandler {
        @Override
        public void handle(HttpExchange h) throws IOException {
            String response = "ERROR - internal error";
            int response_code = 500;
            
            String getparams = h.getRequestURI().getQuery();
            if (getparams == null){
            	response = "ERROR - Invalid params";
            	response_code = 400;
            	send_response(h, response_code, response);
            	return;
            }	
            
            Map <String,String>mpParams = queryToMap(getparams);
            String str_InstrDep = mpParams.get("instr_dep");
            String str_dt_beg = mpParams.get("dt_beg");
            String str_dt_end = mpParams.get("dt_end");
            String str_dt_beg_indx = mpParams.get("dt_beg_indx");
            String str_dt_end_indx = mpParams.get("dt_end_indx");            
            String str_entry_time = mpParams.get("entry_time");
            String str_feature = mpParams.get("feature");
            //String str_viewoption = mpParams.get("viewoption");
            String str_mod_timetarget_day = mpParams.get("mod_timetarget_day");
            String str_mod_timetarget_time = mpParams.get("mod_timetarget_time");

            String str_postscenario = mpParams.get("postscenario");
            String str_bl_postfilter_recprof = mpParams.get("bl_postfilter_recprof");
            String username = mpParams.get("username");
            
            //* Validation
            if (str_feature == null || str_feature == ""){   
                send_response(h, 400, "ERROR - Missing conditions");
        	    return;
            }
            
            str_feature = str_feature.replace("___"," ").replace("__eq","=");
            str_postscenario = str_postscenario.replace("___"," ").replace("__eq","=");
                    
    	    try {   
      	      
    	      Session session = new Session(
    	        str_InstrDep,
    	      	str_dt_beg, str_dt_end, str_dt_beg_indx, str_dt_end_indx,
    	      	str_entry_time, 
    	      	str_feature,
    	      	username
    	      );
    	      
      	      session.bl_postfilter_recprof = false;
      		  if (str_bl_postfilter_recprof.equals("true")){
      		      session.bl_postfilter_recprof = true;
      		      session.str_postscenario = str_postscenario;
      		  }  
              
    	      
      	      Mod_EquityCurve mod_equitycurve = new Mod_EquityCurve(session);
    		  mod_equitycurve.cmd_exit_timetarget_dyfwd = Integer.parseInt(str_mod_timetarget_day);
    		  mod_equitycurve.cmd_exit_timetarget_timecol = session.InstrDep.getTimeCol(str_mod_timetarget_time);
    		  mod_equitycurve.cmd_str_exit_timetarget = session.InstrDep.prcTime[mod_equitycurve.cmd_exit_timetarget_timecol]; 
    	      
      	      mod_equitycurve.set_run_view();  	           
              response = mod_equitycurve.strView;

	          if (response.startsWith("ERROR")){
	            response_code = 400;
	          } else if (response.startsWith("ERROR")){
	             response_code = 500;
	          } else {   
	             response_code = 200;
	          }   
                
  	        } catch(Exception e) {	  
  			  response = "ERROR - Mod_EquityCurve: " + e.getMessage();
  			  response_code = 400;
  	        }  
              
      		send_response(h, response_code, response);   	      
      		
        }
    }
    
    
    static class Handler_regression implements HttpHandler {
        @Override
        public void handle(HttpExchange h) throws IOException {
            String response = "ERROR - internal error";
            int response_code = 500;
            
            String getparams = h.getRequestURI().getQuery();
            if (getparams == null){
            	response = "ERROR - Invalid params";
            	response_code = 400;
            	send_response(h, response_code, response);
            	return;
            }	
            
            Map <String,String>mpParams = queryToMap(getparams);
            
            String str_Instr_dep = mpParams.get("instr_dep");
            String str_dt_beg = mpParams.get("dt_beg");
            String str_dt_end = mpParams.get("dt_end");
            String str_dt_beg_indx = mpParams.get("dt_beg_indx");
            String str_dt_end_indx = mpParams.get("dt_end_indx");            
            String str_entry_time = mpParams.get("entry_time");
            //String str_feature = java.net.URLDecoder.decode(mpParams.get("feature"), "UTF-8");
            //String str_viewoption = java.net.URLDecoder.decode(mpParams.get("viewoption"), "UTF-8");
            String str_mod_y = java.net.URLDecoder.decode(mpParams.get("mod_y"), "UTF-8");
            String str_mod_x1 = java.net.URLDecoder.decode(mpParams.get("mod_x1"), "UTF-8");
            String str_mod_x2 = java.net.URLDecoder.decode(mpParams.get("mod_x2"), "UTF-8");
            String str_mod_x3 = java.net.URLDecoder.decode(mpParams.get("mod_x3"), "UTF-8");
            String str_mod_x4 = java.net.URLDecoder.decode(mpParams.get("mod_x4"), "UTF-8");
            String str_mod_x5 = java.net.URLDecoder.decode(mpParams.get("mod_x5"), "UTF-8");
            String str_mod_x6 = java.net.URLDecoder.decode(mpParams.get("mod_x6"), "UTF-8");
            
            String username = mpParams.get("username");
            
    	    try {   
      	      /* D
    	      response =  str_mod_y + " => " + str_mod_x1 + " => " + str_mod_x2 + " => " + str_mod_x3 + " => " + str_mod_x4 + " => " + str_mod_x5 + " => " + str_mod_x6;	
    	      */
    	      
      	      Session session = new Session(
      	        str_Instr_dep,
      	      	str_dt_beg, str_dt_end, str_dt_beg_indx, str_dt_end_indx,
      	      	username
      	      );
      	      
        	  Mod_Regression mod_regression = new Mod_Regression(session);
      		  mod_regression.cmdY = str_mod_y;
      		  mod_regression.cmdX1 = str_mod_x1;
      		  mod_regression.cmdX2 = str_mod_x2;
      		  mod_regression.cmdX3 = str_mod_x3;
      		  mod_regression.cmdX4 = str_mod_x4;
      		  mod_regression.cmdX5 = str_mod_x5;
      		  mod_regression.cmdX6 = str_mod_x6;
      		  
      		  mod_regression.set_run_view();  	           
              response = mod_regression.strView;

  	          if (response.startsWith("ERROR")){
  	            response_code = 400;
  	          } else if (response.startsWith("ERROR")){
  	             response_code = 500;
  	          } else {   
  	             response_code = 200;
  	          }   
                  
	        } catch(Exception e) {	  
			  response = "ERROR - Mod_Regression: " + e.getMessage();
    		  response_code = 400;
    	    }  
                
        	send_response(h, response_code, response);   	      
 
        }
    }    
}
