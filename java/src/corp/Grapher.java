package program;

import java.util.Arrays;

public class Grapher {

  public String[][][] series_str;
  public String[][] series_yx_str;
  public double[][] series_fd;
  public String[] series_dtstr;
  public String[] series_name;
  public String chart_title;
  private Session session;
  private Instr InstrDep; 	
	
  public Grapher(Session session) {
	this.session = session;  
	InstrDep = session.InstrDep;
  }
      
  public void construct_dataset_systrade() {
    /*********************************************************************
     * java => python => js expects:
     * [N][2]  ==>
     * "[['07/04/2015', 3.14], ['07/05/2015', 6.22], ..., N]"  ==>
     * "[[epoch, 3.14], [epoch, 6.22], ..., N]" ==> $.parseJSON(data);
     * 
     * M series:
     * 0) JS
     * 1) Java Mod_SysTrade: [M][N][2]  ==>
     * 2) Java Grapher: -> "[[['07/04/2015', 3.14], ['07/05/2015', 6.22], ..., N],
     *                       [['07/04/2015', 3.14], ['07/05/2015', 6.22], ..., N],
     *                       ..., M
     *                      ]" 
     * 3) Java Mod_SysTrade: split long/short: "CHART_DATA_LONG: [['07/04/2015', 3.14], ['07/05/2015', 6.22], ..., N]"
     *                                         "CHART_DATA_SHORT: ....   
     *                       return systrade_statistics + chart_data_long + chart_data_short 
     * 4) Python: split sections 
     *            chart_data_long/short -> epoch -> str
     *            return json 
     * 5) JS: function getJsonAjax_module_systrade(param){ ... done -> 
     *        openInNewTab("/analytics/module/systrade/chart_equitycurve/long/" + data.chart_data_long/short);
     * 6) Python: @app.route('/analytics/module/systrade/chart_equitycurve/<side>/<chart_data>')
     * 7) JS: chart_equitycurve.html: chart_data_long/short -> $.parseJSON(data_str);
     ***********************************************************************/
	  
	//* series_fd MUST HAVE BEEN SET FIRST  
	series_str = new String[series_fd.length][series_fd[0].length][2]; 
	
	for (int s=0; s<series_fd.length; s++) {   //* for ex 2 for long and short, M for multivariate regression
	  for (int i_s=0; i_s<series_fd[s].length; i_s++) {
        //* int dy = Integer.parseInt(InstrDep.getDay(i+session.begTstDateIndex));
		String dy = InstrDep.getDay(i_s + session.begTstDateIndex);
		String mt = InstrDep.getMonth(i_s + session.begTstDateIndex);
		String yr = InstrDep.getYear(i_s + session.begTstDateIndex);
		series_str[s][i_s][0] = "'" + mt + "/" + dy + "/" + yr + "'";
		series_str[s][i_s][1] = String.valueOf(series_fd[s][i_s]);
	  }	
    }
	
	//return Arrays.deepToString(series_str);  
  }
  
  
  public void construct_dataset_regression() {
	/*********************************************************************
     * series_yx_str -> [[3.14, 6.22, ..., N],
     *                   [3.14, 6.22, ..., N],
     *                   ..., 1 Y + M X features
     *                  ]  
     * series_dtstr  -> ['07/14/2010', '12/25/2015', ...,N],  
	 *********************************************************************/
    //* series_fd MUST HAVE BEEN SET FIRST  [num_features][end-maxdysbk+1][1] - no dts, thats in series_dtstr
	series_yx_str = new String[series_fd.length][series_fd[0].length];
	series_dtstr = new String[series_fd[0].length];
	 
	for (int s=0; s<series_fd.length; s++) {   //* Y, X features
	    for (int i_s=0; i_s<series_fd[s].length; i_s++) {
			series_yx_str[s][i_s] = String.valueOf(series_fd[s][i_s]);			
	    }	
	}

    for (int i=0; i<series_fd[0].length; i++) {
        String dy = InstrDep.getDay(i + session.InstrDep.maxDysBk);   //***
		String mt = InstrDep.getMonth(i + session.InstrDep.maxDysBk);
		String yr = InstrDep.getYear(i + session.InstrDep.maxDysBk);
		series_dtstr[i] = "'" + mt + "/" + dy + "/" + yr + "'";
	}	
	
  }
  
}


