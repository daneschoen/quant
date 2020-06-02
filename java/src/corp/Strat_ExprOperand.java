package program;

import java.util.HashMap;

public interface Strat_ExprOperand {
  
  double evaluate(HashMap <String, Integer> context);
	  
  void traverse(int level);
}
