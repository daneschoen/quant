/*
 *   Interface RegressionFunction
 *
 *   The sum of squares function needed by the
 *   non-linear regression methods in the class Regression
 *   is supplied by means of this interface, RegressionFunction
 *
 */

package program.stats;

// Interface for Regression class
// Sum of squares function for non-linear regression methods
public interface RegressionFunction{
    double function(double[]param, double[] x);
}