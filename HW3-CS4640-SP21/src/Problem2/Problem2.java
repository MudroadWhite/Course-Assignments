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

class GenerateKey
{
    public static void generateAndWriteKey(int keySize, String outputFileName)
    {
        //TODO: Fill up this function 
        //TODO: USE CRYPTOGRAPHICALLY SECURE RANDOM NUMBER GENERATOR
        //Please make sure you handle exceptions and other error cases carefully
        //Hint: https://howtodoinjava.com/java8/secure-random-number-generation/ 
        try{
            SecureRandom secureRandomGenerator = SecureRandom.getInstance("SHA1PRNG", "SUN");
            byte[] key = new byte[keySize];
            secureRandomGenerator.nextBytes(key);

            Files.write(Path.of(outputFileName), key);
        }
        catch(Exception e){
            e.printStackTrace();
        }
    }
}


public class Problem2 {
    public static void main(String args[]){
        if(args.length != 2)
        {
            System.out.println("Usage: java Problem2 <size-of-random-bytes> <output-file-to-store-key>");
            return ; 
        }
        GenerateKey.generateAndWriteKey(Integer.parseInt(args[0]), args[1]);

    }
}
