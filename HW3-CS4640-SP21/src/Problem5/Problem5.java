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

//Hint: https://www.novixys.com/blog/java-aes-example/

class DecryptFile
{
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

    public static byte[] readByteFromFile(String inputFileName, int dataSize)
    {
        byte[]  rawData = new byte[dataSize]; 
        try {
            FileInputStream inFile = new FileInputStream(inputFileName);
            int bytesRead ; 
            if((bytesRead = inFile.read(rawData))!=-1){
                if(bytesRead == dataSize){
                    return rawData ;
                }
                else{
                    System.out.println("ERROR: Expected reading " + dataSize + "bytes but found " + bytesRead + "bytes in the file: " + inputFileName);
                    System.exit(20);
                    return null ; 
                }
            }
            else{
                System.out.println("ERROR: Could read raw data from the file: " + inputFileName);
                System.exit(20);
                return null ; 
            }
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("ERROR: Could read raw data from the file: " + inputFileName);
            System.exit(20);
            return null ; 
        }

    }
    public static void doDecryptionAndWriteToFile(Cipher cipherContext, String outputPlaintextFile, String inputCiphertextFile)
    {
        //TODO: FILL OUT THIS FUNCTION (HANDLE ERRORS AND EXCEPTIONS)
        try{
            processFile(cipherContext, inputCiphertextFile, outputPlaintextFile);
        }catch(Exception e){
            e.printStackTrace();
        }

    }

    public static void setupAndDecrypt(String outputPlaintextFile, String inputKeyFile, String inputIVFile, String inputCiphertextFile)
    {
        //TODO: FILL OUT THIS FUNCTION (HANDLE ERRORS AND EXCEPTIONS)
        
        // -- load raw IV bytes from the file given by inputIVFile (Use readBytesFromFile) IV LENGTH = 16 BYTES 
        // -- Generate IvParameterSpec object from raw IV bytes  
        // -- load raw key bytes from the file given by inputKeyFile (Use readBytesFromFile) KEY LENGTH = 16 bytes 
        // -- create a secret key spec object from raw key bytes and for "AES" algorithm (handle exception with try-catch)
        // Create a Cipher object with "AES/CBC/PKCS5Padding" (handle exception with try-catch)
        // Initialize the cipher object with the secret key and IV parameter spec obtain before in the Cipher.DECRYPT_MODE
        // Call the doEncryption function 

        try{
            // 1. IV
            byte[] iv = readByteFromFile(inputIVFile, 16);
            IvParameterSpec ivspec = new IvParameterSpec(iv);

            // 2. keys
            byte[] keyb = readByteFromFile(inputKeyFile, 16);
            SecretKeySpec skey = new SecretKeySpec(keyb, "AES");

            // 2.5 Check key & iv length
            if (iv == null){
                System.out.println("ERROR: Invalid IV");
            }            
            if (keyb == null){
                System.out.println("ERROR: Invalid key");
            }

            // 3. Cipher object
            Cipher ci = Cipher.getInstance("AES/CBC/PKCS5Padding");
            ci.init(Cipher.DECRYPT_MODE, skey, ivspec);

            // 4. Decrypt
            doDecryptionAndWriteToFile(ci, outputPlaintextFile, inputCiphertextFile);
        }catch(Exception e){
            e.printStackTrace();
        }
    }

}


public class Problem5 {
    public static void main(String args[])
    {
        if(args.length != 4)
        {
            System.out.println("Usage: java Problem5 <name-of-output-plaintext-file> <input-key-file> <input-IV-file> <input-ciphertext-file>");
            return ; 
        }
        DecryptFile.setupAndDecrypt(args[0], args[1], args[2], args[3]);

    }
}
