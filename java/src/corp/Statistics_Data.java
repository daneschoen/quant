package program;

public class Statistics_Data {
	  
  public String head="";           //* Ran at ... condition cmds, ..., etc...
  
  public String[] obs_Hdr;         //* Y    M  D       W   PLAST  08:20  08:30  08:40  ..."
  public String[][] obsDt;        //* 2010 11 16  TUE
  public double[][] obsDelta;     //*                      plast  deltas_time, ....
    
  public String[] stats_Hdr;       //* D   HOUR     N     MAX     MIN      MU     MUD    PPOS    SDEV         T      TDRF
  public String[][] statsDyTime;   //* 0  09:35
                                   //*              5    1.75   -2.75   -0.35   -0.33   40.00    1.63    -48.13    -45.53
  public int cntN;
  public double[][] chgPrc;

  public double[] statsMin;
  public double[] statsMax;
  public double[] statsMinAvg;
  public double[] statsMaxAvg;  
  public double[] statsMed;
  public double[] statsMu;
  public double[] statsMuPos;
  public double[] statsMuNeg;
  public double[] statsMuAdj;
  public double[] statsPpos;
  public double[] statsPctPos;
  public double[] statsPctNeg;
  public double[] statsSdev;
  public double[] statsT;
  public double[] statsTdrf;
  public double[] statsDrift;
  public double[] statsVar;
  
}
