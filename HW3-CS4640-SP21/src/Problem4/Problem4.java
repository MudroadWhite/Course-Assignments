import java.io.FileInputStream;
import java.io.InputStream;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.OutputStream;
import java.util.*;
import java.io.File ; 
import java.nio.*; 
import java.nio.file.Files;
import java.nio.file.Paths;
import java.io.FileOutputStream;
import java.security.SecureRandom;
import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;
import javax.crypto.spec.IvParameterSpec;
import java.util.Base64;

import java.security.NoSuchAlgorithmException;
import java.security.NoSuchProviderException;
import java.security.SecureRandom;
import java.nio.file.Path;

// Hint: https://www.novixys.com/blog/java-aes-example/

class EncryptFile{

    static private void processFile(Cipher ci,String inFile,String outFile)
    throws javax.crypto.IllegalBlockSizeException,
           javax.crypto.BadPaddingException,
           java.io.IOException
    {
        try (FileInputStream in = new FileInputStream(inFile);
             FileOutputStream out = new FileOutputStream(outFile)) {
            byte[] ibuf = new byte[1024];
            int len;
            int sum = 0;
            while ((len = in.read(ibuf)) != -1) {
                byte[] obuf = ci.update(ibuf, 0, len);
                if ( obuf != null ) out.write(obuf);
                sum += len;
            }
            byte[] obuf = ci.doFinal();
            if ( obuf != null ) out.write(obuf);
            System.out.println("Wrote " + (sum + obuf.length) + "bytes in the file: " + outFile); 
        }
    }

    public static byte[] IVGen()
    {
        //TODO: Fill out this function 
        byte[] iv = new byte[16];
         try{
            SecureRandom secureRandomGenerator = SecureRandom.getInstance("SHA1PRNG", "SUN");
            secureRandomGenerator.nextBytes(iv);
         }
         catch(Exception e){
             e.printStackTrace();
         }
         return iv;
    }
    public static void writeByteToFile(byte[] data, String outputFileName)
    {
        FileOutputStream outputFile = null;
        try {
            outputFile = new FileOutputStream(outputFileName);
            outputFile.write(data);
            System.out.println("Wrote " + data.length + "bytes in the file: " + outputFileName); 
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("ERROR: Couldn't write to file: " + outputFileName);
        }
    }
    public static void doEncryptionAndWriteToFile(Cipher cipherContext, String inputPlaintextFile, String outputCiphertextFile)
    {
        //TODO: Fill out this function 
        try{
            processFile(cipherContext, inputPlaintextFile, outputCiphertextFile);
        }catch (Exception e) {
            e.printStackTrace();
        }
    }
    public static void setupAndEncrypt(String inputPlaintextFile, String outputKeyFile, String outputIVFile, String outputCiphertextFile)
    {
        //TODO: Fill out this function. 
        
        //(********* THE FOLLOWING IS A LIST OF STEPS YOU HAVE TO DO FOR THE DESIRED FUNCTIONALITY *********)

        // -- Generate Raw IV Data using IVGen function 
        // -- Write Raw IV data to the file name provided by outputIVFile  
        // -- Generate IvParameterSpec object from IV Raw Data 
        // -- Generate AES Key through KeyGenerator and SecretKey (handle exception with try-catch)
        // -- Obtain raw key bytes from the SecretKey instance 
        // -- Write raw key bytes into the filed name provided by outputKeyFile 
        // -- Create a Cipher object with "AES/CBC/PKCS5Padding" (handle exception with try-catch)
        // -- Initialize the cipher object with the secret key and IV parameter spec obtain before 
        // -- Call the doEncryption function to actually encrypt the file and output the ciphertext in the output file 

        // 1. IV
        byte [] iv = IVGen();
        IvParameterSpec ivspec = new IvParameterSpec( iv );

        try{
            // 1.5 write it to output IV file
            FileOutputStream outiv = new FileOutputStream(outputIVFile);
            outiv.write(iv);
            outiv.close();

            // 2. key
            KeyGenerator kgen = KeyGenerator.getInstance("AES");
            SecretKey skey = kgen.generateKey();
            byte[] keyb = skey.getEncoded();

            FileOutputStream outkey = new FileOutputStream(outputKeyFile);
            outkey.write(keyb);
            outkey.close();
            
            // 3. Cipher object
            Cipher ci = Cipher.getInstance("AES/CBC/PKCS5Padding");
            ci.init(Cipher.ENCRYPT_MODE, skey, ivspec);

            // 4. Encryption
            doEncryptionAndWriteToFile(ci, inputPlaintextFile, outputCiphertextFile);
        }
        catch(Exception e){
            e.printStackTrace();
        }
    }

}

public class Problem4 {
    public static void main(String args[])
    {
        if(args.length != 4)
        {
            System.out.println("Usage: java Problem4 <name-of-plaintext-file> <output-key-file> <output-IV-file> <output-ciphertext-file>");
            return ; 
        }
        EncryptFile.setupAndEncrypt(args[0], args[1], args[2], args[3]);

    }
}
