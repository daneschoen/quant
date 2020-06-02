/**************************************************************************************
 *   Interface IntegralFunction
 *
 *   This interface provides the abstract method through which
 *   functions to be integrated by methods in the Class Integration
 *   may be coded and supplied to the Integration class.
 *
 *
 *
 ***************************************************************************************/

package program.stats;

// Interface for Integration class
public interface IntegralFunction{
    	double function(double x);
}