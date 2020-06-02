/*
 *   Interface RegressionFunction2
 *   
 *   Interface for Regression class
 *   Sum of squares function for non-linear regression method
 *
 *   The sum of squares function, for multiple y array option, needed
 *   by the non-linear regression methods in the class Regression
 *   is supplied by means of this interface, RegressionFunction2
 *
 */

package program.stats;

public interface RegressionFunction2{
    double function(double[]param, double[] x, int i);
}