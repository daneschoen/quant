package program;

import java.util.Date;
import java.util.HashMap;
import java.util.Map;

public class Indicators {
	
  public String fnName;  //* = key
  
  public double [][] data;    //* [][0]: mth, [][1]: day, [][2]: yr, [][3]: dayOfWk
  public Date[] date;      //* = new Calendar[MaxRow];
  
  public boolean blImported;
  
  /* 
   * Mutliton stuff 
   */
  private static final Map<Object, Indicators> instances = new HashMap<Object, Indicators>();

  private Indicators()   //* also acceptable: protected, {default}
  { /* no explicit implementation */}

  public static Indicators getInstance(Object key)
  {
      synchronized (instances) {
          Indicators instance = (Indicators) instances.get(key);

          if (instance == null) {
              instance = new Indicators();
              instances.put(key, instance);
              
              String strKey = key.toString();
              IndicatorsSetup.setupSpecs(instance, strKey);
          }
          return instance;
      }
  }  
  
}