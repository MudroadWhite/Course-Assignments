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

class RandomOneTimePad
{
    public static void DoEncryption(String plainFileName, String keyFileName, String outputFileName)
    {
        //Please make sure you handle all the exceptions and error conditions..
        try{
            byte[] message = Files.readAllBytes(Path.of(plainFileName));

            InputStream keyFile = new FileInputStream(keyFileName);
            long keySize = new File(keyFileName).length();
            byte [] key = new byte[(int) keySize];

            if (message.length != keySize){
                System.out.println("ERROR: Key size and plain text mismatch");
                keyFile.close();
                return;
            }

            for (int i = 0; i < keySize; i++){
                message[i] = (byte) (message[i] ^ key[i]);
            }
            
            FileOutputStream outputFile = null;
            outputFile = new FileOutputStream(outputFileName);
            outputFile.write(message);

            outputFile.close();
            keyFile.close();
        }
        catch(Exception e){
            e.printStackTrace();
        }
    }
};


public class Problem3 {
    public static void main(String args[]){
        if(args.length != 3)
        {
            System.out.println("Usage: java Problem3 <binary-plaintext> <key-file><binary-ciphertext>");
            return ; 
        }
        RandomOneTimePad.DoEncryption(args[0], args[1], args[2]);

    }
}
