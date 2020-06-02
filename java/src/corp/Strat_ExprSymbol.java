package program;

import java.util.HashMap;

public class Strat_ExprSymbol implements Strat_ExprOperand{


    private String m_name;
    
    public Strat_ExprSymbol(String name) {
        m_name = name;
    }

    public void traverse(int level) {
        System.out.print(m_name + " ");
    }

    public double evaluate(HashMap <String, Integer> context) {
        return context.get(m_name);
    }
}
