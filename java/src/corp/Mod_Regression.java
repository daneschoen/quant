package program;

import java.util.Arrays;

import program.stats.Regression;


class Mod_Regression {
  
  private static final int MAX_FEATURES = 6;
  
  String[] strX = new String[MAX_FEATURES];
  
  protected static String cmdY = "";
  protected static String cmdX1 = "";
  protected static String cmdX2 = "";
  protected static String cmdX3 = "";
  protected static String cmdX4 = "";
  protected static String cmdX5 = "";
  protected static String cmdX6 = "";
  
  
  private int num_features=0;
  private int len_series=0;
  
  private double[][] xData;
  private double[] yData;
  
  boolean bl_savecsv = false;
  
  public String strView = "";  //* X, Y only
  
  protected Session session;
  protected Instr InstrDep; 
  
		  
  public Mod_Regression(Session session) throws Exception{
	this.session = session;  
    InstrDep = session.InstrDep;
  }
  
  
  public void set_run_view() throws Exception{
	parseAndCalcFeature();
	//calcRegression(); --- regression now done in python
	
    Grapher grapher = new Grapher(session);
    grapher.series_name = new String[num_features+1];   //* +1 for y + featur
    grapher.series_name[0] = "Y : " + cmdY;
    for(int f=0; f<num_features; f++)
      grapher.series_name[f+1] = "X"+ (f+1) + ": " + strX[f];
    grapher.series_dtstr = new String[len_series];
    //grapher.series_fd = new double[num_features+1][session.endTstDateIndex-session.begTstDateIndex+1];
    grapher.series_fd = new double[num_features+1][len_series];   //* +1 for y + features   
    
    //* ONLY Regress and graph portion that is being regressed
    //grapher.series_fd[0] = plUnrealCum_long;   
    grapher.series_fd[0] = yData;   //Arrays.copyOfRange(yData, session.InstrDep.maxDysBk, session.endTstDateIndex+1);
    for(int f=0; f<num_features; f++)
      grapher.series_fd[f+1] = xData[f];   //Arrays.copyOfRange(xData[f], session.InstrDep.maxDysBk, session.endTstDateIndex+1);
    
    grapher.construct_dataset_regression();
    //strView  = ("DATA_SERIES_NAME:" + Arrays.deepToString(grapher.series_name));
    strView  = ("DATA_SERIES_NAME:" + Utils_IO.arrstr_to_string(grapher.series_name));
    strView += ("DATA_SERIES_DTSTR:" + Arrays.deepToString(grapher.series_dtstr));
    strView += ("DATA_SERIES_FD:" + Arrays.deepToString(grapher.series_fd));
    //strView += ("DATA_SERIES_FD:" + Arrays.deepToString(grapher.series_yx_str));
     
	/*
    strView  = ("DATA_SERIES_NAME:" + "foo");
    strView += ("DATA_SERIES_DTSTR:" + "bar");
    strView += ("DATA_SERIES_FD:" + "car");
    */
  }
  
  
  void parseAndCalcFeature() throws Exception{
	  
	num_features = 0;
	if (cmdX1.length() > 0) { 
	    strX[0] = cmdX1;
	    num_features++;   
	}  
	if (cmdX2.length() > 0) {
	    strX[1] = cmdX2;
	    num_features++;
	} 
	if (cmdX3.length() > 0) {
	    strX[2] = cmdX3;
	    num_features++;
	}  
	if (cmdX4.length() > 0) {
	    strX[3] = cmdX4;
	    num_features++;
	}  
	if (cmdX5.length() > 0) {
	    strX[4] = cmdX5;
	    num_features++;
	}  
	if (cmdX6.length() > 0) {
	    strX[5] = cmdX6;
	    num_features++;
	}  
	
	//* Parse and calc Y and X feature(s)
    //* Y
	Strat_Expression stratExpr = new Strat_Expression(InstrDep, cmdY, session);
	stratExpr.parseAndSetConditions();
	stratExpr.calc();
	
	//* X features
	Strat_Expression[] stratExprX = new Strat_Expression[num_features];
	for (int f=0; f<num_features; f++) {
	  stratExprX[f] = new Strat_Expression(InstrDep, strX[f], session);
	  stratExprX[f].parseAndSetConditions();  
	  stratExprX[f].calc();
	}
	
	//* Only concerned with calcd y-x mappings
	//len_series = session.endTstDateIndex - session.begTstDateIndex + 1;
    len_series = session.endTstDateIndex - InstrDep.maxDysBk + 1;
	yData = new double[len_series];
	for (int i=0; i<len_series; i++) {
		//yData[i] = stratExpr.calcdExprFn[maxExprDysBk + Strategy.begTstDateIndex + i];
		yData[i] = stratExpr.calcdExprFn[InstrDep.maxDysBk + i];
	}
	
	xData = new double[num_features][len_series];
	for (int f=0; f<num_features; f++) {
	    for (int i=0; i<len_series; i++) {
	    	//xData[f][i] = stratExprX[f].calcdExprFn[maxExprDysBk + Strategy.begTstDateIndex + i];    	
	    	xData[f][i] = stratExprX[f].calcdExprFn[InstrDep.maxDysBk + i];
	    }
	}
	
	if (bl_savecsv) {
	  for (int i=0; i<yData.length; i++) {
	    System.out.print(yData[i]);
	    for (int f=0; f<num_features; f++) {
	      System.out.print(" x" + f + " : " + xData[f][i]);		  
	    }
	    System.out.println();	
	  } 
	}	
	
  }	  
  
  /***
   * NOT BEING USED! REGRESSION STATISTICS CALCULATIONS IN PYTHON NOW
   */
  private void calcRegression() throws Exception{
	Regression reg;  
	if (num_features < 2) {
	    reg = new Regression(xData[0], yData);  //* public Regression(double[] x_Data, double[] yData){
	} else {
		reg = new Regression(xData, yData);     //* public Regression(double[][] xData, double[] yData){
	}
	//* setDefaultValues(xData, yData, weight);
	
	reg.calcLinear();  //* calls -> linear() -> generalLinear(), generalLinearStats()
	reg.displayStats();
	reg.plotLinear();  //* chart X1 vs Y only even when multivariate
  }
  
  
  private void test() throws Exception{
    double[] xArray = {0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0,5.5,6.0,6.5,7.0,7.5};
	double[] yArray = {10.9996,8.8481,7.1415,6.5376,6.466,5.1026,4.7215,3.7115,3.8383,3.4997,3.7972,3.4459,2.8564,3.291,3.0518,3.6073};
			
	Regression reg = new Regression(xArray, yArray);    
	reg.calcLinear();
	reg.displayStats();
	reg.plotLinear();  //* chart X1 vs Y only even when multivariate
  }
  
  
}	
