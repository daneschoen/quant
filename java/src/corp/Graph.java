package program;

import javax.swing.JFrame;


public class Graph {
	
  public Graph() {
	  	  
  }
	
  public static void createAndShowGUI() {
    //* Create and set up the window.
	JFrame frameGraph = new JFrame("Tesla Trading Program - Graphs");
        
        //*Create and set up the content pane.
     //JComponent newContentPane = new Graph();
    //    newContentPane.setOpaque(true); //content panes must be opaque
    //    frameGraph.setContentPane(newContentPane);
        
    //* Display the window.
    frameGraph.pack();
    frameGraph.setSize(700,300);
    frameGraph.setVisible(true);
        
  }

  public static void go() {
    //* Schedule a job for the event-dispatching thread:
    //* creating and showing this application's GUI.
    javax.swing.SwingUtilities.invokeLater(new Runnable() {
      public void run() {
        createAndShowGUI();
      }
    });
  }
}
