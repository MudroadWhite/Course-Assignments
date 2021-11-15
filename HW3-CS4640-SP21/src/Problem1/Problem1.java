import java.io.FileInputStream;
import java.io.InputStream;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.OutputStream;
import java.util.*;
import java.io.File ; 
import java.nio.*; 
import java.nio.file.Files;
import java.nio.file.Path;

class HexadecimalConverter
{
    public static void ReadAndWriteHex(String inpFileName, String outFileName)
    {
        try{  
            // Path fn = Path.of(inpFileName);
            // String str = Files.readString(fn); // Java11 method
            // char ch[] = str.toCharArray();
            // StringBuffer sb = new StringBuffer();
            // for(int i = 0; i < ch.length; i++) {
            //     String hexString = Integer.toHexString(ch[i]);
            //     sb.append(hexString);
            //  }
            // String result = sb.toString();

            // File output = new File(outFileName);
            // FileWriter writer = new FileWriter(output);
            // writer.write(result);
            // writer.flush();
            // writer.close();

            
            InputStream inputStream = new FileInputStream(inpFileName);
            // OutputStream outputStream = new FileOutputStream(outFileName);
 
            long fileSize = new File(inpFileName).length();
 
            byte[] allBytes = new byte[(int) fileSize];
 
            inputStream.read(allBytes);
            
            StringBuilder sb = new StringBuilder();

            for (byte b : allBytes) {
                sb.append(String.format("%02X", b));
            }

            String out = sb.toString();

            File output = new File(outFileName);
            FileWriter writer = new FileWriter(output);
            writer.write(out);
            writer.flush();
            writer.close();
            inputStream.close();
        }
        catch(Exception e){
            e.printStackTrace();
        }
        finally{
        }
    }

}

public class Problem1
{
    public static void main(String args[])
    {
        // HexadecimalConverter.ReadAndWriteHex("123.txt", "123out.txt");
        if(args.length != 2)
        {
            System.out.println("Usage: java problem1 <binary-input-file-name-to-read> <output-file-to-save-hexadecimal>");
            return ; 
        }
        HexadecimalConverter.ReadAndWriteHex(args[0], args[1]);
    }
}