package program;

import java.util.Calendar;
import java.util.HashMap;
import java.util.Map;

public class Multiton {
	
  public String fnName;
  public String fileName;
  
  public int [][] dates;    //* [][0]: mth, [][1]: day, [][2]: yr, [][3]: dayOfWk
  public Calendar[] cal;    //* = new Calendar[MaxRow];
  
  public int maxCols;
  public boolean blImported;
  
  /* 
   * Mutliton stuff 
   */
  private static final Map<Object, Multiton> instances = new HashMap<Object, Multiton>();

  private Multiton()   //* also acceptable: protected, {default}
  { /* hide this */}

  public static Multiton getInstance(Object key) 
  {
      synchronized (instances) {
          Multiton instance = (Multiton) instances.get(key);

          if (instance == null) {
              instance = new Multiton();
              instances.put(key, instance);
              
              String strKey = key.toString();
              int instrKey = Integer.parseInt(strKey);
              //EconSetup.setupSpecs(instance, strKey);
          }
          return instance;
      }
  }  
  
}