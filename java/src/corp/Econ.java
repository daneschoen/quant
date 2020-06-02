package program;

import java.util.Date;
import java.util.HashMap;
import java.util.Map;

public class Econ {
	
  public String name;
  public String fileName;
  
  public Date [] dt;
  
  public boolean blImported;
  
  /* 
   * Mutliton stuff 
   */
  private static final Map<String, Econ> instances = new HashMap<String, Econ>();

  private Econ()   //* also acceptable: protected, {default}
  { /* no explicit implementation */}

  public static Econ getInstance(String strKey)
  {
      synchronized (instances) {
          Econ instance = (Econ) instances.get(strKey);

          if (instance == null) {
              instance = new Econ();
              instances.put(strKey, instance);
              
              EconSetup.setupSpecs(instance, strKey);
          }
          return instance;
      }
  }  
  
}

