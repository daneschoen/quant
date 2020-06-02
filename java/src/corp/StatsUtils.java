package program;

public class StatsUtils {

	  //* Calc the stdev of "C-C1" 
      //* var_s = 1/(N-1)*Sum(x_i - mu)^2
	  //*       = ( N*Sum(x^2) - (Sum_x)^2 ) / N(N-1)
  double[] feature;
  
  double mu=0.0;
  double fdStd_i=0.0;
  double fdZscore_i=0.0;
  
  
  public StatsUtils() {
  }

  
  public void stdev(double[] featExpr) {
	//feature = new double[cmdStdPeriod];
	feature = featExpr;
	int stdPeriod = feature.length;
	  
    for (int k=0; k<stdPeriod; k++)
	  mu += feature[k];
	mu /= stdPeriod;
	for (int k=0; k<stdPeriod; k++) {
	    fdStd_i += Math.pow(feature[k] - mu,2);
    }
	fdStd_i /= (stdPeriod-1);  //* unbiased
    fdStd_i = Math.sqrt(fdStd_i);
    
    fdZscore_i = (feature[stdPeriod-1] - mu)/fdStd_i;
  }
  
}
