package program;

import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.event.*;
import java.awt.print.*;


public class Print implements Printable, ActionListener {
    
  int[] pageBreaks;  // array of page break line positions.

  /* Synthesise some sample lines of text */
  String[] textLines;
  
  private void initTextLines() {
    //if (textLines == null) {
    	/*
            int numLines=200;
            textLines = new String[numLines];
            for (int i=0;i<numLines;i++) {
                textLines[i]= "This is line number " + i;
            }
        */    
    	String s = Gui.jtextArea.getText();
    	textLines = s.split("\n");
    //}
  }
	
	
  public int print(Graphics g, PageFormat pf, int pageIndex) throws
                                                        PrinterException {

        Font font = new Font("Serif", Font.PLAIN, 10);
        Font font1 = new Font("Courier", Font.PLAIN, 7);
        FontMetrics metrics = g.getFontMetrics(font1);
        int lineHeight = metrics.getHeight();
        
        /*
        PageFormat documentPageFormat = new PageFormat();
        documentPageFormat.setOrientation(PageFormat.LANDSCAPE);
        pf = documentPageFormat;
        */
        //if (pageBreaks == null) {
            initTextLines();
            int linesPerPage = (int)(pf.getImageableHeight()/lineHeight);
            int numBreaks = (textLines.length-1)/linesPerPage;
            pageBreaks = new int[numBreaks];
            for (int b=0; b<numBreaks; b++) {
                pageBreaks[b] = (b+1)*linesPerPage; 
            }
        //}

        if (pageIndex > pageBreaks.length) {
            return NO_SUCH_PAGE;
        }

        /* User (0,0) is typically outside the imageable area, so we must
         * translate by the X and Y values in the PageFormat to avoid clipping
         */
        Graphics2D g2d = (Graphics2D)g;
        g2d.translate(pf.getImageableX(), pf.getImageableY());
        
        int y = 0; 
        int start = (pageIndex == 0) ? 0 : pageBreaks[pageIndex-1];
        int end   = (pageIndex == pageBreaks.length)
                         ? textLines.length : pageBreaks[pageIndex];
        g.setFont(font1);
        for (int line=start; line<end; line++) {
            y += lineHeight;
            g.drawString(textLines[line], 0, y);
        
        }

        /* tell the caller that this page is part of the printed document */
        return PAGE_EXISTS;
    }
    

    public void actionPerformed(ActionEvent e) {
    
      PrinterJob job = PrinterJob.getPrinterJob();
      job.setPrintable(this);
      boolean ok = job.printDialog();
      if (ok) {
          try {
            job.print();
          } catch (PrinterException ex) {
             /* The job did not successfully complete */
          }
      }
    }

   
}