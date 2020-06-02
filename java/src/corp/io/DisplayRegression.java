package program.io;

import java.awt.Font;
import java.io.*;
import java.math.*;
import java.text.*;
import java.util.*;

import javax.swing.JTextArea;

import program.Gui;
import program.stats.*;


public class DisplayRegression{
	
  public JTextArea viewer = Gui.jtextArea;	
        
  private boolean append = false;     // true data appended to a file, false new file
  private char app = 'w';             // 'w' new file - overwrites an existing file of the same name
                                      // 'a' append to existing file, creates a new file if file does not exist
                                      // 'n' adds a number to file name. If file name of that number exists creates a file with next highest number added to name
  public DisplayRegression(){
    this.app = 'w';
    viewer.setFont(new java.awt.Font("Courier", Font.PLAIN, 11));
    viewer.setText("");
    this.append = false;                
  }
  
  public DisplayRegression(char c){
    this.app = c;
	    
	if (this.app == 'a'){
	    this.append=true;
	} else {
	    this.append = false;
	    viewer.setText("");
	}           
  }
  
  
  public void display(String s) {
	  Gui.jtextArea.append(s);
  }
  
  public void displayln(String s) {
	  Gui.jtextArea.append(s + "\n");
  }

  public void display(double dd) {
	Gui.jtextArea.append(dd + "");
  }
	        
  public void displayln(double dd) {
	 Gui.jtextArea.append(dd + "\n");
  }

  public void display(boolean bool) {
	if (bool) {  
        Gui.jtextArea.append("true");
	} else {
		Gui.jtextArea.append("false");
	}
  }

  public void displayln(boolean bool) {
	if (bool) {  
	    Gui.jtextArea.append("true\n");
	} else {
		Gui.jtextArea.append("false\n");
    }
  }
  
  // Prints string, no line return
        public final synchronized void print(String word){
                display(word);
        }

        // Prints double, no line return
        public final synchronized void print(double dd){
                display(dd);
        }

        
        // Prints float, no line return
        public final synchronized void print(float ff){
                display(ff);
        }

        // Prints BigDecimal, no line return
        public final synchronized void print(BigDecimal big){
                display(big.toString());
        }


        // Prints BigInteger, no line return
        public final synchronized void print(BigInteger big){
                display(big.toString());
        }



        // Prints int, no line return
        public final synchronized void print(int ii){
                display(ii);
        }

        // Prints int, no line return, fixed field length
        public final synchronized void print(int ii, int f){
                String ss ="";
                ss = ss + ii;
                ss = DisplayRegression.setField(ss,f);
                display(ss);
        }

        // Prints long integer, no line return
        public final synchronized void print(long ll){
                display(ll);
        }

        // Prints long integer, no line return, fixed field length
        public final synchronized void print(long ll, int f){
                String ss ="";
                ss = ss + ll;
                ss = DisplayRegression.setField(ss,f);
                display(ss);
        }

        // Prints short integer, no line return
        public final synchronized void print(short ss){
                display(ss);
        }

        // Prints short integer, no line return, fixed field length
        public final synchronized void print(short si, int f){
                String ss ="";
                ss = ss + si;
                ss = DisplayRegression.setField(ss,f);
                display(ss);
        }


        // Prints boolean, no line return
        public final synchronized void print(boolean bb){
                display(bb);
        }

        // Prints boolean, no line return, fixed field length
        public final synchronized void print(boolean bb, int f){
                String ss ="";
                ss = ss + bb;
                ss = DisplayRegression.setField(ss,f);
                display(ss);
        }

        // Prints array of doubles, no line return
        public final synchronized void print(double[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                }
        }

        // Prints array of floats, no line return
        public final synchronized void print(float[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                }
        }

/*        
        // Prints array of BigDecimal, no line return
        public final synchronized void print(BigDecimal[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                }
        }

        // Prints array of BigInteger, no line return
        public final synchronized void print(BigInteger[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                }
        }
*/
        
        // Prints array of int, no line return
        public final synchronized void print(int[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                }
        }

        // Prints array of short, no line return
        public final synchronized void print(short[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                }
        }

        // Prints array of byte, no line return
        public final synchronized void print(byte[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                }
        }

        // Prints array of char, no line return
        public final synchronized void print(char[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                }
        }

        // Prints array of boolean, no line return
        public final synchronized void print(boolean[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                }
        }

        // Prints array of Strings, no line return
        public final synchronized void print(String[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                }
        }



        // Prints array of doubles, no line return, fixed field length
        public final synchronized void print(double[] array, int f){
                int n = array.length;
                for(int i=0; i<n; i++){
                    String ss ="";
                    ss = ss + array[i];
                    ss = DisplayRegression.setField(ss,f);
                    display(ss);
                }
        }

        // Prints array of floats, no line return, fixed field length
        public final synchronized void print(float[] array, int f){
                int n = array.length;
                for(int i=0; i<n; i++){
                    String ss ="";
                    ss = ss + array[i];
                    ss = DisplayRegression.setField(ss,f);
                    display(ss);
                }
        }

        // Prints array of BigDecimal, no line return, fixed field length
        public final synchronized void print(BigDecimal[] array, int f){
                int n = array.length;
                for(int i=0; i<n; i++){
                    String ss ="";
                    ss = ss + array[i];
                    ss = DisplayRegression.setField(ss,f);
                    display(ss);
                }
        }

        // Prints array of BigInteger, no line return, fixed field length
        public final synchronized void print(BigInteger[] array, int f){
                int n = array.length;
                for(int i=0; i<n; i++){
                    String ss ="";
                    ss = ss + array[i];
                    ss = DisplayRegression.setField(ss,f);
                    display(ss);
                }
        }

        // Prints array of long, no line return, fixed field length
        public final synchronized void print(long[] array, int f){
                int n = array.length;
                for(int i=0; i<n; i++){
                    String ss ="";
                    ss = ss + array[i];
                    ss = DisplayRegression.setField(ss,f);
                    display(ss);
                }
        }

        // Prints array of int, no line return, fixed field length
        public final synchronized void print(int[] array, int f){
                int n = array.length;
                for(int i=0; i<n; i++){
                    String ss ="";
                    ss = ss + array[i];
                    ss = DisplayRegression.setField(ss,f);
                    display(ss);
                }
        }

        // Prints array of short, no line return, fixed field length
        public final synchronized void print(short[] array, int f){
                int n = array.length;
                for(int i=0; i<n; i++){
                    String ss ="";
                    ss = ss + array[i];
                    ss = DisplayRegression.setField(ss,f);
                    display(ss);
                }
        }

        // Prints array of byte, no line return, fixed field length
        public final synchronized void print(byte[] array, int f){
                int n = array.length;
                for(int i=0; i<n; i++){
                    String ss ="";
                    ss = ss + array[i];
                    ss = DisplayRegression.setField(ss,f);
                    display(ss);
                }
        }

        // Prints array of char, no line return, fixed field length
        public final synchronized void print(char[] array, int f){
                int n = array.length;
                for(int i=0; i<n; i++){
                    String ss ="";
                    ss = ss + array[i];
                    ss = DisplayRegression.setField(ss,f);
                    display(ss);
                }
        }

        // Prints array of boolean, no line return, fixed field length
        public final synchronized void print(boolean[] array, int f){
                int n = array.length;
                for(int i=0; i<n; i++){
                    String ss ="";
                    ss = ss + array[i];
                    ss = DisplayRegression.setField(ss,f);
                    display(ss);
                }
        }

        // Prints array of Strings, no line return, fixed field length
        public final synchronized void print(String[] array, int f){
                int n = array.length;
                for(int i=0; i<n; i++){
                    String ss ="";
                    ss = ss + array[i];
                    ss = DisplayRegression.setField(ss,f);
                    display(ss);
                }
        }



  //* Display date and time  (no line return);
  public final synchronized void dateAndTime(){
    Date d = new Date();
    String day = DateFormat.getDateInstance().format(d);
    String tim = DateFormat.getTimeInstance().format(d);

    display("Regression calculated at ");
    display(tim);
    display(" on ");
    display(day);
  }


        // PRINT WITH SPACE (NO LINE RETURN)
        // Prints character plus space, no line return
        public final synchronized void printsp(char ch){
                display(ch);
                display(" ");
        }

        // Prints string plus space, no line return
        public final synchronized void printsp(String word){
                display(word + " ");
        }

        // Prints double plus space, no line return
        public final synchronized void printsp(double dd){
                display(dd);
                display(" ");
        }

        // Prints float plus space, no line return
        public final synchronized void printsp(float ff){
                display(ff);
                display(" ");
        }

        // Prints BigDecimal plus space, no line return
        public final synchronized void printsp(BigDecimal big){
                display(big.toString());
                display(" ");
        }

        // Prints BigInteger plus space, no line return
        public final synchronized void printsp(BigInteger big){
                display(big.toString());
                display(" ");
        }

        // Prints Complex plus space, no line return
        public final synchronized void printsp(Complex ff){
                display(ff.toString());
                display(" ");
        }


        // Prints ErrorProp plus space, no line return
        public final synchronized void printsp(ErrorProp ff){
                display(ff.toString());
                display(" ");
        }

        // Prints ComplexErrorProp plus space, no line return
        public final synchronized void printsp(ComplexErrorProp ff){
                display(ff.toString());
                display(" ");
        }

        // Prints int plus space, no line return
        public final synchronized void printsp(int ii){
                display(ii);
                display(" ");
        }

        // Prints long integer plus space, no line return
        public final synchronized void printsp(long ll){
                display(ll);
                display(" ");
        }

        // Prints short integer plus space, no line return
        public final synchronized void printsp(short ss){
                display(ss);
                display(" ");
        }

        // Prints byte integer plus space, no line return
        public final synchronized void printsp(byte by){
                display(by);
                display(" ");
        }

        // Prints boolean plus space, no line return
        public final synchronized void printsp(boolean bb){
                display(bb);
                display(" ");
        }

        // Prints  space, no line return
        public final synchronized void printsp(){
                display(" ");
        }

        // Prints array of doubles, separated by spaces
        public final synchronized void printsp(double[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display(" ");
                }
        }

        // Prints array of floats, separated by spaces
        public final synchronized void printsp(float[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display(" ");
                }
        }

        
/*        
        // Prints array of BigDecimal, separated by spaces
        public final synchronized void printsp(BigDecimal[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display(" ");
                }
        }

        // Prints array of BigInteger, separated by spaces
        public final synchronized void printsp(BigInteger[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display(" ");
                }
        }
*/
        
        // Prints array of long, separated by spaces
        public final synchronized void printsp(long[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display(" ");
                }
        }

        // Prints array of int, separated by spaces
        public final synchronized void printsp(int[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display(" ");
                }
        }

        // Prints array of char, separated by spaces
        public final synchronized void printsp(char[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display(" ");
                }
        }

        // Prints array of short, separated by spaces
        public final synchronized void printsp(short[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display(" ");
                }
        }

        // Prints array of byte, separated by spaces
        public final synchronized void printsp(byte[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display(" ");
                }
        }

        // Prints array of boolean, separated by spaces
        public final synchronized void printsp(boolean[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display(" ");
                }
        }

        // Prints array of Strings, separated by spaces
        public final synchronized void printsp(String[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display(" ");
                }
        }


        // Prints date and time (plus space, no line return);
        public final synchronized void dateAndTimesp(){
                Date d = new Date();
                String day = DateFormat.getDateInstance().format(d);
                String tim = DateFormat.getTimeInstance().format(d);

                display("This file was created at ");
                display(tim);
                display(" on ");
                display(day);
                display(" ");
        }

        // Prints file title (title), date and time  (no line return);
        public final synchronized void dateAndTimesp(String title){
                Date d = new Date();
                String day = DateFormat.getDateInstance().format(d);
                String tim = DateFormat.getTimeInstance().format(d);

                display("This file, "+title+", was created at ");
                display(tim);
                display(" on ");
                display(day);
                display(" ");
        }

        
  public final synchronized void println(){
    viewer.append("\n");
  }
        
  public final synchronized void println(char ch){
    viewer.append(ch + "\n");
  }

  public final synchronized void println(String s){
	viewer.append(s + "\n");
  }
  
  public final synchronized void println(double dd){
    viewer.append(dd + "\n");
  }

  public final synchronized void println(float ff){
	viewer.append(ff + "\n");
  }

  public final synchronized void println(BigDecimal big){
	viewer.append(big.toString() + "\n");
  }

  public final synchronized void println(BigInteger big){
	viewer.append(big.toString() + "\n");
  }
  
  public final synchronized void println(Complex ff){
	viewer.append(ff.toString() + "\n");
  }
  
  public final synchronized void println(ErrorProp ff){
	viewer.append(ff.toString() + "\n");
  }

        // Prints ComplexErrorProp with line return
        public final synchronized void println(ComplexErrorProp ff){
                displayln(ff.toString());
        }

        // Prints int with line return
        public final synchronized void println(int ii){
                displayln(ii);
        }

        // Prints long integer with line return
        public final synchronized void println(long ll){
                displayln(ll);
        }

        // Prints short integer with line return
        public final synchronized void println(short ss){
                displayln(ss);
        }

        // Prints byte integer with line return
        public final synchronized void println(byte by){
                displayln(by);
        }

        // Prints boolean with line return
        public final synchronized void println(boolean bb){
                displayln(bb);
        }

        // Prints array of doubles, each followed by a line return
        public final synchronized void println(double[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    displayln(array[i]);
                }
        }

        // Prints array of floats, each followed by a line return
        public final synchronized void println(float[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    displayln(array[i]);
                 }
        }


        // Prints array of long, each followed by a line return
        public final synchronized void println(long[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    displayln(array[i]);
                }
        }

        // Prints array of int, each followed by a line return
        public final synchronized void println(int[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    displayln(array[i]);
                }
        }

        // Prints array of short, each followed by a line return
        public final synchronized void println(short[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    displayln(array[i]);
                }
        }

        // Prints array of byte, each followed by a line return
        public final synchronized void println(byte[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    displayln(array[i]);
                }
        }

        // Prints array of char, each followed by a line return
        public final synchronized void println(char[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    displayln(array[i]);
                }
        }

        // Prints array of Strings, each followed by a line return
        public final synchronized void println(String[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    displayln(array[i]);
                }
        }

        
  public final synchronized void dateAndTimeln(){
    Date d = new Date();
    String day = DateFormat.getDateInstance().format(d);
    String tim = DateFormat.getTimeInstance().format(d);

    print("Calculated at ");
    print(tim);
    print(" on ");
    println(day);
  }

  // Prints file title (title), date and time (with line return);
        public final synchronized void dateAndTimeln(String title){
                Date d = new Date();
                String day = DateFormat.getDateInstance().format(d);
                String tim = DateFormat.getTimeInstance().format(d);

                print("This file, "+title+", was created at ");
                print(tim);
                print(" on ");
                println(day);
        }

        // PRINT WITH FOLLOWING TAB, NO LINE RETURN
        // Prints character plus tab, no line return
        public final synchronized void printtab(char ch){
                print(ch);
                print("\t");
        }

        // Prints character plus tab, no line return, fixed field length
        public final synchronized void printtab(char ch, int f){
                String ss ="";
                ss = ss + ch;
                ss = DisplayRegression.setField(ss,f);
                print(ss);
                print("\t");
        }

        // Prints string plus tab, no line return
        public final synchronized void printtab(String word){
                display(word + "\t");
        }

        // Prints string plus tab, no line return, fixed field length
        public final synchronized void printtab(String word, int f){
            String ss ="";
                ss = ss + word;
                ss = DisplayRegression.setField(ss,f);
                display(ss);
                display("\t");
        }

        // Prints double plus tab, no line return
        public final synchronized void printtab(double dd){
                display(dd);
                display("\t");
        }

        // Prints double plus tab, fixed field length, fixed field length
        public final synchronized void printtab(double dd, int f){
                String ss ="";
                ss = ss + dd;
                ss = DisplayRegression.setField(ss,f);
                display(ss);
                display("\t");
        }

        // Prints float plus tab, no line return
        public final synchronized void printtab(float ff){
                display(ff);
                display("\t");
        }

        // Prints float plus tab, no line return, fixed field length
        public final synchronized void printtab(float ff, int f){
                String ss ="";
                ss = ss + ff;
                ss = DisplayRegression.setField(ss,f);
                display(ss);
                display("\t");
        }

        // Prints BigDecimal plus tab, no line return
        public final synchronized void printtab(BigDecimal big){
                display(big.toString());
                display("\t");
        }

        // Prints BigDecimal plus tab, no line return, fixed field length
        public final synchronized void printtab(BigDecimal big, int f){
                String ss ="";
                ss = ss + big.toString();
                ss = DisplayRegression.setField(ss,f);
                display(ss);
                display("\t");
        }

        // Prints BigInteger plus tab, no line return
        public final synchronized void printtab(BigInteger big){
                display(big.toString());
                display("\t");
        }

        // Prints BigInteger plus tab, no line return, fixed field length
        public final synchronized void printtab(BigInteger big, int f){
                String ss ="";
                ss = ss + big.toString();
                ss = DisplayRegression.setField(ss,f);
                display(ss);
                display("\t");
        }


        // Prints Complex plus tab, no line return, fixed field length
        public final synchronized void printtab(Complex ff, int f){
                String ss ="";
                ss = ss + ff;
                ss = DisplayRegression.setField(ss,f);
                display(ss);
                display("\t");
        }

        public final synchronized void printtab(Complex ff){
            display(ff.toString());
            display("\t");
        }


        // Prints ErrorProp plus tab, no line return
        public final synchronized void printtab(ErrorProp ff){
                display(ff.toString());
                display("\t");
        }

        // Prints ErrorProp plus tab, no line return, fixed field length
        public final synchronized void printtab(ErrorProp ff, int f){
                String ss ="";
                ss = ss + ff;
                ss = DisplayRegression.setField(ss,f);
                display(ss);
                display("\t");
        }

        // Prints ComplexErrorProp plus tab, no line return
        public final synchronized void printtab(ComplexErrorProp ff){
                display(ff.toString());
                display("\t");
        }

        // Prints ComplexErrorProp plus tab, no line return, fixed field length
        public final synchronized void printtab(ComplexErrorProp ff, int f){
                String ss ="";
                ss = ss + ff;
                ss = DisplayRegression.setField(ss,f);
                display(ss);
                display("\t");
        }

        // Prints int plus tab, no line return
        public final synchronized void printtab(int ii){
                display(ii);
                display("\t");
        }

        // Prints int plus tab, no line return, fixed field length
        public final synchronized void printtab(int ii, int f){
               String ss ="";
                ss = ss + ii;
                ss = DisplayRegression.setField(ss,f);
                display(ss);
                display("\t");
        }

        // Prints long integer plus tab, no line return
        public final synchronized void printtab(long ll){
                display(ll);
                display("\t");
        }

        // Prints long integer plus tab, no line return, fixed field length
        public final synchronized void printtab(long ll, int f){
               String ss ="";
                ss = ss + ll;
                ss = DisplayRegression.setField(ss,f);
                display(ss);
                display("\t");
        }

        // Prints short integer plus tab, no line return
        public final synchronized void printtab(short ss){
                display(ss);
                display("\t");
        }

        // Prints short integer plus tab, no line return, fixed field length
        public final synchronized void printtab(short si, int f){
               String ss ="";
                ss = ss + si;
                ss = DisplayRegression.setField(ss,f);
                display(ss);
                display("\t");
        }

        // Prints byte integer plus tab, no line return
        public final synchronized void printtab(byte by){
                display(by);
                display("\t");
        }

        // Prints byte integer plus tab, no line return, fixed field length
        public final synchronized void printtab(byte by, int f){
               String ss ="";
                ss = ss + by;
                ss = DisplayRegression.setField(ss,f);
                display(ss);
                display("\t");
        }

        // Prints boolean plus tab, no line return
        public final synchronized void printtab(boolean bb){
                display(bb);
                display("\t");
        }

        // Prints boolean plus tab, no line return, fixed field length
        public final synchronized void printtab(boolean bb, int f){
                String ss ="";
                ss = ss + bb;
                ss = DisplayRegression.setField(ss,f);
                display(ss);
                display("\t");
        }

        // Prints tab, no line return
        public final synchronized void printtab(){
                display("\t");
        }

        // Prints array of doubles, tab, no line return, fixed field length
        public final synchronized void printtab(double[] array, int f){
                int n = array.length;
                for(int i=0; i<n; i++){
                    String ss ="";
                    ss = ss + array[i];
                    ss = DisplayRegression.setField(ss,f);
                    display(ss);
                    display("\t");
                }
        }

        // Prints array of floats, tab, no line return, fixed field length
        public final synchronized void printtab(float[] array, int f){
                int n = array.length;
                for(int i=0; i<n; i++){
                    String ss ="";
                    ss = ss + array[i];
                    ss = DisplayRegression.setField(ss,f);
                    display(ss);
                    display("\t");
                }
        }

        // Prints array of BigDecimal, tab, no line return, fixed field length
        public final synchronized void printtab(BigDecimal[] array, int f){
                int n = array.length;
                for(int i=0; i<n; i++){
                    String ss ="";
                    ss = ss + array[i].toString();
                    ss = DisplayRegression.setField(ss,f);
                    display(ss);
                    display("\t");
                }
        }

        // Prints array of BigInteger, tab, no line return, fixed field length
        public final synchronized void printtab(BigInteger[] array, int f){
                int n = array.length;
                for(int i=0; i<n; i++){
                    String ss ="";
                    ss = ss + array[i].toString();
                    ss = DisplayRegression.setField(ss,f);
                    display(ss);
                    display("\t");
                }
        }


        // Prints array of long, tab, no line return, fixed field length
        public final synchronized void printtab(long[] array, int f){
                int n = array.length;
                for(int i=0; i<n; i++){
                    String ss ="";
                    ss = ss + array[i];
                    ss = DisplayRegression.setField(ss,f);
                    display(ss);
                    display("\t");
                }
        }

        // Prints array of int, tab, no line return, fixed field length
        public final synchronized void printtab(int[] array, int f){
                int n = array.length;
                for(int i=0; i<n; i++){
                    String ss ="";
                    ss = ss + array[i];
                    ss = DisplayRegression.setField(ss,f);
                    display(ss);
                    display("\t");
                }
        }

        // Prints array of short, tab, no line return, fixed field length
        public final synchronized void printtab(short[] array, int f){
                int n = array.length;
                for(int i=0; i<n; i++){
                    String ss ="";
                    ss = ss + array[i];
                    ss = DisplayRegression.setField(ss,f);
                    display(ss);
                    display("\t");
                }
        }

        // Prints array of byte, tab, no line return, fixed field length
        public final synchronized void printtab(byte[] array, int f){
                int n = array.length;
                for(int i=0; i<n; i++){
                    String ss ="";
                    ss = ss + array[i];
                    ss = DisplayRegression.setField(ss,f);
                    display(ss);
                    display("\t");
                }
        }

        // Prints array of char, tab, no line return, fixed field length
        public final synchronized void printtab(char[] array, int f){
                int n = array.length;
                for(int i=0; i<n; i++){
                    String ss ="";
                    ss = ss + array[i];
                    ss = DisplayRegression.setField(ss,f);
                    display(ss);
                    display("\t");
                }
        }

        // Prints array of boolean, tab, no line return, fixed field length
        public final synchronized void printtab(boolean[] array, int f){
                int n = array.length;
                for(int i=0; i<n; i++){
                    String ss ="";
                    ss = ss + array[i];
                    ss = DisplayRegression.setField(ss,f);
                    display(ss);
                    display("\t");
                }
        }

        // Prints array of Strings, tab, no line return, fixed field length
        public final synchronized void printtab(String[] array, int f){
                int n = array.length;
                for(int i=0; i<n; i++){
                    String ss ="";
                    ss = ss + array[i];
                    ss = DisplayRegression.setField(ss,f);
                    display(ss);
                    display("\t");
                }
        }

        // Prints array of Complex, tab, no line return, fixed field length
        public final synchronized void printtab(Complex[] array, int f){
                int n = array.length;
                for(int i=0; i<n; i++){
                    String ss ="";
                    ss = ss + array[i];
                    ss = DisplayRegression.setField(ss,f);
                    display(ss);
                    display("\t");
                }
        }

        
        // Prints array of ErrorProp, tab, no line return, fixed field length
        public final synchronized void printtab(ErrorProp[] array, int f){
                int n = array.length;
                for(int i=0; i<n; i++){
                    String ss ="";
                    ss = ss + array[i];
                    ss = DisplayRegression.setField(ss,f);
                    display(ss);
                    display("\t");
                }
        }

        // Prints array of ComplexErrorProp, tab, no line return, fixed field length
        public final synchronized void printtab(ComplexErrorProp[] array, int f){
                int n = array.length;
                for(int i=0; i<n; i++){
                    String ss ="";
                    ss = ss + array[i];
                    ss = DisplayRegression.setField(ss,f);
                    display(ss);
                    display("\t");
                }
        }

        // Prints array of doubles, tab, no line return
        public final synchronized void printtab(double[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display("\t");
                }
        }

        // Prints array of floats, tab, no line return
        public final synchronized void printtab(float[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display("\t");
                }
        }

        // Prints array of BigDecimal, tab, no line return
        public final synchronized void printtab(BigDecimal[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i].toString());
                    display("\t");
                }
        }

        // Prints array of BigInteger, tab, no line return
        public final synchronized void printtab(BigInteger[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i].toString());
                    display("\t");
                }
        }

        // Prints array of long, tab, no line return
        public final synchronized void printtab(long[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display("\t");
                }
        }

        // Prints array of int, tab, no line return
        public final synchronized void printtab(int[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display("\t");
                }
        }

        // Prints array of char, tab, no line return
        public final synchronized void printtab(char[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display("\t");
                }
        }

        // Prints array of boolean, tab, no line return
        public final synchronized void printtab(boolean[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display("\t");
                }
        }

        // Prints array of Strings, tab, no line return
        public final synchronized void printtab(String[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display("\t");
                }
        }


        // Prints date and time (plus tab, no line return);
        public final synchronized void dateAndTimetab(){
                Date d = new Date();
                String day = DateFormat.getDateInstance().format(d);
                String tim = DateFormat.getTimeInstance().format(d);

                display("This file was created at ");
                display(tim);
                display(" on ");
                display(day);
                display("\t");
        }

        // Prints file title (title), date and time (plus tab, no line return);
        public final synchronized void dateAndTimetab(String title){
                Date d = new Date();
                String day = DateFormat.getDateInstance().format(d);
                String tim = DateFormat.getTimeInstance().format(d);

                display("This file, "+title+", was created at ");
                display(tim);
                display(" on ");
                display(day);
                display("\t");
        }

        // PRINT FOLLOWED BY A COMMA, NO LINE RETURN
        // Prints character plus comma, no line return
        public final synchronized void printcomma(char ch){
                display(ch);
                display(",");
        }

        // Prints string plus comma, no line return
        public final synchronized void printcomma(String word){
                display(word + ",");
        }

        // Prints double plus comma, no line return
        public final synchronized void printcomma(double dd){
                display(dd);
                display(",");
        }

        // Prints float plus comma, no line return
        public final synchronized void printcomma(float ff){
                display(ff);
                display(",");
        }

        // Prints BigDecimal plus comma, no line return
        public final synchronized void printcomma(BigDecimal big){
                display(big.toString());
                display(",");
        }

        // Prints BigInteger plus comma, no line return
        public final synchronized void printcomma(BigInteger big){
                display(big.toString());
                display(",");
        }

        // Prints Complex plus comma, no line return
        public final synchronized void printcomma(Complex ff){
                display(ff.toString());
                display(",");
        }


        // Prints ErrorProp plus comma, no line return
        public final synchronized void printcomma(ErrorProp ff){
                display(ff.toString());
                display(",");
        }

        // Prints ComplexErrorProp plus comma, no line return
        public final synchronized void printcomma(ComplexErrorProp ff){
                display(ff.toString());
                display(",");
        }

        // Prints int plus comma, no line return
        public final synchronized void printcomma(int ii){
                display(ii);
                display(",");
        }

        // Prints long integer plus comma, no line return
        public final synchronized void printcomma(long ll){
                display(ll);
                display(",");
        }

        // Prints boolean plus comma, no line return
        public final synchronized void printcomma(boolean bb){
                display(bb);
                display(",");
        }

        // Prints short integer plus comma, no line return
        public final synchronized void printcomma(short ss){
                display(ss);
                display(",");
        }

        // Prints byte integer plus comma, no line return
        public final synchronized void printcomma(byte by){
                display(by);
                display(",");
        }

        // Prints comma, no line return
        public final synchronized void printcomma(){
                display(",");
        }

                // Prints array of doubles, each separated by a comma
        public final synchronized void printcomma(double[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display(",");
                }
        }

        // Prints array of floats, each separated by a comma
        public final synchronized void printcomma(float[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display(",");
                }
        }

        // Prints array of BigDecimal, each separated by a comma
        public final synchronized void printcomma(BigDecimal[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i].toString());
                    display(",");
                }
        }

        // Prints array of BigInteger, each separated by a comma
        public final synchronized void printcomma(BigInteger[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i].toString());
                    display(",");
                }
        }

        // Prints array of long, each separated by a comma
        public final synchronized void printcomma(long[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display(",");
                }
        }

        // Prints array of int, each separated by a comma
        public final synchronized void printcomma(int[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display(",");
                }
        }

        // Prints array of short, each separated by a comma
        public final synchronized void printcomma(short[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display(",");
                }
        }

        // Prints array of byte, each separated by a comma
        public final synchronized void printcomma(byte[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display(",");
                }
        }

        // Prints array of char, each separated by a comma
        public final synchronized void printcomma(char[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display(",");
                }
        }

        // Prints array of boolean, each separated by a comma
        public final synchronized void printcomma(boolean[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display(",");
                }
        }

        // Prints array of Strings, each separated by a comma
        public final synchronized void printcomma(String[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display(",");
                }
        }

        // Prints date and time (plus comma, no line return);
        public final synchronized void dateAndTimecomma(){
                Date d = new Date();
                String day = DateFormat.getDateInstance().format(d);
                String tim = DateFormat.getTimeInstance().format(d);

                display("This file was created at ");
                display(tim);
                display(" on ");
                display(day);
                display(",");
        }

        // Prints file title (title), date and time (plus comma, no line return);
        public final synchronized void dateAndTimecomma(String title){
                Date d = new Date();
                String day = DateFormat.getDateInstance().format(d);
                String tim = DateFormat.getTimeInstance().format(d);

                display("This file, "+title+", was created at ");
                display(tim);
                display(" on ");
                display(day);
                display(",");
        }

        // PRINT FOLLOWED BY A SEMICOLON, NO LINE RETURN
        // Prints character plus semicolon, no line return
        public final synchronized void printsc(char ch){
                display(ch);
                display(";");
        }

        // Prints string plus semicolon, no line return
        public final synchronized void printsc(String word){
                display(word + ";");
        }

        // Prints double plus semicolon, no line return
        public final synchronized void printsc(double dd){
                display(dd);
                display(";");
        }

        // Prints float plus semicolon, no line return
        public final synchronized void printsc(float ff){
                display(ff);
                display(";");
        }

        // Prints BigDecimal plus semicolon, no line return
        public final synchronized void printsc(BigDecimal big){
                display(big.toString());
                display(";");
        }

        // Prints BigInteger plus semicolon, no line return
        public final synchronized void printsc(BigInteger big){
                display(big.toString());
                display(";");
        }

        // Prints Complex plus semicolon, no line return
        public final synchronized void printsc(Complex ff){
                display(ff.toString());
                display(";");
        }

        // Prints ErrorProp plus semicolon, no line return
        public final synchronized void printsc(ErrorProp ff){
                display(ff.toString());
                display(";");
        }

        // Prints ComplexErrorProp plus semicolon, no line return
        public final synchronized void printsc(ComplexErrorProp ff){
                display(ff.toString());
                display(";");
        }

        // Prints int plus semicolon, no line return
        public final synchronized void printsc(int ii){
                display(ii);
                display(";");
        }

        // Prints long integer plus semicolon, no line return
        public final synchronized void printsc(long ll){
                display(ll);
                display(";");
        }

        // Prints short integer plus semicolon, no line return
        public final synchronized void printsc(short ss){
                display(ss);
                display(";");
        }

        // Prints byte integer plus semicolon, no line return
        public final synchronized void printsc(byte by){
                display(by);
                display(";");
        }

        // Prints boolean plus semicolon, no line return
        public final synchronized void printsc(boolean bb){
                display(bb);
                display(";");
        }

        // Prints  semicolon, no line return
        public final synchronized void printsc(){
                display(";");
        }

        // Prints array of doubles, each separated by a semicolon
        public final synchronized void printsc(double[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display(";");
                }
        }

        // Prints array of floats, each separated by a semicolon
        public final synchronized void printsc(float[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display(";");
                }
        }

        // Prints array of BigDecimal, each separated by a semicolon
        public final synchronized void printsc(BigDecimal[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i].toString());
                    display(";");
                }
        }

        // Prints array of BigInteger, each separated by a semicolon
        public final synchronized void printsc(BigInteger[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i].toString());
                    display(";");
                }
        }

        // Prints array of long, each separated by a semicolon
        public final synchronized void printsc(long[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display(";");
                }
        }

        // Prints array of short, each separated by a semicolon
        public final synchronized void printsc(short[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display(";");
                }
        }

        // Prints array of byte, each separated by a semicolon
        public final synchronized void printsc(byte[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display(";");
                }
        }

        // Prints array of int, each separated by a semicolon
        public final synchronized void printsc(int[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display(";");
                }
        }

        // Prints array of char, each separated by a semicolon
        public final synchronized void printsc(char[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display(";");
                }
        }

        // Prints array of boolean, each separated by a semicolon
        public final synchronized void printsc(boolean[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display(";");
                }
        }

        // Prints array of Strings, each separated by a semicolon
        public final synchronized void printsc(String[] array){
                int n = array.length;
                for(int i=0; i<n; i++){
                    display(array[i]);
                    display(";");
                }
        }

        // Prints date and time (plus semicolon, no line return);
        public final synchronized void dateAndTimesc(){
                Date d = new Date();
                String day = DateFormat.getDateInstance().format(d);
                String tim = DateFormat.getTimeInstance().format(d);

                display("This file was created at ");
                display(tim);
                display(" on ");
                display(day);
                display(";");
        }

        // Prints file title (title), date and time (plus semicolon, no line return);
        public final synchronized void dateAndTimesc(String title){
                Date d = new Date();
                String day = DateFormat.getDateInstance().format(d);
                String tim = DateFormat.getTimeInstance().format(d);

                display("This file, "+title+", was created at ");
                display(tim);
                display(" on ");
                display(day);
                display(";");
        }


        // Print a 2-D array of doubles to a text file, no file title provided
        public static void printArrayToText(double[][] array){
            String title = "ArrayToText.txt";
            printArrayToText(title, array);
        }


        // Print a 2-D array of doubles to a text file, file title provided
        public static void printArrayToText(String title, double[][] array){
            FileOutput fo = new FileOutput(title, 'n');
            fo.dateAndTimeln(title);
            int nrow = array.length;
            int ncol = 0;
            for(int i=0; i<nrow; i++){
                ncol=array[i].length;
                for(int j=0; j<ncol; j++){
                    fo.printtab(array[i][j]);
                }
                fo.println();
            }
            fo.println("End of file.");
            fo.close();
        }

        // Print a 1-D array of doubles to a text file, no file title provided
        public static void printArrayToText(double[] array){
            String title = "ArrayToText.txt";
            printArrayToText(title, array);
        }


        // Print a 1-D array of doubles to a text file, file title provided
        public static void printArrayToText(String title, double[] array){
            FileOutput fo = new FileOutput(title, 'n');
            fo.dateAndTimeln(title);
            int nrow = array.length;
            for(int i=0; i<nrow; i++){
                fo.printtab(array[i]);
            }
            fo.println();
            fo.println("End of file.");
            fo.close();
        }

        // Print a 2-D array of floats to a text file, no file title provided
        public static void printArrayToText(float[][] array){
            String title = "ArrayToText.txt";
            printArrayToText(title, array);
        }


        // Print a 2-D array of floats to a text file, file title provided
        public static void printArrayToText(String title, float[][] array){
            FileOutput fo = new FileOutput(title, 'n');
            fo.dateAndTimeln(title);
            int nrow = array.length;
            int ncol = 0;
            for(int i=0; i<nrow; i++){
                ncol=array[i].length;
                for(int j=0; j<ncol; j++){
                    fo.printtab(array[i][j]);
                }
                fo.println();
            }
            fo.println("End of file.");
            fo.close();
        }


        // Print a 1-D array of floats to a text file, no file title provided
        public static void printArrayToText(float[] array){
            String title = "ArrayToText.txt";
            printArrayToText(title, array);
        }


        // Print a 1-D array of float to a text file, file title provided
        public static void printArrayToText(String title, float[] array){
            FileOutput fo = new FileOutput(title, 'n');
            fo.dateAndTimeln(title);
            int nrow = array.length;
            for(int i=0; i<nrow; i++){
                fo.printtab(array[i]);
            }
            fo.println();
            fo.println("End of file.");
            fo.close();
        }

        // Print a 2-D array of BigDecimal to a text file, no file title provided
        public static void printArrayToText(BigDecimal[][] array){
            String title = "ArrayToText.txt";
            printArrayToText(title, array);
        }


        // Print a 2-D array of BigDecimal to a text file, file title provided
        public static void printArrayToText(String title, BigDecimal[][] array){
            FileOutput fo = new FileOutput(title, 'n');
            fo.dateAndTimeln(title);
            int nrow = array.length;
            int ncol = 0;
            for(int i=0; i<nrow; i++){
                ncol=array[i].length;
                for(int j=0; j<ncol; j++){
                    fo.printtab(array[i][j].toString());
                }
                fo.println();
            }
            fo.println("End of file.");
            fo.close();
        }

        // Print a 2-D array of BigInteger to a text file, no file title provided
        public static void printArrayToText(BigInteger[][] array){
            String title = "ArrayToText.txt";
            printArrayToText(title, array);
        }

        // Print a 2-D array of BigInteger to a text file, file title provided
        public static void printArrayToText(String title, BigInteger[][] array){
            FileOutput fo = new FileOutput(title, 'n');
            fo.dateAndTimeln(title);
            int nrow = array.length;
            int ncol = 0;
            for(int i=0; i<nrow; i++){
                ncol=array[i].length;
                for(int j=0; j<ncol; j++){
                    fo.printtab(array[i][j].toString());
                }
                fo.println();
            }
            fo.println("End of file.");
            fo.close();
        }


        // Print a 1-D array of BigDecimal to a text file, no file title provided
        public static void printArrayToText(BigDecimal[] array){
            String title = "ArrayToText.txt";
            printArrayToText(title, array);
        }


        // Print a 1-D array of BigDecimal to a text file, file title provided
        public static void printArrayToText(String title, BigDecimal[] array){
            FileOutput fo = new FileOutput(title, 'n');
            fo.dateAndTimeln(title);
            int nrow = array.length;
            for(int i=0; i<nrow; i++){
                fo.printtab(array[i].toString());
            }
            fo.println();
            fo.println("End of file.");
            fo.close();
        }

        // Print a 1-D array of BigInteger to a text file, no file title provided
        public static void printArrayToText(BigInteger[] array){
            String title = "ArrayToText.txt";
            printArrayToText(title, array);
        }


        // Print a 1-D array of BigInteger to a text file, file title provided
        public static void printArrayToText(String title, BigInteger[] array){
            FileOutput fo = new FileOutput(title, 'n');
            fo.dateAndTimeln(title);
            int nrow = array.length;
            for(int i=0; i<nrow; i++){
                fo.printtab(array[i].toString());
            }
            fo.println();
            fo.println("End of file.");
            fo.close();
        }

        // Print a 2-D array of ints to a text file, no file title provided
        public static void printArrayToText(int[][] array){
            String title = "ArrayToText.txt";
            printArrayToText(title, array);
        }


        // Print a 2-D array of ints to a text file, file title provided
        public static void printArrayToText(String title, int[][] array){
            FileOutput fo = new FileOutput(title, 'n');
            fo.dateAndTimeln(title);
            int nrow = array.length;
            int ncol = 0;
            for(int i=0; i<nrow; i++){
                ncol=array[i].length;
                for(int j=0; j<ncol; j++){
                    fo.printtab(array[i][j]);
                }
                fo.println();
            }
            fo.println("End of file.");
            fo.close();
        }


        // Print a 1-D array of ints to a text file, no file title provided
        public static void printArrayToText(int[] array){
            String title = "ArrayToText.txt";
            printArrayToText(title, array);
        }


        // Print a 1-D array of int to a text file, file title provided
        public static void printArrayToText(String title, int[] array){
            FileOutput fo = new FileOutput(title, 'n');
            fo.dateAndTimeln(title);
            int nrow = array.length;
            for(int i=0; i<nrow; i++){
                fo.printtab(array[i]);
            }
            fo.println();
            fo.println("End of file.");
            fo.close();
        }

        // Print a 2-D array of longs to a text file, no file title provided
        public static void printArrayToText(long[][] array){
            String title = "ArrayToText.txt";
            printArrayToText(title, array);
        }


        // Print a 2-D array of longs to a text file, file title provided
        public static void printArrayToText(String title, long[][] array){
            FileOutput fo = new FileOutput(title, 'n');
            fo.dateAndTimeln(title);
            int nrow = array.length;
            int ncol = 0;
            for(int i=0; i<nrow; i++){
                ncol=array[i].length;
                for(int j=0; j<ncol; j++){
                    fo.printtab(array[i][j]);
                }
                fo.println();
            }
            fo.println("End of file.");
            fo.close();
        }




        // Print a 1-D array of longs to a text file, no file title provided
        public static void printArrayToText(long[] array){
            String title = "ArrayToText.txt";
            printArrayToText(title, array);
        }


        // Print a 1-D array of long to a text file, file title provided
        public static void printArrayToText(String title, long[] array){
            FileOutput fo = new FileOutput(title, 'n');
            fo.dateAndTimeln(title);
            int nrow = array.length;
            for(int i=0; i<nrow; i++){
                fo.printtab(array[i]);
            }
            fo.println();
            fo.println("End of file.");
            fo.close();
        }

        // Print a 2-D array of shorts to a text file, no file title provided
        public static void printArrayToText(short[][] array){
            String title = "ArrayToText.txt";
            printArrayToText(title, array);
        }


        // Print a 2-D array of shorts to a text file, file title provided
        public static void printArrayToText(String title, short[][] array){
            FileOutput fo = new FileOutput(title, 'n');
            fo.dateAndTimeln(title);
            int nrow = array.length;
            int ncol = 0;
            for(int i=0; i<nrow; i++){
                ncol=array[i].length;
                for(int j=0; j<ncol; j++){
                    fo.printtab(array[i][j]);
                }
                fo.println();
            }
            fo.println("End of file.");
            fo.close();
        }

        // Print a 1-D array of shorts to a text file, no file title provided
        public static void printArrayToText(short[] array){
            String title = "ArrayToText.txt";
            printArrayToText(title, array);
        }


        // Print a 1-D array of short to a text file, file title provided
        public static void printArrayToText(String title, short[] array){
            FileOutput fo = new FileOutput(title, 'n');
            fo.dateAndTimeln(title);
            int nrow = array.length;
            for(int i=0; i<nrow; i++){
                fo.printtab(array[i]);
            }
            fo.println();
            fo.println("End of file.");
            fo.close();
        }


        // Print a 2-D array of bytes to a text file, no file title provided
        public static void printArrayToText(byte[][] array){
            String title = "ArrayToText.txt";
            printArrayToText(title, array);
        }


        // Print a 2-D array of bytes to a text file, file title provided
        public static void printArrayToText(String title, byte[][] array){
            FileOutput fo = new FileOutput(title, 'n');
            fo.dateAndTimeln(title);
            int nrow = array.length;
            int ncol = 0;
            for(int i=0; i<nrow; i++){
                ncol=array[i].length;
                for(int j=0; j<ncol; j++){
                    fo.printtab(array[i][j]);
                }
                fo.println();
            }
            fo.println("End of file.");
            fo.close();
        }


        // Print a 1-D array of bytes to a text file, no file title provided
        public static void printArrayToText(byte[] array){
            String title = "ArrayToText.txt";
            printArrayToText(title, array);
        }


        // Print a 1-D array of byte to a text file, file title provided
        public static void printArrayToText(String title, byte[] array){
            FileOutput fo = new FileOutput(title, 'n');
            fo.dateAndTimeln(title);
            int nrow = array.length;
            for(int i=0; i<nrow; i++){
                fo.printtab(array[i]);
            }
            fo.println();
            fo.println("End of file.");
            fo.close();
        }


        // Print a 2-D array of Strings to a text file, no file title provided
        public static void printArrayToText(String[][] array){
            String title = "ArrayToText.txt";
            printArrayToText(title, array);
        }


        // Print a 2-D array of Strings to a text file, file title provided
        public static void printArrayToText(String title, String[][] array){
            FileOutput fo = new FileOutput(title, 'n');
            fo.dateAndTimeln(title);
            int nrow = array.length;
            int ncol = 0;
            for(int i=0; i<nrow; i++){
                ncol=array[i].length;
                for(int j=0; j<ncol; j++){
                    fo.printtab(array[i][j]);
                }
                fo.println();
            }
            fo.println("End of file.");
            fo.close();
        }


        // Print a 1-D array of Strings to a text file, no file title provided
        public static void printArrayToText(String[] array){
            String title = "ArrayToText.txt";
            printArrayToText(title, array);
        }


        // Print a 1-D array of String to a text file, file title provided
        public static void printArrayToText(String title, String[] array){
            FileOutput fo = new FileOutput(title, 'n');
            fo.dateAndTimeln(title);
            int nrow = array.length;
            for(int i=0; i<nrow; i++){
                fo.printtab(array[i]);
            }
            fo.println();
            fo.println("End of file.");
            fo.close();
        }
         // Print a 2-D array of chars to a text file, no file title provided
        public static void printArrayToText(char[][] array){
            String title = "ArrayToText.txt";
            printArrayToText(title, array);
        }


        // Print a 2-D array of chars to a text file, file title provided
        public static void printArrayToText(String title, char[][] array){
            FileOutput fo = new FileOutput(title, 'n');
            fo.dateAndTimeln(title);
            int nrow = array.length;
            int ncol = 0;
            for(int i=0; i<nrow; i++){
                ncol=array[i].length;
                for(int j=0; j<ncol; j++){
                    fo.printtab(array[i][j]);
                }
                fo.println();
            }
            fo.println("End of file.");
            fo.close();
        }


        // Print a 1-D array of chars to a text file, no file title provided
        public static void printArrayToText(char[] array){
            String title = "ArrayToText.txt";
            printArrayToText(title, array);
        }


        // Print a 1-D array of char to a text file, file title provided
        public static void printArrayToText(String title, char[] array){
            FileOutput fo = new FileOutput(title, 'n');
            fo.dateAndTimeln(title);
            int nrow = array.length;
            for(int i=0; i<nrow; i++){
                fo.printtab(array[i]);
            }
            fo.println();
            fo.println("End of file.");
            fo.close();
        }
        // Print a 2-D array of booleans to a text file, no file title provided
        public static void printArrayToText(boolean[][] array){
            String title = "ArrayToText.txt";
            printArrayToText(title, array);
        }


        // Print a 2-D array of booleans to a text file, file title provided
        public static void printArrayToText(String title, boolean[][] array){
            FileOutput fo = new FileOutput(title, 'n');
            fo.dateAndTimeln(title);
            int nrow = array.length;
            int ncol = 0;
            for(int i=0; i<nrow; i++){
                ncol=array[i].length;
                for(int j=0; j<ncol; j++){
                    fo.printtab(array[i][j]);
                }
                fo.println();
            }
            fo.println("End of file.");
            fo.close();
        }


        // Print a 1-D array of booleans to a text file, no file title provided
        public static void printArrayToText(boolean[] array){
            String title = "ArrayToText.txt";
            printArrayToText(title, array);
        }


        // Print a 1-D array of boolean to a text file, file title provided
        public static void printArrayToText(String title, boolean[] array){
            FileOutput fo = new FileOutput(title, 'n');
            fo.dateAndTimeln(title);
            int nrow = array.length;
            for(int i=0; i<nrow; i++){
                fo.printtab(array[i]);
            }
            fo.println();
            fo.println("End of file.");
            fo.close();
        }

        // Print a 2-D array of Complex to a text file, no file title provided
        public static void printArrayToText(Complex[][] array){
            String title = "ArrayToText.txt";
            printArrayToText(title, array);
        }

        // Print a 2-D array of Complex to a text file, file title provided
        public static void printArrayToText(String title, Complex[][] array){
            FileOutput fo = new FileOutput(title, 'n');
            fo.dateAndTimeln(title);
            int nrow = array.length;
            int ncol = 0;
            for(int i=0; i<nrow; i++){
                ncol=array[i].length;
                for(int j=0; j<ncol; j++){
                    fo.printtab(array[i][j]);
                }
                fo.println();
            }
            fo.println("End of file.");
            fo.close();
        }


        // Print a 1-D array of Complex to a text file, no file title provided
        public static void printArrayToText(Complex[] array){
            String title = "ArrayToText.txt";
            printArrayToText(title, array);
        }


        // Print a 1-D array of Complex to a text file, file title provided
        public static void printArrayToText(String title, Complex[] array){
            FileOutput fo = new FileOutput(title, 'n');
            fo.dateAndTimeln(title);
            int nrow = array.length;
            for(int i=0; i<nrow; i++){
                fo.printtab(array[i]);
            }
            fo.println();
            fo.println("End of file.");
            fo.close();
        }


        // Print a 2-D array of ErrorProp to a text file, no file title provided
        public static void printArrayToText(ErrorProp[][] array){
            String title = "ArrayToText.txt";
            printArrayToText(title, array);
        }


        // Print a 2-D array of ErrorProp to a text file, file title provided
        public static void printArrayToText(String title, ErrorProp[][] array){
            FileOutput fo = new FileOutput(title, 'n');
            fo.dateAndTimeln(title);
            int nrow = array.length;
            int ncol = 0;
            for(int i=0; i<nrow; i++){
                ncol=array[i].length;
                for(int j=0; j<ncol; j++){
                    fo.printtab(array[i][j]);
                }
                fo.println();
            }
            fo.println("End of file.");
            fo.close();
        }


        // Print a 1-D array of ErrorProp to a text file, no file title provided
        public static void printArrayToText(ErrorProp[] array){
            String title = "ArrayToText.txt";
            printArrayToText(title, array);
        }


        // Print a 1-D array of ErrorProp to a text file, file title provided
        public static void printArrayToText(String title, ErrorProp[] array){
            FileOutput fo = new FileOutput(title, 'n');
            fo.dateAndTimeln(title);
            int nrow = array.length;
            for(int i=0; i<nrow; i++){
                fo.printtab(array[i]);
            }
            fo.println();
            fo.println("End of file.");
            fo.close();

        }

        // Print a 2-D array of ComplexErrorProp to a text file, no file title provided
        public static void printArrayToText(ComplexErrorProp[][] array){
            String title = "ArrayToText.txt";
            printArrayToText(title, array);
        }


        // Print a 2-D array of ComplexErrorProp to a text file, file title provided
        public static void printArrayToText(String title, ComplexErrorProp[][] array){
            FileOutput fo = new FileOutput(title, 'n');
            fo.dateAndTimeln(title);
            int nrow = array.length;
            int ncol = 0;
            for(int i=0; i<nrow; i++){
                ncol=array[i].length;
                for(int j=0; j<ncol; j++){
                    fo.printtab(array[i][j]);
                }
                fo.println();
            }
            fo.println("End of file.");
            fo.close();
        }


        // Print a 1-D array of ComplexErrorProp to a text file, no file title provided
        public static void printArrayToText(ComplexErrorProp[] array){
            String title = "ArrayToText.txt";
            printArrayToText(title, array);
        }


        // Print a 1-D array of ComplexErrorProp to a text file, file title provided
        public static void printArrayToText(String title, ComplexErrorProp[] array){
            FileOutput fo = new FileOutput(title, 'n');
            fo.dateAndTimeln(title);
            int nrow = array.length;
            for(int i=0; i<nrow; i++){
                fo.printtab(array[i]);
            }
            fo.println();
            fo.println("End of file.");
            fo.close();
        }

        private static String setField(String ss, int f){
             char sp =  ' ';
                int n = ss.length();
                if(f>n){
                    for(int i=n+1; i<=f; i++){
                        ss=ss+sp;
                    }
                }
                return ss;
        }
}
