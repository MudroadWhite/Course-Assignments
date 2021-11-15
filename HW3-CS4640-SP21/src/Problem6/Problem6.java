import java.io.FileInputStream;
import java.io.InputStream;
import java.io.FileOutputStream;
import java.io.OutputStream;
import java.util.*;
import java.io.File ; 
import java.nio.*; 
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.Path;

import java.nio.ByteBuffer;

import java.util.Arrays;

class InputSorter{

    private static boolean compareLT(byte[] r1, byte[] r2){
        byte [] k1 = keyOf(r1);
        byte [] k2 = keyOf(r2);
        ByteBuffer b1 = ByteBuffer.wrap(k1);
        b1.order(ByteOrder.LITTLE_ENDIAN);
        ByteBuffer b2 = ByteBuffer.wrap(k2);
        b2.order(ByteOrder.LITTLE_ENDIAN);

        return b1.getInt() < b2.getInt();
    }

    private static byte [] keyOf(byte [] data){
        return Arrays.copyOfRange(data, 0, 4);
    }

    private static byte [] valueOf(byte [] data){
        return Arrays.copyOfRange(data, 3, 100);
    }

    private static byte [][] merge(byte [][] r1, byte [][] r2){
        int l1 = r1.length;
        int l2 = r2.length;
        byte [][] result = new byte[l1 + l2][100];

        int i = 0, j = 0;

        for(int k = 0; k < l1 + l2; k++){
            if (i >= l1 - 1){
                result[k] = r2[j]; j++;
            }
            else if (j >= l2 - 1){
                result[k] = r1[i]; i++;
            }
            else if (compareLT(r1[i], r2[j]) == true){
                result[k] = r1[i]; i++;
            }
            else{
                result[k] = r2[j]; j++;
            }
        }
        return result;
    }

    private static byte [][] sort(byte [][] r1){
        int l1 = r1.length;
        if (l1 <= 1) return r1;
        else{
            int mid = l1 / 2;
            int remain = l1 - mid;
            byte [][] rr1 = new byte[mid][100];
            byte [][] rr2 = new byte[remain][100];
            int i = 0;
            while(i < mid){
                rr1[i] = r1[i];
                i++;
            }
            while(i < l1){
                rr2[i - mid] = r1[i];
                i++;
            }
            return merge(sort(rr1), sort(rr2));
        }
    }


    public static void sortBinaryRecords(String inputFileName, String outputFileName)
    {
        try{
            // NOTE: Assume the file is well formated
            // 1. Read bytes
            byte[] raw = Files.readAllBytes(Paths.get(inputFileName));
            int l = raw.length / 100;
            if (l * 100 != raw.length){
                System.out.println("ERROR: Ill-formatted file");
                return;
            }

            // 2. Reformat the data
            byte [][] records = new byte [l][100];
            for (int i = 0; i < l; i++){
                for (int j = 0; j < 100; j++){
                    records[i][j] = raw[j + i * 100];
                }
            }

            // 3. Sort the data
            byte [][] sorted = sort(records);

            // 4. Reformat and output the result
            byte [] result = new byte [96 * l];
            for (int i = 0; i < l; i++){
                byte [] v = valueOf(sorted[i]);
                for(int j = 0; j < 96; j++){
                    result [i * 96 + j] = v[j];
                }
            }
            Files.write(Path.of(outputFileName), result);
        }
        catch(Exception e){
            e.printStackTrace();
        }
    }
}


public class Problem6
{
    public static void main(String args[])
    {
        if(args.length != 2)
        {
            System.out.println("Usage: java problem6 <input-file-name-to-sort> <output-file-to-save-sorted>");
            return ; 
        }
        InputSorter.sortBinaryRecords(args[0], args[1]);
    }
}