/*
 *   Class   Db
 *
 *   Methods for entering doubles, floats, integers,
 *   long integers, strings, chars, Complexes and Phasors
 *   from the key board via the standard console window
 *
 */

package program.stats;

import java.io.*;
import java.math.*;
import javax.swing.JOptionPane;


public class Db
{
        // Reads a double from a dialog box with a prompt message
        // No default option
        public static final synchronized double readDouble(String mess){
                String line="";
                double d=0.0D;
                boolean finish = false;
                System.out.flush();
                String mess0 = "Input type: double\n";

                while(!finish){
                        line = JOptionPane.showInputDialog(mess0+mess);
                        if(line!=null){
                            try{
                                d = Double.parseDouble(line.trim());
                                finish=true;
                            }catch(NumberFormatException e){
                                // Valid double not entered - dialog box recalled
                            }
                        }
                }
                return d;
        }

        // Reads a double from a dialog box with a prompt message and the return
        // of a default option if the return key alone is pressed
        public static final synchronized double readDouble(String mess, double dflt){
                String line="";
                double d=0.0D;
                boolean finish = false;
                System.out.flush();
                String mess0 = "Input type: double\n";
                mess = mess + "\n";
                String dfltmess = dflt + "";

                while(!finish){
                        line = JOptionPane.showInputDialog(mess0 + mess + " [default value = " + dflt + "] ", dfltmess);

                        if(line!=null){
                            if(line.equals("")){
                                d=dflt;
                                finish=true;
                                line=null;
                            }
                            else{
                                try{
                                    d = Double.parseDouble(line.trim());
                                    finish=true;
                                }catch(NumberFormatException e){
                                    // Valid double not entered - dialog box recalled
                                }
                            }
                        }
                }
                return d;
        }

        // Reads a double from the dialog box
        // No prompt message, No default option
        public static final synchronized double readDouble(){
                String line="";
                String mess="Input type: double";
                double d=0.0D;
                boolean finish = false;
                System.out.flush();

                while(!finish){
                        line = JOptionPane.showInputDialog(mess);
                        if(line!=null){
                            try{
                                d = Double.parseDouble(line.trim());
                                finish=true;
                            }catch(NumberFormatException e){
                                // Valid double not entered - dialog box recalled
                            }
                        }
                }
                return d;
        }

        // Read a Complex number from dialog box with a prompt message
        // in a String format compatible with Complex.parse,
        // e.g 2+j3, 2 + j3, 2+i3, 2 + i3
        // No default option
        public static final synchronized Complex readComplex(String mess){
                String line="";
                Complex c = new Complex();
                boolean finish = false;
                String mess0 = "Input type: Complex (x + jy)\n";

                System.out.flush();

                while(!finish){
                        line = JOptionPane.showInputDialog(mess0+mess);
                        if(line!=null){
                            try{
                                c = Complex.parseComplex(line);
                                finish=true;
                            }catch(NumberFormatException e){
                                // Valid double not entered - dialog box recalled
                            }
                        }
                }
                return c;
        }

      // Reads a Complex from a dialog box with a prompt message and the return
        // of a default option if the return key alone is pressed - Complex default
        public static final synchronized Complex readComplex(String mess, Complex dflt){
                String line="";
                Complex c = new Complex();
                boolean finish = false;
                String mess0 = "Input type: Complex (x + jy)\n";
                String dfltmess = dflt+"";
                mess = mess + "\n";

                System.out.flush();

                while(!finish){
                        line = JOptionPane.showInputDialog(mess0 + mess + " [default value = " + dflt + "] ", dfltmess);

                        if(line!=null){
                            if(line.equals("")){
                                c = dflt;
                                finish=true;
                                line=null;
                            }
                            else{
                                try{
                                    c = Complex.parseComplex(line);
                                    finish=true;
                                }catch(NumberFormatException e){
                                    // Valid double not entered - dialog box recalled
                                }
                            }
                        }
                }
                return c;
        }

        // Reads a Complex from a dialog box with a prompt message and the return
        // of a default option if the return key alone is pressed - String default
        public static final synchronized Complex readComplex(String mess, String dflt){
                String line="";
                Complex c = new Complex();
                boolean finish = false;
                String mess0 = "Input type: Complex (x + jy)\n";
                String dfltmess = dflt;
                mess = mess + "\n";

                System.out.flush();


                while(!finish){
                        line = JOptionPane.showInputDialog(mess0 + mess + " [default value = " + dflt + "] ", dfltmess);

                        if(line!=null){
                            if(line.equals("")){
                                c = Complex.parseComplex(dflt);
                                finish=true;
                                line=null;
                            }
                            else{
                                try{
                                    c = Complex.parseComplex(line);
                                    finish=true;
                                }catch(NumberFormatException e){
                                    // Valid double not entered - dialog box recalled
                                }
                            }
                        }
                }
                return c;
        }

        // Reads a Complex from the dialog box
        // No prompt message, No default option
        public static final synchronized Complex readComplex(){
                String line="";
                String mess="Input type: Complex (x + jy)";
                Complex c = new Complex();
                boolean finish = false;
                System.out.flush();

                while(!finish){
                        line = JOptionPane.showInputDialog(mess);
                        if(line!=null){
                            try{
                                c = Complex.parseComplex(line.trim());
                                finish=true;
                            }catch(NumberFormatException e){
                                // Valid double not entered - dialog box recalled
                            }
                        }
                }
                return c;
        }




        // Reads a float from a dialog box with a prompt message
        // No default option
        public static final synchronized float readFloat(String mess){
                String line="";
                float d=0.0F;
                boolean finish = false;
                System.out.flush();
                String mess0 = "Input type: float\n";

                while(!finish){
                        line = JOptionPane.showInputDialog(mess0+mess);
                        if(line!=null){
                            try{
                                d = Float.parseFloat(line.trim());
                                finish=true;
                            }catch(NumberFormatException e){
                                // Valid float not entered - dialog box recalled
                            }
                        }
                }
                return d;
        }

        // Reads a float from a dialog box with a prompt message and the return
        // of a default option if the return key alone is pressed
        public static final synchronized float readFloat(String mess, float dflt){
                String line="";
                float d=0.0F;
                boolean finish = false;
                System.out.flush();
                String mess0 = "Input type: float\n";
                mess = mess +"\n";
                String dfltmess = dflt + "";

                while(!finish){
                        line = JOptionPane.showInputDialog(mess0 + mess + " [default value = " + dflt + "] ", dfltmess);

                        if(line!=null){
                            if(line.equals("")){
                                d=dflt;
                                finish=true;
                                line=null;
                            }
                            else{
                                try{
                                    d = Float.parseFloat(line.trim());
                                    finish=true;
                                }catch(NumberFormatException e){
                                    // Valid float not entered - dialog box recalled
                                }
                            }
                        }
                }
                return d;
        }

        // Reads a float from the dialog box
        // No prompt message, No default option
        public static final synchronized float readFloat(){
                String line="";
                String mess="Input type: float";
                float d=0.0F;
                boolean finish = false;
                System.out.flush();

                while(!finish){
                        line = JOptionPane.showInputDialog(mess);
                        if(line!=null){
                            try{
                                d = Float.parseFloat(line.trim());
                                finish=true;
                            }catch(NumberFormatException e){
                                // Valid float not entered - dialog box recalled
                            }
                        }
                }
                return d;
        }



        // Reads a int from a dialog box with a prompt message
        // No default option
        public static final synchronized int readInt(String mess){
                String line="";
                int d=0;
                boolean finish = false;
                System.out.flush();
                String mess0 = "Input type: int\n";

                while(!finish){
                        line = JOptionPane.showInputDialog(mess0+mess);
                        if(line!=null){
                            try{
                                d = Integer.parseInt(line.trim());
                                finish=true;
                            }catch(NumberFormatException e){
                                // Valid int not entered - dialog box recalled
                            }
                        }
                }
                return d;
        }

        // Reads a int from a dialog box with a prompt message and the return
        // of a default option if the return key alone is pressed
        public static final synchronized int readInt(String mess, int dflt){
                String line="";
                int d=0;
                boolean finish = false;
                String mess0 = "Input type: int\n";
                mess = mess +"\n";
                String dfltmess = dflt + "";

                System.out.flush();

                while(!finish){
                        line = JOptionPane.showInputDialog(mess0+mess + " [default value = " + dflt + "] ",dfltmess);

                        if(line!=null){
                            if(line.equals("")){
                                d=dflt;
                                finish=true;
                                line=null;
                            }
                            else{
                                try{
                                    d = Integer.parseInt(line.trim());
                                    finish=true;
                                }catch(NumberFormatException e){
                                    // Valid int not entered - dialog box recalled
                                }
                            }
                        }
                }
                return d;
        }

        // Reads a int from the dialog box
        // No prompt message, No default option
        public static final synchronized int readInt(){
                String line="";
                String mess="Input type: int";
                int d=0;
                boolean finish = false;
                System.out.flush();

                while(!finish){
                        line = JOptionPane.showInputDialog(mess);
                        if(line!=null){
                            try{
                                d = Integer.parseInt(line.trim());
                                finish=true;
                            }catch(NumberFormatException e){
                                // Valid int not entered - dialog box recalled
                           }
                        }
                }
                return d;
        }


        // Reads a long from a dialog box with a prompt message
        // No default option
        public static final synchronized long readLong(String mess){
                String line="";
                long d=0L;
                boolean finish = false;
                String mess0 = "Input type: long\n";

                System.out.flush();

                while(!finish){
                        line = JOptionPane.showInputDialog(mess0+mess);
                        if(line!=null){
                            try{
                                d = Long.parseLong(line.trim());
                                finish=true;
                            }catch(NumberFormatException e){
                                // Valid long not entered - dialog box recalled
                            }
                        }
                }
                return d;
        }

        // Reads a long from a dialog box with a prompt message and the return
        // of a default option if the return key alone is pressed
        public static final synchronized long readLong(String mess, long dflt){
                String line="";
                long d=0L;
                boolean finish = false;
                String mess0 = "Input type: long\n";
                mess = mess +"\n";
                String dfltmess = dflt + "";

                System.out.flush();

                while(!finish){
                        line = JOptionPane.showInputDialog(mess0+mess + " [default value = " + dflt + "] ", dfltmess);

                        if(line!=null){
                            if(line.equals("")){
                                d=dflt;
                                finish=true;
                                line=null;
                            }
                            else{
                                try{
                                    d = Long.parseLong(line.trim());
                                    finish=true;
                                }catch(NumberFormatException e){
                                    // Valid long not entered - dialog box recalled
                               }
                            }
                        }
                }
                return d;
        }

        // Reads a long from the dialog box
        // No prompt message, No default option
        public static final synchronized long readLong(){
                String line="";
                String mess="Input type: long";
                long d=0L;
                boolean finish = false;

                System.out.flush();

                while(!finish){
                        line = JOptionPane.showInputDialog(mess);
                        if(line!=null){
                            try{
                                d = Long.parseLong(line.trim());
                                finish=true;
                            }catch(NumberFormatException e){
                                // Valid long not entered - dialog box recalled
                            }
                        }
                }
                return d;
        }

        // Reads a short from a dialog box with a prompt message
        // No default option
        public static final synchronized long readShort(String mess){
                String line="";
                long d=0;
                boolean finish = false;
                String mess0 = "Input type: short\n";

                System.out.flush();

                while(!finish){
                        line = JOptionPane.showInputDialog(mess0+mess);
                        if(line!=null){
                            try{
                                d = Short.parseShort(line.trim());
                                finish=true;
                            }catch(NumberFormatException e){
                                // Valid short not entered - dialog box recalled
                            }
                        }
                }
                return d;
        }

        // Reads a short from a dialog box with a prompt message and the return
        // of a default option if the return key alone is pressed
        public static final synchronized short readShort(String mess, short dflt){
                String line="";
                short d=0;
                boolean finish = false;
                String mess0 = "Input type: short\n";
                mess = mess +"\n";
                String dfltmess = dflt + "";

                System.out.flush();

                while(!finish){
                        line = JOptionPane.showInputDialog(mess0+mess + " [default value = " + dflt + "] ", dfltmess);

                        if(line!=null){
                            if(line.equals("")){
                                d=dflt;
                                finish=true;
                                line=null;
                            }
                            else{
                                try{
                                    d = Short.parseShort(line.trim());
                                    finish=true;
                                }catch(NumberFormatException e){
                                    // Valid short not entered - dialog box recalled
                               }
                            }
                        }
                }
                return d;
        }

        // Reads a short from the dialog box
        // No prompt message, No default option
        public static final synchronized short readShort(){
                String line="";
                String mess="Input type: short";
                short d=0;
                boolean finish = false;

                System.out.flush();

                while(!finish){
                        line = JOptionPane.showInputDialog(mess);
                        if(line!=null){
                            try{
                                d = Short.parseShort(line.trim());
                                finish=true;
                            }catch(NumberFormatException e){
                                // Valid short not entered - dialog box recalled
                            }
                        }
                }
                return d;
        }

        // Reads a byte from a dialog box with a prompt message
        // No default option
        public static final synchronized long readByte(String mess){
                String line="";
                long d=0;
                boolean finish = false;
                String mess0 = "Input type: short\n";

                System.out.flush();

                while(!finish){
                        line = JOptionPane.showInputDialog(mess0+mess);
                        if(line!=null){
                            try{
                                d = Byte.parseByte(line.trim());
                                finish=true;
                            }catch(NumberFormatException e){
                                // Valid byte not entered - dialog box recalled
                            }
                        }
                }
                return d;
        }

        // Reads a byte from a dialog box with a prompt message and the return
        // of a default option if the return key alone is pressed
        public static final synchronized byte readByte(String mess, byte dflt){
                String line="";
                byte d=0;
                boolean finish = false;
                String mess0 = "Input type: byte\n";
                mess = mess +"\n";
                String dfltmess = dflt + "";

                System.out.flush();

                while(!finish){
                        line = JOptionPane.showInputDialog(mess0+mess + " [default value = " + dflt + "] ", dfltmess);

                        if(line!=null){
                            if(line.equals("")){
                                d=dflt;
                                finish=true;
                                line=null;
                            }
                            else{
                                try{
                                    d = Byte.parseByte(line.trim());
                                    finish=true;
                                }catch(NumberFormatException e){
                                    // Valid byte not entered - dialog box recalled
                               }
                            }
                        }
                }
                return d;
        }

        // Reads a byte from the dialog box
        // No prompt message, No default option
        public static final synchronized byte readByte(){
                String line="";
                String mess="Input type: byte";
                byte d=0;
                boolean finish = false;

                System.out.flush();

                while(!finish){
                        line = JOptionPane.showInputDialog(mess);
                        if(line!=null){
                            try{
                                d = Byte.parseByte(line.trim());
                                finish=true;
                            }catch(NumberFormatException e){
                                // Valid byte not entered - dialog box recalled
                            }
                        }
                }
                return d;
        }


        // Reads a char from a dialog box with a prompt message
        // No default option
        public static final synchronized char readChar(String mess){
                String line="";
                char d=' ';
                boolean finish = false;
                String mess0 = "Input type: char\n";

                System.out.flush();

                while(!finish){
                        line = JOptionPane.showInputDialog(mess0+mess);
                        if(line!=null){
                            if(line.equals("")){
                                // Valid char not entered - dialog box recalled
                            }
                            else{
                                d = line.charAt(0);
                                finish=true;
                            }
                        }
                }
                return d;
        }

        // Reads a char from a dialog box with a prompt message and the return
        // of a default option if the return key alone is pressed
        public static final synchronized char readChar(String mess, char dflt){
                String line="";
                char d = ' ';
                boolean finish = false;
                String mess0 = "Input type: char\n";
                mess = mess +"\n";
                String dfltmess = dflt + "";

                System.out.flush();

                while(!finish){
                        line = JOptionPane.showInputDialog(mess0+mess + " [default value = " + dflt + "] ", dfltmess);
                        if(line!=null){
                            if(line.equals("")){
                                d=dflt;
                                finish=true;
                                line=null;
                            }
                            else{
                                d = line.charAt(0);
                                finish=true;
                            }
                        }
                }
                return d;
        }

        // Reads a char from the dialog box
        // No prompt message, No default option
        public static final synchronized char readChar(){
                String line="";
                String mess="Input type: char";
                char d=' ';
                boolean finish = false;
                System.out.flush();

                while(!finish){
                        line = JOptionPane.showInputDialog(mess);
                        if(line!=null){
                            if(line.equals("")){
                               // Valid char not entered - dialog box recalled
                            }
                            else{
                                d = line.charAt(0);
                                finish=true;
                            }
                        }
                }
                return d;
        }




        // Reads a line from a dialog box with a prompt message
        // No default option
        public static final synchronized String readLine(String mess){
                String line="";
                boolean finish = false;
                String mess0 = "Input type: String [a line]\n";

                System.out.flush();

                while(!finish){
                        line = JOptionPane.showInputDialog(mess0+mess);
                        if(line!=null){
                                finish=true;
                        }
                }
                return line;
        }

        // Reads a line from a dialog box with a prompt message and the return
        // of a default option if the return key alone is pressed
        public static final synchronized String readLine(String mess, String dflt){
                String line="";
                boolean finish = false;
                String mess0 = "Input type: String [a line]\n";
                mess = mess +"\n";
                String dfltmess = dflt + "";

                System.out.flush();

                while(!finish){
                        line = JOptionPane.showInputDialog(mess0+mess + " [default value = " + dflt + "] ", dfltmess);
                        if(line!=null){
                            if(line.equals("")){
                                line=dflt;
                                finish=true;
                            }
                            else{
                                 finish=true;
                            }
                        }
                }
                return line;
        }

        // Reads a line from the dialog box
        // No prompt message, No default option
        public static final synchronized String readLine(){
                String line="";
                String mess="Input type: String [a line]";
                boolean finish = false;
                System.out.flush();

                while(!finish){
                        line = JOptionPane.showInputDialog(mess);
                        if(line!=null){
                             finish=true;
                        }
                }
                return line;
        }

        // Reads a boolean from a dialog box with a prompt message and the return
        // of a default option if the return key alone is pressed
        public static final synchronized boolean readBoolean(String mess, boolean dflt){
                String line="";
                boolean b=false;
                boolean finish = false;
                System.out.flush();
                String mess0 = "Input boolean\n";
                mess = mess + "\n";
                String dfltmess = dflt+"";

                while(!finish){
                        line = JOptionPane.showInputDialog(mess0 + mess + " [default value = " + dflt + "] ", dfltmess);

                        if(line!=null){
                            if(line.equals("")){
                                b=dflt;
                                finish=true;
                                line=null;
                            }
                            else{
                                if(line.equals("true") || line.trim().equals("TRUE")){
                                    b=true;
                                    finish=true;
                                }
                                else{
                                    if(line.equals("false") || line.trim().equals("FALSE")){
                                        b=false;
                                        finish=true;
                                    }
                                }
                            }
                        }
                }
                return b;
        }

        // Reads a boolean from a dialog box with a prompt message
        // No default option
        public static final synchronized boolean readBoolean(String mess){
                String line="";
                boolean b=false;
                boolean finish = false;
                System.out.flush();
                String mess0 = "Input type: boolean\n";

                while(!finish){
                        line = JOptionPane.showInputDialog(mess0+mess);
                        if(line!=null){
                            if(line.equals("true") || line.trim().equals("TRUE")){
                                b=true;
                                finish=true;
                            }
                            else{
                                if(line.equals("false") || line.trim().equals("FALSE")){
                                    b=false;
                                    finish=true;
                                }
                            }
                        }
                }
                return b;
        }

        // Reads a boolean from the dialog box
        // No prompt message, No default option
        public static final synchronized boolean readBoolean(){
                String line="";
                String mess="Input type: boolean";
                boolean b=false;
                boolean finish = false;
                System.out.flush();

                while(!finish){
                        line = JOptionPane.showInputDialog(mess);
                        if(line!=null){
                            if(line.equals("true") || line.trim().equals("TRUE")){
                                b=true;
                                finish=true;
                            }
                            else{
                                if(line.equals("false") || line.trim().equals("FALSE")){
                                    b=false;
                                    finish=true;
                                }
                            }
                        }
                }
                return b;
        }

        // Read a BigDecimal  from dialog box with a prompt message
        // No default option
        public static final synchronized BigDecimal readBigDecimal(String mess){
                String line="";
                BigDecimal big = null;
                boolean finish = false;
                String mess0 = "Input type: BigDecimal\n";

                System.out.flush();

                while(!finish){
                        line = JOptionPane.showInputDialog(mess0+mess);
                        if(line!=null){
                            try{
                                big = new BigDecimal(line);
                                finish=true;
                            }catch(NumberFormatException e){
                                // Valid BigDecimal not entered - dialog box recalled
                            }
                        }
                }
                return big;
        }

        // Reads a BigDecimal from a dialog box with a prompt message and the return
        // of a default option if the return key alone is pressed - BigDecimal default
        public static final synchronized BigDecimal readBigDecimal(String mess, BigDecimal dflt){
                String line="";
                BigDecimal big = null;
                boolean finish = false;
                String mess0 = "Input type: BigDecimal\n";
                String dfltmess = dflt.toString()+"";
                mess = mess + "\n";

                System.out.flush();

                while(!finish){
                        line = JOptionPane.showInputDialog(mess0 + mess + " [default value = " + dflt + "] ", dfltmess);

                        if(line!=null){
                            if(line.equals("")){
                                big = dflt;
                                finish=true;
                                line=null;
                            }
                            else{
                                try{
                                    big = new BigDecimal(line);
                                    finish=true;
                                }catch(NumberFormatException e){
                                    // Valid BigDecimal not entered - dialog box recalled
                                }
                            }
                        }
                }
                return big;
        }

        // Reads a BigDecimal from a dialog box with a prompt message and the return
        // of a default option if the return key alone is pressed - String default
        public static final synchronized BigDecimal readBigDecimal(String mess, String dflt){
                String line="";
                BigDecimal big = null;
                boolean finish = false;
                String mess0 = "Input type: BigDecimal\n";
                String dfltmess = dflt;
                mess = mess + "\n";

                System.out.flush();


                while(!finish){
                        line = JOptionPane.showInputDialog(mess0 + mess + " [default value = " + dflt + "] ", dfltmess);

                        if(line!=null){
                            if(line.equals("")){
                                big = new BigDecimal(dflt);
                                finish=true;
                                line=null;
                            }
                            else{
                                try{
                                    big = new BigDecimal(line);
                                    finish=true;
                                }catch(NumberFormatException e){
                                    // Valid BigDecimal not entered - dialog box recalled
                                }
                            }
                        }
                }
                return big;
        }

        // Reads a BigDecimal from a dialog box with a prompt message and the return
        // of a default option if the return key alone is pressed - double default
        public static final synchronized BigDecimal readBigDecimal(String mess, double dflt){
                String line="";
                BigDecimal big = null;
                boolean finish = false;
                String mess0 = "Input type: BigDecimal\n";
                Double dfltD = new Double(dflt);
                String dfltmess = dfltD.toString();
                mess = mess + "\n";

                System.out.flush();


                while(!finish){
                        line = JOptionPane.showInputDialog(mess0 + mess + " [default value = " + dflt + "] ", dfltmess);

                        if(line!=null){
                            if(line.equals("")){
                                big = new BigDecimal(dfltmess);
                                finish=true;
                                line=null;
                            }
                            else{
                                try{
                                    big = new BigDecimal(line);
                                    finish=true;
                                }catch(NumberFormatException e){
                                    // Valid BigDecimal not entered - dialog box recalled
                                }
                            }
                        }
                }
                return big;
        }

        // Reads a BigDecimal from a dialog box with a prompt message and the return
        // of a default option if the return key alone is pressed - float default
        public static final synchronized BigDecimal readBigDecimal(String mess, float dflt){
                String line="";
                BigDecimal big = null;
                boolean finish = false;
                String mess0 = "Input type: BigDecimal\n";
                Float dfltF = new Float(dflt);
                String dfltmess = dfltF.toString();
                mess = mess + "\n";

                System.out.flush();


                while(!finish){
                        line = JOptionPane.showInputDialog(mess0 + mess + " [default value = " + dflt + "] ", dfltmess);

                        if(line!=null){
                            if(line.equals("")){
                                big = new BigDecimal(dfltmess);
                                finish=true;
                                line=null;
                            }
                            else{
                                try{
                                    big = new BigDecimal(line);
                                    finish=true;
                                }catch(NumberFormatException e){
                                    // Valid BigDecimal not entered - dialog box recalled
                                }
                            }
                        }
                }
                return big;
        }

        // Reads a BigDecimal from a dialog box with a prompt message and the return
        // of a default option if the return key alone is pressed - long default
        public static final synchronized BigDecimal readBigDecimal(String mess, long dflt){
                String line="";
                BigDecimal big = null;
                boolean finish = false;
                String mess0 = "Input type: BigDecimal\n";
                Long dfltF = new Long(dflt);
                String dfltmess = dfltF.toString();
                mess = mess + "\n";

                System.out.flush();


                while(!finish){
                        line = JOptionPane.showInputDialog(mess0 + mess + " [default value = " + dflt + "] ", dfltmess);

                        if(line!=null){
                            if(line.equals("")){
                                big = new BigDecimal(dfltmess);
                                finish=true;
                                line=null;
                            }
                            else{
                                try{
                                    big = new BigDecimal(line);
                                    finish=true;
                                }catch(NumberFormatException e){
                                    // Valid BigDecimal not entered - dialog box recalled
                                }
                            }
                        }
                }
                return big;
        }

// Reads a BigDecimal from a dialog box with a prompt message and the return
        // of a default option if the return key alone is pressed - int default
        public static final synchronized BigDecimal readBigDecimal(String mess, int dflt){
                String line="";
                BigDecimal big = null;
                boolean finish = false;
                String mess0 = "Input type: BigDecimal\n";
                Integer dfltF = new Integer(dflt);
                String dfltmess = dfltF.toString();
                mess = mess + "\n";

                System.out.flush();


                while(!finish){
                        line = JOptionPane.showInputDialog(mess0 + mess + " [default value = " + dflt + "] ", dfltmess);

                        if(line!=null){
                            if(line.equals("")){
                                big = new BigDecimal(dfltmess);
                                finish=true;
                                line=null;
                            }
                            else{
                                try{
                                    big = new BigDecimal(line);
                                    finish=true;
                                }catch(NumberFormatException e){
                                    // Valid BigDecimal not entered - dialog box recalled
                                }
                            }
                        }
                }
                return big;
        }

        // Reads a BigDecimal from the dialog box
        // No prompt message, No default option
        public static final synchronized BigDecimal readBigDecimal(){
                String line="";
                String mess="Input type: BigDecimal";
                BigDecimal big = null;
                boolean finish = false;
                System.out.flush();

                while(!finish){
                        line = JOptionPane.showInputDialog(mess);
                        if(line!=null){
                            try{
                                big = new BigDecimal(line.trim());
                                finish=true;
                            }catch(NumberFormatException e){
                                // Valid BigDecimal not entered - dialog box recalled
                            }
                        }
                }
                return big;
        }

        // Read a BigInteger  from dialog box with a prompt message
        // No default option
        public static final synchronized BigInteger readBigInteger(String mess){
                String line="";
                BigInteger big = null;
                boolean finish = false;
                String mess0 = "Input type: BigInteger\n";

                System.out.flush();

                while(!finish){
                        line = JOptionPane.showInputDialog(mess0+mess);
                        if(line!=null){
                            try{
                                big = new BigInteger(line);
                                finish=true;
                            }catch(NumberFormatException e){
                                // Valid BigInteger not entered - dialog box recalled
                            }
                        }
                }
                return big;
        }

        // Reads a BigInteger from a dialog box with a prompt message and the return
        // of a default option if the return key alone is pressed - BigInteger default
        public static final synchronized BigInteger readBigInteger(String mess, BigInteger dflt){
                String line="";
                BigInteger big = null;
                boolean finish = false;
                String mess0 = "Input type: BigInteger\n";
                String dfltmess = dflt.toString()+"";
                mess = mess + "\n";

                System.out.flush();

                while(!finish){
                        line = JOptionPane.showInputDialog(mess0 + mess + " [default value = " + dflt + "] ", dfltmess);

                        if(line!=null){
                            if(line.equals("")){
                                big = dflt;
                                finish=true;
                                line=null;
                            }
                            else{
                                try{
                                    big = new BigInteger(line);
                                    finish=true;
                                }catch(NumberFormatException e){
                                    // Valid BigInteger not entered - dialog box recalled
                                }
                            }
                        }
                }
                return big;
        }

        // Reads a BigInteger from a dialog box with a prompt message and the return
        // of a default option if the return key alone is pressed - String default
        public static final synchronized BigInteger readBigInteger(String mess, String dflt){
                String line="";
                BigInteger big = null;
                boolean finish = false;
                String mess0 = "Input type: BigInteger\n";
                String dfltmess = dflt;
                mess = mess + "\n";

                System.out.flush();


                while(!finish){
                        line = JOptionPane.showInputDialog(mess0 + mess + " [default value = " + dflt + "] ", dfltmess);

                        if(line!=null){
                            if(line.equals("")){
                                big = new BigInteger(dflt);
                                finish=true;
                                line=null;
                            }
                            else{
                                try{
                                    big = new BigInteger(line);
                                    finish=true;
                                }catch(NumberFormatException e){
                                    // Valid BigInteger not entered - dialog box recalled
                                }
                            }
                        }
                }
                return big;
        }

        // Reads a BigInteger from a dialog box with a prompt message and the return
        // of a default option if the return key alone is pressed - long default
        public static final synchronized BigInteger readBigInteger(String mess, long dflt){
                String line="";
                BigInteger big = null;
                boolean finish = false;
                String mess0 = "Input type: BigInteger\n";
                Long dfltF = new Long(dflt);
                String dfltmess = dfltF.toString();
                mess = mess + "\n";

                System.out.flush();


                while(!finish){
                        line = JOptionPane.showInputDialog(mess0 + mess + " [default value = " + dflt + "] ", dfltmess);

                        if(line!=null){
                            if(line.equals("")){
                                big = new BigInteger(dfltmess);
                                finish=true;
                                line=null;
                            }
                            else{
                                try{
                                    big = new BigInteger(line);
                                    finish=true;
                                }catch(NumberFormatException e){
                                    // Valid BigInteger not entered - dialog box recalled
                                }
                            }
                        }
                }
                return big;
        }

        // Reads a BigInteger from a dialog box with a prompt message and the return
        // of a default option if the return key alone is pressed - int default
        public static final synchronized BigInteger readBigInteger(String mess, int dflt){
                String line="";
                BigInteger big = null;
                boolean finish = false;
                String mess0 = "Input type: BigInteger\n";
                Integer dfltF = new Integer(dflt);
                String dfltmess = dfltF.toString();
                mess = mess + "\n";

                System.out.flush();


                while(!finish){
                        line = JOptionPane.showInputDialog(mess0 + mess + " [default value = " + dflt + "] ", dfltmess);

                        if(line!=null){
                            if(line.equals("")){
                                big = new BigInteger(dfltmess);
                                finish=true;
                                line=null;
                            }
                            else{
                                try{
                                    big = new BigInteger(line);
                                    finish=true;
                                }catch(NumberFormatException e){
                                    // Valid BigInteger not entered - dialog box recalled
                                }
                            }
                        }
                }
                return big;
        }

        // Reads a BigInteger from the dialog box
        // No prompt message, No default option
        public static final synchronized BigInteger readBigInteger(){
                String line="";
                String mess="Input type: BigInteger";
                BigInteger big = null;
                boolean finish = false;
                System.out.flush();

                while(!finish){
                        line = JOptionPane.showInputDialog(mess);
                        if(line!=null){
                            try{
                                big = new BigInteger(line.trim());
                                finish=true;
                            }catch(NumberFormatException e){
                                // Valid BigInteger not entered - dialog box recalled
                            }
                        }
                }
                return big;
        }

        // returns true if answer is yes, false if not, default = YES
        public static final synchronized boolean yesNo(String question){
            int ans = JOptionPane.showConfirmDialog(null, question, "Db Class Yes or No Box", JOptionPane.YES_NO_OPTION, JOptionPane.QUESTION_MESSAGE);
            boolean ansb =false;
            if(ans == 0)ansb =true;
            return ansb;
        }

        // returns true if answer is yes, false if not, default = NO
        public static final synchronized boolean noYes(String question){
            Object[] opts = {"Yes", "No"};
            int ans = JOptionPane.showOptionDialog(null, question, "Db Class Yes or No Box", JOptionPane.YES_NO_OPTION, JOptionPane.QUESTION_MESSAGE, null, opts, opts[1]);
            boolean ansb =false;
            if(ans == 0)ansb =true;
            return ansb;
        }


        // Shows a message and the value of a double in a message dialogue box
        public static final synchronized void show(String message, double output){
            JOptionPane.showMessageDialog(null, message+" "+output, "Db.show (double)", JOptionPane.INFORMATION_MESSAGE);
        }

         // Shows a message and the value of a truncated double in a message dialogue box
        public static final synchronized void show(String message, double output, int trunc){
            JOptionPane.showMessageDialog(null, message+" "+MathFns.truncate(output, trunc), "Db.show (double)", JOptionPane.INFORMATION_MESSAGE);
        }

        // Shows a message and the value of a float in a message dialogue box
        public static final synchronized void show(String message, float output){
            JOptionPane.showMessageDialog(null, message+" "+output, "Db.show (float)", JOptionPane.INFORMATION_MESSAGE);
        }

        // Shows a message and the value of a truncated float in a message dialogue box
        public static final synchronized void show(String message, float output, int trunc){
            JOptionPane.showMessageDialog(null, message+" "+MathFns.truncate(output, trunc), "Db.show (float)", JOptionPane.INFORMATION_MESSAGE);
        }

        // Shows a message and the value of a BigDecimal in a message dialogue box
        public static final synchronized void show(String message, BigDecimal output){
            JOptionPane.showMessageDialog(null, message+" "+output.toString(), "Db.show (BigDecimal)", JOptionPane.INFORMATION_MESSAGE);
        }

        // Shows a message and the value of a BigInteger in a message dialogue box
        public static final synchronized void show(String message, BigInteger output){
            JOptionPane.showMessageDialog(null, message+" "+output.toString(), "Db.show (BigInteger)", JOptionPane.INFORMATION_MESSAGE);
        }

        // Shows a message and the value of a int in a message dialogue box
        public static final synchronized void show(String message, int output){
            JOptionPane.showMessageDialog(null, message+" "+output, "Db.show (int)", JOptionPane.INFORMATION_MESSAGE);
        }

        // Shows a message and the value of a long in a message dialogue box
        public static final synchronized void show(String message, long output){
            JOptionPane.showMessageDialog(null, message+" "+output, "Db.show (long)", JOptionPane.INFORMATION_MESSAGE);
        }

        // Shows a message and the value of a short in a message dialogue box
        public static final synchronized void show(String message, short output){
            JOptionPane.showMessageDialog(null, message+" "+output, "Db.show (short)", JOptionPane.INFORMATION_MESSAGE);
        }

        // Shows a message and the value of a byte in a message dialogue box
        public static final synchronized void show(String message, byte output){
            JOptionPane.showMessageDialog(null, message+" "+output, "Db.show (byte)", JOptionPane.INFORMATION_MESSAGE);
        }

        // Shows a message and the value of a Complex in a message dialogue box
        public static final synchronized void show(String message, Complex output){
            JOptionPane.showMessageDialog(null, message+" "+output, "Db.show (Complex)", JOptionPane.INFORMATION_MESSAGE);
        }

        // Shows a message and the value of a truncated Complex in a message dialogue box
        public static final synchronized void show(String message, Complex output, int trunc){
            JOptionPane.showMessageDialog(null, message+" "+Complex.truncate(output, trunc), "Db.show (Complex)", JOptionPane.INFORMATION_MESSAGE);
        }

        // Shows a message and the value of a ErrorProp in a message dialogue box
        public static final synchronized void show(String message, ErrorProp output){
            JOptionPane.showMessageDialog(null, message+" "+output, "Db.show (ErrorProp)", JOptionPane.INFORMATION_MESSAGE);
        }

        // Shows a message and the value of a ErrorProp in a message dialogue box
        public static final synchronized void show(String message, ErrorProp output, int trunc){
            JOptionPane.showMessageDialog(null, message+" "+ErrorProp.truncate(output, trunc), "Db.show (ErrorProp)", JOptionPane.INFORMATION_MESSAGE);
        }

        // Shows a message and the value of a ComplexErrorProp in a message dialogue box
        public static final synchronized void show(String message, ComplexErrorProp output){
            JOptionPane.showMessageDialog(null, message+" "+output, "Db.show (ComplexErrorProp)", JOptionPane.INFORMATION_MESSAGE);
        }

        // Shows a message and the value of a truncated ComplexErrorProp in a message dialogue box
        public static final synchronized void show(String message, ComplexErrorProp output, int trunc){
            JOptionPane.showMessageDialog(null, message+" "+ComplexErrorProp.truncate(output, trunc), "Db.show (ComplexErrorProp)", JOptionPane.INFORMATION_MESSAGE);
        }
        // Shows a message and the value of a boolean in a message dialogue box
        public static final synchronized void show(String message, boolean output){
            JOptionPane.showMessageDialog(null, message+" "+output, "Db.show (boolean)", JOptionPane.INFORMATION_MESSAGE);
        }

        // Shows a message and the value of a char in a message dialogue box
        public static final synchronized void show(String message, char output){
            JOptionPane.showMessageDialog(null, message+" "+output, "Db.show (char)", JOptionPane.INFORMATION_MESSAGE);
        }

        // Shows a message and the value of a String in a message dialogue box
        public static final synchronized void show(String message, String output){
            JOptionPane.showMessageDialog(null, message+" "+output, "Db.show (String)", JOptionPane.INFORMATION_MESSAGE);
        }

        // Shows a message only in a message dialogue box
        public static final synchronized void show(String message){
            JOptionPane.showMessageDialog(null, message, "Db.show (message only)", JOptionPane.INFORMATION_MESSAGE);
        }

        // Multiple choice box - Multiple query column closely matching box row
        public static final synchronized int optionBox(String headerComment, String[] comments, String[] boxTitles, int defaultBox){
            int nChoice = boxTitles.length;
            if(nChoice!=comments.length)throw new IllegalArgumentException("There must be the same number of boxTitles and comments");
            Object[] options = new Object[nChoice];
            for(int i=0; i<nChoice; i++){
                options[i] =  "(" + (i+1) +") " + boxTitles[i];
            }
            String quest = "1. " + comments[0] + "\n";
            for(int i=1; i<nChoice; i++){
                quest = quest  + (i+1) +". " + comments[i] + "\n";
            }

            return 1 + JOptionPane.showOptionDialog(null, quest, headerComment, JOptionPane.YES_NO_CANCEL_OPTION, JOptionPane.QUESTION_MESSAGE,null, options, options[defaultBox-1]);
        }

        // Multiple choice box - Single general query
        public static final synchronized int optionBox(String headerComment, String quest, String[] boxTitles, int defaultBox){
           int nChoice = boxTitles.length;
           Object[] options = new Object[nChoice];
            for(int i=0; i<nChoice; i++){
                options[i] =  "(" + (i+1) +") " + boxTitles[i];
            }

            return 1 + JOptionPane.showOptionDialog(null, quest, headerComment, JOptionPane.YES_NO_CANCEL_OPTION, JOptionPane.QUESTION_MESSAGE,null, options, options[defaultBox-1]);
        }

        // Displays dialogue box asking if you wish to exit program
        // Answering yes end program
        public static final synchronized void endProgram(){

                int ans = JOptionPane.showConfirmDialog(null, "Do you wish to end the program", "End Program", JOptionPane.YES_NO_OPTION, JOptionPane.QUESTION_MESSAGE);
                if(ans==0){
                    System.exit(0);
                }
                else{
                    JOptionPane.showMessageDialog(null, "Now you must press the appropriate escape key/s, e.g. Ctrl C, to exit this program");
                }
        }
}

