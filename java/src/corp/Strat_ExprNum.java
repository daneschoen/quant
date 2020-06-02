package program;

import java.util.HashMap;

public class Strat_ExprNum implements Strat_ExprOperand{
    private double m_value;

    public Strat_ExprNum(double value) {
        m_value = value;
    }

    public void traverse(int level) {
        System.out.print(m_value + " ");
    }

    public double evaluate(HashMap context) {
        return m_value;
    }

}
