package program;

import java.awt.*;
import java.awt.event.*;
import java.awt.print.PrinterException;
import java.awt.print.PrinterJob;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

import javax.swing.*;

public class Gui extends JPanel implements ActionListener {
	
  private static final long serialVersionUID = 1L;	
    
  private static Utils utils;
  
   /*   A
    * B   E
    * C
    * D
    */
    
  public static JComboBox jdrp_AInstr;
  public static JComboBox jdrp_ATimeBase;
  public static JComboBox jdrp_ABegTstDate;
  public static JComboBox jdrp_AEndTstDate;
  JButton jbtn_AImport;
  JButton jbtn_APrint;
  JButton jbtn_ARun;
  static JCheckBox jchk_AImport;
  JLabel jlbl_Empty;
    
  JPanel jPanelEntry;
  JPanel jPanelExit;
  public static JTextArea jtxt_CmdConditions;
  public static JTextArea jtxt_CmdEventIntraDy;
  public static JTextArea jtxt_CmdExitDy;
  public static JTextArea jtxt_CmdExitIntraDy;
  
  public static JTextArea jtxt_SetView;
    
  //* Panel 1,2,3,4
  JPanel jPanelTabPane;
  JScrollPane jScrollPane;
  JPanel jPanel_Scenarios;
  public static JTabbedPane jtbPane;
  public static JTextArea jtxt_Scenarios;
  private static JCheckBox jchk_HiLo;
  private static JCheckBox jchk_RecProf;

  JPanel jPanel_Survival;
  private static JTextField jtxtBox_SurDayTarget;
  private static JTextField jtxtBox_SurTimeTarget;
  private static JTextField jtxtBox_SurWait0TimeTarget;
  JButton jbtn_Survival;

  JPanel jPanel_SysTrade;
  private static JTextField jtxtBox_SysMaxContracts;
  private static JCheckBox jchk_SysExitCondition;
  private static JTextField jtxtBox_SysExitTime;
  private static JCheckBox jchk_SysProfitTarget;
  private static JTextField jtxtBox_SysProfitTarget;
  private static JCheckBox jchk_SysSellStop;
  private static JTextField jtxtBox_SysSellStop;
  private static JCheckBox jchk_SysTimeTarget;
  private static JTextField jtxtBox_SysDayTarget;
  private static JTextField jtxtBox_SysTimeTarget;
  JButton jbtn_SysTrade;
  
    JPanel jPanel_EquityCurve;
    private static JTextField jtxtBox_EquDayTarget;
    private static JTextField jtxtBox_EquTimeTarget;
    JButton jbtn_EquityCurve;
    
    JPanel jPanel_Volatility;
    private static JTextField jtxtBox_VolHist_Days;
    private static JTextField jtxtBox_VolHist_Time;
    private static JTextField jtxtBox_VolHiLo_Days;
    JButton jbtn_Volatility;
    
   JPanel jPanel_CondProb;
   public static JTextArea jtxt_CondProb;    
   JButton jbtn_CondProb;
        
   JPanel jPanel_Regression;
   private static JTextField jtxtBox_Regr_Y;
   private static JTextField jtxtBox_Regr_X1;
   private static JTextField jtxtBox_Regr_X2;
   private static JTextField jtxtBox_Regr_X3;
   private static JTextField jtxtBox_Regr_X4;
   private static JTextField jtxtBox_Regr_X5;
   private static JTextField jtxtBox_Regr_X6;
   JButton jbtn_Regression;
        
   JComponent jpanel9;
    
    //* Output 
    public static JTextArea jtextArea;
    public static JTextArea jtextDummy;
        
  /* Constructor 
   * Put all the components in JPanel, etc.
   */
  public Gui() {
    super(new GridBagLayout());
        
    //Instr InstrDep = Instr.getInstance(Strategy.iDependentInstr);
    utils = new Utils();
        
    //* Populate dropdowns
    String listInstr[] = new String[InstrSpecs.TOT_INSTRS]; 
    for (int j=0; j<InstrSpecs.TOT_INSTRS; j++) { 
      listInstr[j] = InstrSpecs.idNames[j];     
    }
                
    String[] listTime = new String[1];
    listTime[0] = "  -  ";
        
	jdrp_AInstr = new JComboBox(listInstr);
    jdrp_AInstr.setSelectedIndex(0);
    jdrp_AInstr.addActionListener(new ActionListener() {
      public void actionPerformed(ActionEvent evt) {
        jdrp_AInstr_ActionPerformed(evt);
      }
    });

    jdrp_ATimeBase = new JComboBox(listTime);
    jdrp_ATimeBase.setSelectedIndex(0);
    jdrp_ATimeBase.addActionListener(new ActionListener() {
      public void actionPerformed(ActionEvent evt) {
        jdrp_ATimeBase_ActionPerformed(evt);
      }
    });
        
    String[] listTmp = new String[1];
    listTmp[0] = "     -     ";
    jdrp_ABegTstDate = new JComboBox(listTmp);
    jdrp_AEndTstDate = new JComboBox(listTmp);
    jdrp_ABegTstDate.setEditable(true);
    jdrp_AEndTstDate.setEditable(true);
    jdrp_ABegTstDate.setSelectedIndex(0);
    jdrp_AEndTstDate.setSelectedIndex(0);
    /* 
    jdrp_ABegTstDate.addActionListener(new ActionListener() {	
      public void actionPerformed(ActionEvent evt) {
        jdrp_ABegEndTstDate_ActionPerformed(evt);
      }
    
    });
    jdrp_AEndTstDate.addActionListener(new ActionListener() {
      public void actionPerformed(ActionEvent evt) {
        jdrp_ABegEndTstDate_ActionPerformed(evt);
      }
    });
    */             
    jbtn_AImport = new JButton("Import");
    jbtn_AImport.setVerticalTextPosition(AbstractButton.CENTER);
    jbtn_AImport.setHorizontalTextPosition(AbstractButton.CENTER); //aka LEFT, for left-to-right locales
    jbtn_AImport.setMnemonic(KeyEvent.VK_I);        
    jbtn_AImport.setToolTipText("Imports Dependent data, cleans, outputs formatted raw file");
    jbtn_AImport.setActionCommand("Import");
    jbtn_AImport.addActionListener(this);
    
    jbtn_APrint = new JButton("Print");
    jbtn_APrint.setVerticalTextPosition(AbstractButton.CENTER);
    jbtn_APrint.setHorizontalTextPosition(AbstractButton.CENTER); 
    jbtn_APrint.setMnemonic(KeyEvent.VK_P);
    jbtn_APrint.setActionCommand("Print");
    jbtn_APrint.addActionListener(new Print());
    //jbtn_APrint.addActionListener(this);
    
    jbtn_ARun = new JButton("Run");
    jbtn_ARun.setVerticalTextPosition(AbstractButton.CENTER);
    jbtn_ARun.setHorizontalTextPosition(AbstractButton.CENTER);
    jbtn_ARun.setMnemonic(KeyEvent.VK_R);
    jbtn_ARun.setActionCommand("Run");
    jbtn_ARun.addActionListener(this);
        
    jchk_AImport = new JCheckBox("Import All Instruments");
    jchk_AImport.setSelected(false);
        //jchk.addItemListener(this);
        
        /* Now add components in A */
        GridBagConstraints gbc = new GridBagConstraints();
        
        //EmptyBorder border = new EmptyBorder( new Insets( 0, 0, 0, 10 ) );
        //EmptyBorder border1 = new EmptyBorder( new Insets( 0, 20, 0, 10 ) );
        //jdrp_AInstr.setBorder(border);

        gbc.insets = new Insets( 10, 10, 5, 5 );  // (above,left,below,right)
        gbc.anchor = GridBagConstraints.WEST;       
        gbc.ipadx = 5;
        gbc.gridy = 0;
        gbc.gridx = 0;
        add(jdrp_AInstr, gbc);
        
        gbc.insets = new Insets( 10, 10, 5, 20 );
        gbc.gridx = 1;
        add(jdrp_ATimeBase, gbc);        
        
        gbc.insets = new Insets( 10, 5, 5, 5 );
        gbc.ipadx = 0;
        gbc.gridx = 2;
        add(jdrp_ABegTstDate, gbc);        
        gbc.insets = new Insets( 10, 5, 5, 5 );
        gbc.ipadx = 0;
        gbc.gridx = 3;
        add(jdrp_AEndTstDate, gbc);
        
        gbc.insets = new Insets( 10, 50, 5, 40 );
        gbc.ipadx = 35;
        gbc.gridx = 4;
        add(jbtn_ARun,gbc);
        gbc.insets = new Insets( 10, 10, 5, 40 );
        gbc.gridx = 5;
        add(jbtn_APrint,gbc);
        gbc.gridx = 6;
        add(jbtn_AImport,gbc);
        gbc.gridx = 7;
        add(jchk_AImport,gbc);    

        /*
        gbc.insets = new Insets( 10, 10, 5, 10 );
        jlbl_Empty = new JLabel("         ");
        gbc.gridx = 8;
        add(jlbl_Empty,gbc);
        */
        gbc.insets = new Insets( 5, 10, 5, 5 );
        gbc.ipadx = 1;
        gbc.ipady = 1;
        
        /* JPanel B */
        jtxt_CmdConditions = new JTextArea();
        jtxt_CmdConditions.setEditable(true);
        JScrollPane scrollpaneB = new JScrollPane(jtxt_CmdConditions,
        		                      JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED,
        		                      JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED);
        //jtxt_CmdConditions.addActionListener(this);        
        gbc.weightx = 1;
        gbc.weighty = 2;
        gbc.gridx = 0;
        gbc.gridy = 1;
        gbc.gridwidth = 4;
        gbc.gridheight = 2;
        //gbc.fill = GridBagConstraints.NONE; // Remember to reset to none        
        gbc.fill = GridBagConstraints.BOTH;
        add( scrollpaneB, gbc );

        
        /* JPanel C */
        jtxt_CmdExitDy = new JTextArea();
        jtxt_CmdExitDy.setEditable(true);
        JScrollPane scrollpaneC = new JScrollPane(jtxt_CmdExitDy,
        		                      JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED,
        		                      JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED);
        gbc.weightx = 1;
        gbc.weighty = 1;
        gbc.gridx = 0;
        gbc.gridy = 3;
        gbc.gridwidth = 4;
        gbc.gridheight = 1;
        //gbc.fill = GridBagConstraints.NONE; // Remember to reset to none        
        gbc.fill = GridBagConstraints.BOTH;
        add( scrollpaneC, gbc );

        
        /* JPanel D - Tabbed Pane */
        jtbPane = new JTabbedPane();
        //* Tab #1 - Set View Options
        jtxt_SetView = new JTextArea();
        jtxt_SetView.setEditable(true);
        JScrollPane scrollPane = new JScrollPane(jtxt_SetView);
        //JPanel panel1 = new JPanel(false);
        //panel1.setLayout(new GridLayout(1, 1));
        //panel1.add(scrollPaneC);
        //jtbPane.addTab("View Options", panel1);
        jtbPane.addTab("View Options", scrollPane);
        try {
          SetUserOptions.setDefault();  // fill only with default view specs
        } catch(Exception e) {
          //e.printStackTrace();
        }
        
        //* Tab #2 -         
        jPanel_Scenarios = new JPanel();
    	jPanel_Scenarios.setLayout(new GridBagLayout());
	    jtxt_Scenarios = new JTextArea();
        jtxt_Scenarios.setEditable(true);
        scrollPane = new JScrollPane(jtxt_Scenarios);
        jchk_HiLo = new JCheckBox("HiLo");
        jchk_RecProf = new JCheckBox("RecProf");
    	GridBagConstraints c = new GridBagConstraints();
    	c.fill = GridBagConstraints.HORIZONTAL;
        c.insets = new Insets(5,0,0,0);  //top padding
        c.weightx = 0.5;
	    c.gridx = 0;
	    c.gridy = 0;
        jPanel_Scenarios.add(jchk_HiLo,c);
	    c.gridx = 1;
	    c.gridy = 0;
        jPanel_Scenarios.add(jchk_RecProf,c);
	    c.gridx = 0;
	    c.gridy = 1;
        c.weightx = 0.0;
    	c.gridwidth = 4;
    	//c.gridheight = 10; //GridBagConstraints.REMAINDER;
    	//c.ipady = 40;
    	c.weighty = 1.0;   //request any extra vertical space
		//c.anchor = GridBagConstraints.PAGE_END;
		c.fill = GridBagConstraints.BOTH;
		c.insets = new Insets(5,0,0,0);  //top padding
        jPanel_Scenarios.add(scrollPane,c);
        jtbPane.addTab("Scenarios", jPanel_Scenarios);
        Scenarios.displayDefault();
        
        //* Tab #3 - Survival
        jPanel_Survival = new JPanel();
    	jPanel_Survival.setLayout(new GridBagLayout());
        jtxtBox_SurDayTarget = new JTextField("1");   
        jtxtBox_SurTimeTarget = new JTextField("1615");
        jtxtBox_SurWait0TimeTarget = new JTextField("1615");
        jbtn_Survival = new JButton("Run Survival");
        jbtn_Survival.setVerticalTextPosition(AbstractButton.CENTER);
        jbtn_Survival.setHorizontalTextPosition(AbstractButton.CENTER);
        jbtn_Survival.setActionCommand("Run Survival");
        jbtn_Survival.addActionListener(this);
    	c = new GridBagConstraints();
    	c.fill = GridBagConstraints.HORIZONTAL;
    	c.insets = new Insets(50,10,5,5);
        c.weightx = 1;
        c.weighty = 1;
	    c.gridx = 0;
	    c.gridy = 1;
	    JLabel jlbl = new JLabel("Hold To ");
	    jPanel_Survival.add(jlbl,c);
	    c.insets = new Insets(40,5,5,5);
	    c.gridx = 1;
	    c.gridy = 1;	     
        jPanel_Survival.add(jtxtBox_SurDayTarget,c);
        c.insets = new Insets(40,0,5,5);
	    c.gridx = 2;
	    c.gridy = 1;
	    jPanel_Survival.add(jtxtBox_SurTimeTarget,c);
	    c.insets = new Insets(40,30,5,5);
	    c.gridx = 3;
	    c.gridy = 1;	    
	    jPanel_Survival.add(jbtn_Survival,c);
	    c.insets = new Insets(5,10,70,5);
	    c.gridx = 0;
	    c.gridy = 2;
	    jlbl = new JLabel("Wait=0 Hold To ");
	    jPanel_Survival.add(jlbl,c);
	    c.insets = new Insets(5,0,70,5);
	    c.gridx = 2;
	    c.gridy = 2;
	    jPanel_Survival.add(jtxtBox_SurWait0TimeTarget,c);
        jtbPane.addTab("Survival", jPanel_Survival);
        
    //* Tab #4 - SysTrade
    jPanel_SysTrade = new JPanel();
    jPanel_SysTrade.setLayout(new GridBagLayout());
    jtxtBox_SysMaxContracts = new JTextField("1");
    jchk_SysExitCondition = new JCheckBox(" Exit Qualifiers     ");
    jchk_SysExitCondition.setSelected(true);
    jtxtBox_SysExitTime = new JTextField("1615");
    jchk_SysProfitTarget = new JCheckBox(" Profit Target     ");
    jtxtBox_SysProfitTarget = new JTextField("10.0   ");
    jchk_SysSellStop = new JCheckBox(" Stop Loss     ");
    jtxtBox_SysSellStop = new JTextField("10.0   ");
    jchk_SysTimeTarget = new JCheckBox(" Time Target     ");
    jtxtBox_SysDayTarget = new JTextField("1");   
    jtxtBox_SysTimeTarget = new JTextField("1615");
    jbtn_SysTrade = new JButton("Run SysTrade");
    jbtn_SysTrade.setVerticalTextPosition(AbstractButton.CENTER);
    jbtn_SysTrade.setHorizontalTextPosition(AbstractButton.CENTER);
    jbtn_SysTrade.setActionCommand("Run SysTrade");
    jbtn_SysTrade.addActionListener(this);
    c = new GridBagConstraints();
    c.fill = GridBagConstraints.HORIZONTAL;
	c.insets = new Insets(12,5,3,0);  
    c.gridx = 0; c.gridy = 1;
	JLabel jlbl_SysMaxContracts = new JLabel("       Max Contracts ");
	jPanel_SysTrade.add(jlbl_SysMaxContracts,c);
    c.gridx = 1;
	c.gridy = 1;	    
	jPanel_SysTrade.add(jtxtBox_SysMaxContracts,c);
  	c.insets = new Insets(12,0,0,12);
    c.weightx = 1; c.weighty = 1;
    c.gridx = 3; c.gridy = 1;
	jPanel_SysTrade.add(jbtn_SysTrade,c);
	c.insets = new Insets(0,5,3,1); 
	c.gridx = 0; c.gridy = 2;
    jPanel_SysTrade.add(jchk_SysExitCondition,c);        	    
	c.gridx = 1; c.gridy = 2;
    jPanel_SysTrade.add(jtxtBox_SysExitTime,c);
	c.gridx = 0; c.gridy = 3;
    jPanel_SysTrade.add(jchk_SysProfitTarget,c);        
	c.gridx = 1; c.gridy = 3;
    jPanel_SysTrade.add(jtxtBox_SysProfitTarget,c);
	c.gridx = 0; c.gridy = 4;
    jPanel_SysTrade.add(jchk_SysSellStop,c);
	c.gridx = 1; c.gridy = 4;
    jPanel_SysTrade.add(jtxtBox_SysSellStop,c);
    c.insets = new Insets(0,5,10,1); 
	c.gridx = 0; c.gridy = 5;
    jPanel_SysTrade.add(jchk_SysTimeTarget,c);
	c.gridx = 1; c.gridy = 5;
    jPanel_SysTrade.add(jtxtBox_SysDayTarget,c); 
	c.gridx = 2; c.gridy = 5;
	jPanel_SysTrade.add(jtxtBox_SysTimeTarget,c);
    jScrollPane = new JScrollPane(jPanel_SysTrade);
    jScrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED);
    jScrollPane.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED);
    jtbPane.addTab("SysTrade", jScrollPane);
        
    //* Panel 6 - Equity Curve
        jPanel_EquityCurve = new JPanel();
    	jPanel_EquityCurve.setLayout(new GridBagLayout());
        jtxtBox_EquDayTarget = new JTextField("1");   
        jtxtBox_EquTimeTarget = new JTextField("1615");
        jbtn_EquityCurve = new JButton("Run Equity Curve");
        jbtn_EquityCurve.setVerticalTextPosition(AbstractButton.CENTER);
        jbtn_EquityCurve.setHorizontalTextPosition(AbstractButton.CENTER);
        jbtn_EquityCurve.setActionCommand("Run Equity Curve");
        jbtn_EquityCurve.addActionListener(this);
    	c = new GridBagConstraints();
    	c.fill = GridBagConstraints.HORIZONTAL;
    	c.insets = new Insets(5,10,5,5);
        c.weightx = 1;
        c.weighty = 1;
	    c.gridx = 0;
	    c.gridy = 1;
	    jlbl = new JLabel("Hold Upto ");
	    jPanel_EquityCurve.add(jlbl,c);
	    c.insets = new Insets(5,5,5,5);
	    c.gridx = 1;
	    c.gridy = 1;	     
        jPanel_EquityCurve.add(jtxtBox_EquDayTarget,c);
        c.insets = new Insets(5,0,5,5);
	    c.gridx = 2;
	    c.gridy = 1;
	    jPanel_EquityCurve.add(jtxtBox_EquTimeTarget,c);
	    c.insets = new Insets(5,30,5,5);
	    c.gridx = 3;
	    c.gridy = 1;	    
	    jPanel_EquityCurve.add(jbtn_EquityCurve,c);
        jtbPane.addTab("Equity Curve", jPanel_EquityCurve);
        
        //* Tab #7 - Volatility
        jPanel_Volatility = new JPanel();
    	jPanel_Volatility.setLayout(new GridBagLayout());
        jtxtBox_VolHist_Days = new JTextField("10");   
        jtxtBox_VolHist_Time = new JTextField("1615");
        jtxtBox_VolHiLo_Days = new JTextField("10");
        jbtn_Volatility = new JButton("Chart Volatilility");
        jbtn_Volatility.setVerticalTextPosition(AbstractButton.CENTER);
        jbtn_Volatility.setHorizontalTextPosition(AbstractButton.CENTER);
        jbtn_Volatility.setActionCommand("Chart Volatility");
        jbtn_Volatility.addActionListener(this);
    	c = new GridBagConstraints();
    	c.fill = GridBagConstraints.HORIZONTAL;
    	c.insets = new Insets(50,10,5,5);
        c.weightx = 1;
        c.weighty = 1;
	    c.gridx = 0;
	    c.gridy = 1;
	    jlbl = new JLabel("Hist Vol ");
	    jPanel_Volatility.add(jlbl,c);
	    c.insets = new Insets(40,5,5,5);
	    c.gridx = 1;
	    c.gridy = 1;	     
        jPanel_Volatility.add(jtxtBox_VolHist_Days,c);
        c.insets = new Insets(40,0,5,5);
	    c.gridx = 2;
	    c.gridy = 1;
	    jPanel_Volatility.add(jtxtBox_VolHist_Time,c);
	    c.insets = new Insets(40,30,5,5);
	    c.gridx = 3;
	    c.gridy = 1;	    
	    jPanel_Volatility.add(jbtn_Volatility,c);
	    c.insets = new Insets(5,10,70,5);
	    c.gridx = 0;
	    c.gridy = 2;
	    jlbl = new JLabel("HiLo Vol ");
	    jPanel_Volatility.add(jlbl,c);
	    c.insets = new Insets(5,0,70,5);
	    c.gridx = 2;
	    c.gridy = 2;
	    jPanel_Volatility.add(jtxtBox_VolHiLo_Days,c);
    if(AGlobal.BUILD_VER == 1)
      jtbPane.addTab("Volatility", jPanel_Volatility);
        
    //* Tab #8 - Conditional Probability        
    jPanel_CondProb = new JPanel();
    jPanel_CondProb.setLayout(new GridBagLayout());
	jtxt_CondProb = new JTextArea();
	jtxt_CondProb.setFont(new java.awt.Font("Courier", Font.PLAIN, 11));
    scrollPane = new JScrollPane(jtxt_CondProb);
    jbtn_CondProb = new JButton("Probability");
    jbtn_CondProb.setVerticalTextPosition(AbstractButton.CENTER);
    jbtn_CondProb.setHorizontalTextPosition(AbstractButton.CENTER);
    jbtn_CondProb.setActionCommand("Probability");
    jbtn_CondProb.addActionListener(this);
    c = new GridBagConstraints();
    c.fill = GridBagConstraints.HORIZONTAL;
    c.insets = new Insets(5,0,0,0);  //top padding
    c.weightx = 0.5;
    //c.weightx = 1;
    //c.weighty = 1;
	c.gridx = 1;
	c.gridy = 0;     
	jPanel_CondProb.add(jbtn_CondProb,c);
	c.gridx = 0;
	c.gridy = 1;
    c.weightx = 0.0;
    c.gridwidth = 4;
    c.weighty = 1.0;   //request any extra vertical space
	c.fill = GridBagConstraints.BOTH;
	c.insets = new Insets(5,0,0,0);  //top padding
	jPanel_CondProb.add(scrollPane,c);
    if(AGlobal.BUILD_VER == 1)
      jtbPane.addTab("Probability", jPanel_CondProb);
        
    //* Tab #9 - Regression
    jPanel_Regression = new JPanel();
    jPanel_Regression.setLayout(new GridBagLayout());
    jtxtBox_Regr_Y = new JTextField();   
    jtxtBox_Regr_X1 = new JTextField();
    jtxtBox_Regr_X2 = new JTextField();
    jtxtBox_Regr_X3 = new JTextField();
    jtxtBox_Regr_X4 = new JTextField();
    jtxtBox_Regr_X5 = new JTextField();
    jtxtBox_Regr_X6 = new JTextField();    
    jbtn_Regression = new JButton("Run Regression");
    jbtn_Regression.setVerticalTextPosition(AbstractButton.CENTER);
    jbtn_Regression.setHorizontalTextPosition(AbstractButton.CENTER);
    jbtn_Regression.setActionCommand("Run Regression");
    jbtn_Regression.addActionListener(this);   
    c = new GridBagConstraints();
    c.fill = GridBagConstraints.HORIZONTAL;
    c.insets = new Insets(10,10,10,10);    
    c.gridx = 0;
    c.gridy = 0;    
    jlbl = new JLabel(" ");
	jPanel_Regression.add(jlbl,c);
    c.gridx = 1;
    c.gridy = 0;    
    jlbl = new JLabel("                             ");
	jPanel_Regression.add(jlbl,c);
    c.gridx = 2;
    c.gridy = 0;        
    jPanel_Regression.add(jbtn_Regression,c);
    c.insets = new Insets(0,10,0,0);  //(50,10,5,5);
    c.gridwidth = 1;
    c.gridx = 0;
    c.gridy = 1;    
	jlbl = new JLabel("Y  ");
	jPanel_Regression.add(jlbl,c);
	c.insets = new Insets(0,0,0,0);
	c.gridwidth = 2;
	c.gridx = 1;
	c.gridy = 1;
    jPanel_Regression.add(jtxtBox_Regr_Y,c);
    c.insets = new Insets(0,10,0,0);
    c.gridwidth = 1;
    c.weightx = 1;
	c.gridx = 0;
	c.gridy = 2;
	jlbl = new JLabel("X1  ");
	jPanel_Regression.add(jlbl,c);
	c.insets = new Insets(0,0,0,0);
	c.gridwidth = 2;
	c.gridx = 1;
	c.gridy = 2;
	jPanel_Regression.add(jtxtBox_Regr_X1,c);   
	c.insets = new Insets(0,10,0,0);
	c.gridwidth = 1;
	c.gridx = 0;
	c.gridy = 3;
	jlbl = new JLabel("X2  ");
	jPanel_Regression.add(jlbl,c);
	c.insets = new Insets(0,0,0,0);
	c.gridwidth = 2;
	c.gridx = 1;
	c.gridy = 3;	     
	jPanel_Regression.add(jtxtBox_Regr_X2,c);   
	c.insets = new Insets(0,10,0,0);
	c.gridwidth = 1;
	c.gridx = 0;
	c.gridy = 4;
	jlbl = new JLabel("X3  ");
	jPanel_Regression.add(jlbl,c);
	c.insets = new Insets(0,0,0,0);
	c.gridwidth = 2;
	c.gridx = 1;
	c.gridy = 4;	     
	jPanel_Regression.add(jtxtBox_Regr_X3,c);   
	c.insets = new Insets(0,10,0,0);
	c.gridwidth = 1;
	c.gridx = 0;
	c.gridy = 5;
	jlbl = new JLabel("X4  ");
	jPanel_Regression.add(jlbl,c);
	c.insets = new Insets(0,0,0,0);
	c.gridwidth = 2;
	c.gridx = 1;
	c.gridy = 5;	     
	jPanel_Regression.add(jtxtBox_Regr_X4,c);
	c.insets = new Insets(0,10,0,0);
	c.gridwidth = 1;
	c.gridx = 0;
	c.gridy = 6;
	jlbl = new JLabel("X5  ");
	jPanel_Regression.add(jlbl,c);
	c.insets = new Insets(0,0,0,0);
	c.gridwidth = 2;
	c.gridx = 1;
	c.gridy = 6;	     
	jPanel_Regression.add(jtxtBox_Regr_X5,c);   
	c.insets = new Insets(0,10,0,0);
	c.gridwidth = 1;
	c.gridx = 0;
	c.gridy = 7;
	jlbl = new JLabel("X6  ");
	jPanel_Regression.add(jlbl,c);
	c.insets = new Insets(0,0,0,0);
	c.gridwidth = 2;
	c.gridx = 1;
	c.gridy = 7;	     
	jPanel_Regression.add(jtxtBox_Regr_X6,c);   
    jScrollPane = new JScrollPane(jPanel_Regression);
    jScrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED);
    jScrollPane.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED);
    jtbPane.addTab("Regression", jScrollPane);
    //JScrollPane scrollPane=new JScrollPane(panel);
    //instead of scrollPane.add(panel);
        
    /*
    jpanelX = makeTextPanel("Panel #9");
    //?jpanelX.setPreferredSize(new Dimension(410, 50));
    jtbPane.addTab("Tab 9", jpanel9);
    */
        
    //* Now add the entire tabbed pane
    jtbPane.setTabLayoutPolicy(JTabbedPane.SCROLL_TAB_LAYOUT);
    gbc.gridx = 0;
    gbc.gridy = 4;
    gbc.weighty = 0;
    gbc.gridwidth = 4;
    gbc.gridheight = 1;//GridBagConstraints.REMAINDER;
    //gbc.fill = GridBagConstraints.NONE;
    add(jtbPane, gbc);
        
    /* 
     * JPanel E 
     */
    gbc.insets = new Insets( 5, 5, 15, 10 );
    jtextArea = new JTextArea(100, 100);
    jtextArea.setEditable(false);   
    jtextArea.setFont(new java.awt.Font("Courier", Font.PLAIN, 11));
    JScrollPane scrollPaneE = new JScrollPane(jtextArea,
                                              JScrollPane.VERTICAL_SCROLLBAR_ALWAYS,
                                              JScrollPane.HORIZONTAL_SCROLLBAR_ALWAYS);
    gbc.gridwidth = GridBagConstraints.REMAINDER;
    gbc.gridx = 4;
    gbc.gridy = 1;
    gbc.gridheight = 6; //GridBagConstraints.REMAINDER;
    gbc.fill = GridBagConstraints.BOTH;
    add(scrollPaneE, gbc);
    jtextArea.append(AGlobal.strVER + "\n");
                    
  }  //* end constructor
    
    
  /* ACTIONS */
  public void actionPerformed(ActionEvent evt) {
    if ("Import".equals(evt.getActionCommand())) {
    	SimpleDateFormat sdf = new SimpleDateFormat("MM/dd/yyyy HH:mm:ss");
    	String strText = sdf.format(new Date());
    	jtextArea.setText("Importing at " + strText + "\n\n");
    	  
    	importEcon();      //* NOTE: Must import econ bef dep bec prices need to be scrubbed of hol's
    	importDependent();
    	jtextArea.setCaretPosition(0);
        
    } else if ("Print".equals(evt.getActionCommand())) {
    	  /*
    	  try {       	       
    	     setPrint();
	    	 Print print = new Print();
	    	 print.run();              
    	  } catch (Exception e) {	
      		  Gui.jtextArea.append("Error printing\n");
      		  Gui.jtextArea.append(e.toString() + "\n\n");  
      	  }
          */
    	  /*
          PrinterJob job = PrinterJob.getPrinterJob();
          job.setPrintable(new Printer());
          boolean ok = job.printDialog();
          if (ok) {
              try {
                   job.print();
              } catch (PrinterException ex) {
               //* The job did not successfully complete
              }
          }
    	  */
    } else if ("Run".equals(evt.getActionCommand())) {   
    	
    	if (checkDates()) {
    		try {
    	      jtextArea.setText("Running commands ...\n\n");   
    	      setScenarios();
    	      Parser parser = new Parser(); 	      
              parser.run();  // inside checks for import of dep or indp yet   
              
	        } catch(Exception e) {	  
			  Gui.jtextArea.append("ERROR Parser.go - Running of Strategy failed: " + e + "\n\n");
	        }  
    	}  
    	  
      } else if ("Run SysTrade".equals(evt.getActionCommand())) {   	   
    	  if (checkDates()) {
    		  try {
    	        jtextArea.setText("Running SysTrade ...\n\n");
    	        setScenarios();	
    	        setSysTrade();
    	        Mod_SysTrade sysTrade = new Mod_SysTrade();
    	        sysTrade.run();
    		  } catch (Exception e) {	
    			Gui.jtextArea.append("Error in SysTrade: \n");
    			Gui.jtextArea.append(e.toString() + "\n\n");  
    		  }
    	  }  
    	      	  
      } else if ("Run Survival".equals(evt.getActionCommand())) {   	   
    	  if (checkDates()) {
    		  try {
    	        jtextArea.setText("Running Survival ...\n\n");
    	        setScenarios();
    	        setSurvival();
	    	    Mod_Survival survival = new Mod_Survival();
	    	    survival.run();
    		  } catch (Exception e) {	
      			Gui.jtextArea.append("Error in Survival: \n");
      			Gui.jtextArea.append(e.toString() + "\n\n");  
      		  }
	    	    
    	  }
    	  
      } else if ("Run Equity Curve".equals(evt.getActionCommand())) {   	   
    	  if (checkDates()) {
    		  try {
    	        jtextArea.setText("Running Equity Curve ...\n\n");   
    	        setScenarios();
    	        setEquityCurve();
	    	    Mod_EquityCurve equitycurve = new Mod_EquityCurve();
	    	    equitycurve.run();              
    		  } catch (Exception e) {	
      			Gui.jtextArea.append("Error in Equity Curve: \n");
      			Gui.jtextArea.append(e.toString() + "\n\n");  
      		  }    
    	  }
    	  
      } else if ("Chart Volatility".equals(evt.getActionCommand())) {   	   
    	  if (checkDates()) {
    		  try {
    	        jtextArea.setText("Chart Volatility ...\n\n");

    	        setScenarios();
    	        setVolatility();
	    	    Mod_Volatility volatility = new Mod_Volatility();
	    	    volatility.run();
	    	    
    		  } catch (Exception e) {	
      			Gui.jtextArea.append("Error in Volatility: \n");
      			Gui.jtextArea.append(e.toString() + "\n\n");  
      		  }    
    	  }
       
      } else if ("Probability".equals(evt.getActionCommand())) {   	   
  	      if (checkDates()) {
  		      try {
  	            //jtextArea.setText("Calculating Probability ...\n\n");

  	            setScenarios();
  	            setCondProbability();
	    	    Mod_CondProb condProb = new Mod_CondProb();
	    	    condProb.run();
	    	    
  		    } catch (Exception e) {	
    		    Gui.jtxt_CondProb.append("Error in Probability: \n");
    		    Gui.jtxt_CondProb.append(e.toString() + "\n\n");  
  		    } 	    
  	      }
  	      
      } else if ("Run Regression".equals(evt.getActionCommand())) {
  	      if (checkDates()) {
    		  try {
    	        jtextArea.setText("Calculating Regression ...\n\n");

    	        setScenarios();
    	        setRegression();
  	    	    Mod_Regression regr = new Mod_Regression();
  	    	    regr.run();
  	    	    
    		  } catch (Exception e) {	
      		    Gui.jtxt_CondProb.append("Error in Regression: \n");
      		    Gui.jtxt_CondProb.append(e.toString() + "\n\n");  
    		  } 	    
    	  }

      }

    }  //* method actionPerformed
    
    
  public void jdrp_AInstr_ActionPerformed(ActionEvent evt) {
      //JComboBox cb = (JComboBox)evt.getSource();
      //String instrSelect = (String)cb.getSelectedItem();
    Strategy.iDependentInstr = jdrp_AInstr.getSelectedIndex();
      //* Must update time stamps corresponding to the dependent var
  	refreshDrpTstDates();
  	refreshDrpTimeStamps();
  	  
  	jtextArea.setText("Changed dependent instrument to " + InstrSpecs.idNames[Strategy.iDependentInstr] + "\n");
  	jtextArea.setCaretPosition(0);
  }
    
    
  public void jdrp_ATimeBase_ActionPerformed(ActionEvent evt) {
      //JComboBox cb = (JComboBox)evt.getSource();
      //String strTimeSelect = (String)cb.getSelectedItem();
    Instr InstrDep = Instr.getInstance(Strategy.iDependentInstr);
    	
    int i = jdrp_ATimeBase.getSelectedIndex();
    if (i >= 0) {
        if(i==0)
    	  Strategy.timeRefCol = InstrDep.opnDyCol;	  
        else if(i==1)
      	  Strategy.timeRefCol = InstrDep.clsDyCol;
        else
    	  Strategy.timeRefCol = InstrDep.firstTimeCol + i-2;  
    }
  }
    
  /* this gets run from check dates instead since combobox editable now      
    public void jdrp_ABegEndTstDate_ActionPerformed(ActionEvent evt) {
      //Strategy.begTstDateIndex = jdrp_ABegTstDate.getSelectedIndex();
	  //Strategy.endTstDateIndex = jdrp_AEndTstDate.getSelectedIndex();
    }
  */
   
  //* Checks: combo box editable
  private boolean checkDates() {   
      
  	if (jdrp_ABegTstDate.getSelectedIndex() < 0) {
  		Instr InstrDep = Instr.getInstance(Strategy.iDependentInstr);
        try {
        	
          String strBadDate = (String)jdrp_ABegTstDate.getSelectedItem();
          DateFormat formatter = new SimpleDateFormat(AGlobal.DATE_FORMAT);
          Date date = (Date)formatter.parse(strBadDate);
          
          boolean blDateFound = false;
          int index=-1;
          for (int i=0; i<InstrDep.prc.length; i++) {
            String strADate = (String)jdrp_ABegTstDate.getItemAt(i);      
            Date aDate = (Date)formatter.parse(strADate);      
            if (aDate.after(date)) {
            	index = i;
            	blDateFound = true;
            	break;
            }
          }
          
          if (blDateFound) {
        	  jdrp_ABegTstDate.setSelectedIndex(index);
          }	else {
        	  jdrp_ABegTstDate.setSelectedIndex(0);
          }
          
  	      //jtextArea.setText("ERROR: Dates do not exist. \n");
  	      //jtextArea.setCaretPosition(0);
 	    } catch (ParseException e) {
 	    	jdrp_ABegTstDate.setSelectedIndex(0);
	    } 
  	}

  	if (jdrp_AEndTstDate.getSelectedIndex() < 0) {
  		Instr InstrDep = Instr.getInstance(Strategy.iDependentInstr);
        try {
        	
          String strBadDate = (String)jdrp_AEndTstDate.getSelectedItem();
          DateFormat formatter = new SimpleDateFormat(AGlobal.DATE_FORMAT);
          Date date = (Date)formatter.parse(strBadDate);
            
          boolean blDateFound = false;
          int index=-1;
          for (int i=0; i<InstrDep.prc.length; i++) {
              String strADate = (String)jdrp_AEndTstDate.getItemAt(i);
              Date aDate = (Date)formatter.parse(strADate);
              if (date.before(aDate)) {
              	  index = i;
              	  blDateFound = true;
              	  break;
              }
          }
            
          if (blDateFound) {
              if (index-1 >= 0) {
                    jdrp_AEndTstDate.setSelectedIndex(index-1);
              } else {
            		jdrp_AEndTstDate.setSelectedIndex(index);
              }
          } else {
          	  jdrp_AEndTstDate.setSelectedIndex(InstrDep.prc.length-1);
          }
            
   	    } catch (ParseException e) {
   	      jdrp_AEndTstDate.setSelectedIndex(InstrDep.prc.length-1);
  	    } 
    }

	Strategy.begTstDateIndex = jdrp_ABegTstDate.getSelectedIndex();
    Strategy.endTstDateIndex = jdrp_AEndTstDate.getSelectedIndex();
  	return true;
  }

    
  /* 
   * private methods 
   */
    protected JComponent makeTextPanel(String text) {
      JPanel panel = new JPanel(false);
      JLabel filler = new JLabel(text);
      filler.setHorizontalAlignment(JLabel.CENTER);
      panel.setLayout(new GridLayout(1, 1));
      panel.add(filler);
      return panel;
    }
    
  /*  
   * public static methods
   */
  public static void importDependent() {
    	
  	jtextArea.append("Importing dependent var...\n");
  	  
  	ImportDataConvert importDataConvert = new ImportDataConvert();
  	if (jchk_AImport.isSelected()) {
  	    for (int r=0; r<InstrSpecs.TOT_INSTRS; r++) {
  	    	Instr InstrX = Instr.getInstance(r);  
  	        try {
  	    	  jtextArea.append("Importing instrument: " + InstrSpecs.idNames[r] + "\n");
  	    	  
  	    	  importDataConvert.go(r);
  	    	  /*
  	    	  importDataConvert.importFile(r); 	
  	    	  importDataConvert.scrubPrices(r); 	    	
  	    	  importDataConvert.outputNewRawFile(r);
  	    	  */
              InstrX.blImported = true;
              jtextArea.append("\n");
  	        } catch (Exception e) {
  	          InstrX.blImported = false;
  	          jtextArea.append("ERROR importing instrument: " + InstrSpecs.idNames[r] + "\n");
  			  Gui.jtextArea.append(e + "\n\n");
  		    }
  	      }  
          refreshDrpTstDates();
          refreshDrpTimeStamps();
             	
  	} else {
  		Instr InstrDep = Instr.getInstance(Strategy.iDependentInstr);
  	    try {	 	  
  	      importDataConvert.go(Strategy.iDependentInstr);              
          InstrDep.blImported = true;
          jtextArea.append("\n");
            
          refreshDrpTstDates();
          refreshDrpTimeStamps();
        
          //jtextArea.selectAll();
          //jtextArea.setCaretPosition(jtextArea.getDocument().getLength());
	    } catch (Exception e) {
	      InstrDep.blImported = false;  
	  	  jtextArea.append("ERROR importing instrument: " + InstrSpecs.idNames[Strategy.iDependentInstr] + "\n");
	      Gui.jtextArea.append(e + "\n\n");
	    }         
  	}  
  	  
  }  //* method importDependent

    
  public static void importEcon() {
    	 
    jtextArea.append("Importing economic data...\n");
    	  
    for (int k=0; k<EconSetup.TOT_ECON; k++) {
        Econ EconX = Econ.getInstance(EconSetup.name[k]);
  	    ImportEcon.importFile(EconX.name);
  	    EconX.blImported = true;
    }  
    jtextArea.append("\n");
                             
  }

    
  private static void refreshDrpTstDates() {
    Instr InstrDep = Instr.getInstance(Strategy.iDependentInstr);
    SimpleDateFormat sdfDt = new SimpleDateFormat("MM/dd/yyyy");
        
    //* Update date dropdowns only with dependent var
        //listBegEndTstDate = new String[InstrSpecs.TOT_INSTRS];
    jdrp_ABegTstDate.removeAllItems();
    jdrp_AEndTstDate.removeAllItems();
        
    if (!InstrDep.blImported) {
        jdrp_ABegTstDate.addItem("-");        	
        jdrp_AEndTstDate.addItem("-");        	
    } else {
        for (int i=0;i<InstrDep.prc.length;i++) {    
            jdrp_ABegTstDate.addItem(sdfDt.format(InstrDep.prcDate[i]));        	
            jdrp_AEndTstDate.addItem(sdfDt.format(InstrDep.prcDate[i]));        	
        }
        jdrp_ABegTstDate.setSelectedIndex(0);
        if(InstrDep.idName.equals("ES"))
          jdrp_ABegTstDate.setSelectedIndex(1508);
        	
        jdrp_AEndTstDate.setSelectedIndex(InstrDep.prc.length-1);

    	  //Strategy.begTstDateIndex = jdrp_ABegTstDate.getSelectedIndex();  // defaults
	      //Strategy.endTstDateIndex = jdrp_AEndTstDate.getSelectedIndex();
    	Strategy.begTstDateIndex = 0;  // defaults
	    Strategy.endTstDateIndex = InstrDep.prc.length-1;
      }
  }


  private static void refreshDrpTimeStamps() {
	    //* When switching dependent but assume already imported

    	/*
        String[] listTime = new String[51];
        listTime[0] = "O";
        listTime[1] = "C";
		Calendar timeStamp = new GregorianCalendar(2006,0,1,8,10,0);
		Format sdf = new SimpleDateFormat("HH:mm");
		String strTime = sdf.format(timeStamp.getTime());
		for (int j=2; j<51; j++) {  // 41+4=45 
		  timeStamp.add(Calendar.MINUTE,10);
		  strTime = sdf.format(timeStamp.getTime());
		  listTime[j] = strTime;    
		}
    	*/
    	
    jdrp_ATimeBase.removeAllItems();
    Instr InstrDep = Instr.getInstance(Strategy.iDependentInstr);    	
    if (!InstrDep.blImported) {
    	jdrp_ATimeBase.addItem("-"); 	
    } else {
        jdrp_ATimeBase.addItem("O");
        jdrp_ATimeBase.addItem("C");        
        for(int i=0; i<InstrDep.totTimeSteps; i++)
          jdrp_ATimeBase.addItem(InstrDep.prcTime[InstrDep.firstTimeCol+i]);        	
        jdrp_ATimeBase.setSelectedIndex(1);
        Strategy.timeRefCol = InstrDep.clsDyCol;
    }
  }
    
    
  private static void setScenarios() {
    if(jchk_HiLo.isSelected())
      Scenarios.bl_HiLo = true;
    else 
      Scenarios.bl_HiLo = false;
   
    if(jchk_RecProf.isSelected())
      Scenarios.bl_RecProf = true;
    else
      Scenarios.bl_RecProf = false;

    Scenarios.strCmdWindow = jtxt_Scenarios.getText(); 
  }

    
  private static void setSysTrade() throws Exception{
    Instr InstrDep = Instr.getInstance(Strategy.iDependentInstr);	
    Mod_SysTrade.strEntryDyWindow = jtxt_CmdConditions.getText().trim().toLowerCase();
    //Mod_SysTrade.strEnterIntradyWindow = jtxt_CmdEventIntraDy.getText().trim().toLowerCase();
    Mod_SysTrade.strExitDyWindow = jtxt_CmdExitDy.getText().trim().toLowerCase();
    //Mod_SysTrade.strExitIntradyWindow = jtxt_CmdExitIntraDy.getText().trim().toLowerCase();
    Mod_SysTrade.cmdMaxOpenContracts = Integer.parseInt(jtxtBox_SysMaxContracts.getText().trim());
 
    if (!jchk_SysExitCondition.isSelected()) {
    	Mod_SysTrade.blChk_Exit_Condition = false;
    } else {
    	Mod_SysTrade.blChk_Exit_Condition = true;
        String strTime = jtxtBox_SysExitTime.getText().trim().toLowerCase();
        Mod_SysTrade.cmdExitConditionTimeStr = strTime;
        Mod_SysTrade.cmdExitConditionTimeCol = InstrDep.getTimeCol(strTime); 
    }
    
    if (!jchk_SysProfitTarget.isSelected()) {
    	Mod_SysTrade.blChk_Exit_ProfitTarget = false;
    	Mod_SysTrade.blChk_Exit_ProfitTargetZ = false;
    } else {
    	String strProfitTarget = jtxtBox_SysProfitTarget.getText().trim();
		Mod_SysTrade.evtProfitBegFrameTimeCol = InstrDep.firstTimeCol;
		Mod_SysTrade.evtProfitEndFrameTimeCol = InstrDep.lastTimeCol;
		Mod_SysTrade.evtProfitBegDyFwd = 0;
		Mod_SysTrade.evtProfitEndDyFwd = 9999999;
		Mod_SysTrade.evtProfitBegTimeCol = Strategy.timeRefCol+1;  //*
		Mod_SysTrade.evtProfitEndTimeCol = InstrDep.lastTimeCol;
    	if (strProfitTarget.indexOf("z") > 0) {
    	    Mod_SysTrade.blChk_Exit_ProfitTarget = false;
    	    Mod_SysTrade.blChk_Exit_ProfitTargetZ = true;
    	    Mod_SysTrade.cmdExitProfitTargetZ = Double.parseDouble(strProfitTarget.substring(0,strProfitTarget.indexOf("z")).trim());
    		Mod_SysTrade.evtProfitStdPeriod = 40;
    		if(Strategy.maxDysBk < Mod_SysTrade.evtProfitStdPeriod+1) 
    		  Strategy.maxDysBk = Mod_SysTrade.evtProfitStdPeriod+1;
    	} else {
    		Mod_SysTrade.blChk_Exit_ProfitTarget = true;
    		Mod_SysTrade.blChk_Exit_ProfitTargetZ = false;
    		Mod_SysTrade.cmdExitProfitTargetPr = Double.parseDouble(strProfitTarget);	
    	}	    	    
    }
    
    if (!jchk_SysSellStop.isSelected()) {
    	Mod_SysTrade.blChk_Exit_StopLoss = false;
    	Mod_SysTrade.blChk_Exit_StopLossZ = false;
    } else {
    	String strStopLoss = jtxtBox_SysSellStop.getText().trim();
		Mod_SysTrade.evtStopBegFrameTimeCol = InstrDep.firstTimeCol;
		Mod_SysTrade.evtStopEndFrameTimeCol = InstrDep.lastTimeCol;
		Mod_SysTrade.evtStopBegDyFwd = 0;
		Mod_SysTrade.evtStopEndDyFwd = 9999999;
		Mod_SysTrade.evtStopBegTimeCol = Strategy.timeRefCol+1;  //*
		Mod_SysTrade.evtStopEndTimeCol = InstrDep.lastTimeCol;
    	if (strStopLoss.indexOf("z") > 0) {
    		Mod_SysTrade.blChk_Exit_StopLoss = false;
    		Mod_SysTrade.blChk_Exit_StopLossZ = true;	
    		Mod_SysTrade.cmdExitStopZ = Double.parseDouble(strStopLoss.substring(0,strStopLoss.indexOf("z")).trim());
    		Mod_SysTrade.evtStopStdPeriod = 40;
    		if(Strategy.maxDysBk < Mod_SysTrade.evtStopStdPeriod+1) 
      		  Strategy.maxDysBk = Mod_SysTrade.evtStopStdPeriod+1;
    	} else {
    		Mod_SysTrade.blChk_Exit_StopLoss = true;
    		Mod_SysTrade.blChk_Exit_StopLossZ = false;
    		Mod_SysTrade.cmdExitStopPr = Double.parseDouble(strStopLoss);	
    	}	
    }
    
    if (!jchk_SysTimeTarget.isSelected()) {
    	Mod_SysTrade.blChk_Exit_TimeTargetRel = false;
    	Mod_SysTrade.blChk_Exit_TimeTargetFix = false;
    } else {
    	Mod_SysTrade.blChk_Exit_TimeTargetRel = true;
    	Mod_SysTrade.blChk_Exit_TimeTargetFix = false;
    	Mod_SysTrade.cmdExitTimeTarget_DysFwd = Integer.parseInt(jtxtBox_SysDayTarget.getText().trim());
    	String strTime = jtxtBox_SysTimeTarget.getText().trim();
    	Mod_SysTrade.cmdExitTimeTargetStr = strTime;
    	Mod_SysTrade.cmdExitTimeTarget_Col = InstrDep.getTimeCol(strTime); 
    }
              
  }
  
  
  private static void setEquityCurve() throws Exception{
	Instr InstrDep = Instr.getInstance(Strategy.iDependentInstr);	
	      	
	Mod_EquityCurve.strEntryWindow = jtxt_CmdConditions.getText().trim();
	Mod_EquityCurve.cmdTimeTarget_DysFwd = Integer.parseInt(jtxtBox_EquDayTarget.getText().trim());
	String strTime = jtxtBox_EquTimeTarget.getText().trim();
	Mod_EquityCurve.cmdstrTimeTarget = strTime;
	Mod_EquityCurve.cmdExitTimeCol = InstrDep.getTimeCol(strTime);
  }
  
  
  private static void setSurvival() throws Exception{
    Instr InstrDep = Instr.getInstance(Strategy.iDependentInstr);	
      	
    Mod_Survival.strEntryWindow = jtxt_CmdConditions.getText().trim();
    Mod_Survival.CmdiExitDysFwd = Integer.parseInt(jtxtBox_SurDayTarget.getText().trim());
    String strTime = jtxtBox_SurTimeTarget.getText().trim();
    Mod_Survival.CmdstrExitTime = strTime;
    Mod_Survival.CmdiExitCol = Utils.strTimeToCol(strTime, InstrDep);
    strTime = jtxtBox_SurWait0TimeTarget.getText().trim();
    Mod_Survival.CmdstrWait0ExitTime = strTime;
    Mod_Survival.CmdiWait0ExitCol = Utils.strTimeToCol(strTime, InstrDep);
  }
   
  
    private static void setVolatility() throws Exception{
      Instr InstrDep = Instr.getInstance(Strategy.iDependentInstr);	
        	
      //Mod_Volatility.strEntryWindow = jtxt_CmdConditions.getText().trim();
      String strDays = jtxtBox_VolHist_Days.getText().trim();
      Mod_Volatility.cmdstrVolHist_Days = strDays;
      Mod_Volatility.cmdVolHist_Days = Integer.parseInt(strDays);
      String strTime = jtxtBox_VolHist_Time.getText().trim();
      Mod_Volatility.cmdstrVolHist_Time = strTime;
      Mod_Volatility.cmdVolHist_TimeCol = Utils.strTimeToCol(strTime, InstrDep);
      
      strDays = jtxtBox_VolHiLo_Days.getText().trim();
      Mod_Volatility.cmdVolHiLo_Days = Integer.parseInt(strDays);
    }
    
    
    private static void setCondProbability() throws Exception{      	
      Mod_CondProb.strWindowPosterior = jtxt_CmdConditions.getText().trim();
      Mod_CondProb.strWindowConditional = jtxt_CmdExitDy.getText().trim();
    }

    
    private static void setPrint() throws Exception{      	
      //Print.strWindow = jtextArea.getText();
    }

    
  private static void setRegression() throws Exception{	
    Mod_Regression.cmdY = jtxtBox_Regr_Y.getText().trim();
    Mod_Regression.cmdX1 = jtxtBox_Regr_X1.getText().trim();
    Mod_Regression.cmdX2 = jtxtBox_Regr_X2.getText().trim();
    Mod_Regression.cmdX3 = jtxtBox_Regr_X3.getText().trim();
    Mod_Regression.cmdX4 = jtxtBox_Regr_X4.getText().trim();
    Mod_Regression.cmdX5 = jtxtBox_Regr_X5.getText().trim();
    Mod_Regression.cmdX6 = jtxtBox_Regr_X6.getText().trim();
  }
    
    
  /**
   * Create the GUI and show it.  For thread safety,
   * this method should be invoked from the event-dispatching thread.
   */
  public static void createAndShowGUI() {
    //* Create and set up the window.
    JFrame frame = new JFrame(AGlobal.TITLE);
    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    //* Create and set up the content pane.
    JComponent newContentPane = new Gui();
    newContentPane.setOpaque(true); //content panes must be opaque
    frame.setContentPane(newContentPane);
        
    //* Display the window.
    frame.pack();
    frame.setSize(1240,740);
    frame.setVisible(true);      
  }

  public static void start() {
    //* Schedule a job for the event-dispatching thread:
    //* creating and showing this application's GUI.
    javax.swing.SwingUtilities.invokeLater(new Runnable() {
      public void run() {
        createAndShowGUI();
      }
    });
  }
}

