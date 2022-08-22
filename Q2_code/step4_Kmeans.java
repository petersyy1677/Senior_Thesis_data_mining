package com.eecs476;

//import javafx.util.Pair;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.DoubleWritable;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.lang.reflect.Array;
import java.net.URI;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.InputFormat;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.MultipleInputs;
import org.apache.hadoop.mapreduce.lib.input.KeyValueTextInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;

import java.io.IOException;
import java.util.*;

public class step4_Kmeans {
    private static double length(String v) {
        String[] vec = v.split(",");
        double l = 0;
        for (String s : vec) {
            l += Double.parseDouble(s)*Double.parseDouble(s);
        }
        return l;
    }

    private static double distance(int type, String v1, String v2) {
        String[] var1 = v1.split(",");
        String[] var2 = v2.split(",");
        ArrayList<Double> vector1 = new ArrayList<>();
        ArrayList<Double> vector2 = new ArrayList<>();
        for (String s : var1) {
            vector1.add(Double.parseDouble(s));
        }
        for (String s : var2) {
            vector2.add(Double.parseDouble(s));
        }
        double l2 = (double) 0;
        double l1 = (double) 0;
        for (int i = 0; i < vector1.size(); i++) {
            l2 += (vector1.get(i) - vector2.get(i))*(vector1.get(i) - vector2.get(i));
            l1 += Math.abs(vector1.get(i) - vector2.get(i));
        }
        if (type==1) {
            return l1;
        }
        return l2;
    }


    public static class job_mapper1
      extends Mapper<LongWritable, Text, Text, Text>{
        ArrayList<String> centroids = null;
        public void setup(Context context) throws IOException,
          InterruptedException
        {
            centroids = new ArrayList<>();

            URI[] cacheFiles = context.getCacheFiles();

            if (cacheFiles != null && cacheFiles.length > 0)
            {
                String line = "";
                FileSystem fs = FileSystem.get(context.getConfiguration());
                Path getFilePath = new Path(cacheFiles[0].toString());
                BufferedReader reader = new BufferedReader(new InputStreamReader(fs.open(getFilePath)));
                double e = 0;
                while ((line = reader.readLine()) != null) {
                    if (line.indexOf('#') == -1) {
                        centroids.add(line);
                    }
                    else {
                        String[] s = line.split("#");
                        centroids.add(s[0]);
                        e += Double.parseDouble(s[1]);
                    }
                }
                if (centroids.size() > k) {
                    centroids.subList(k, centroids.size()).clear();
                }
                errors.add(e);
            }
        }

        public void map(LongWritable key, Text value, Context context
        ) throws IOException, InterruptedException {
            Configuration conf = context.getConfiguration();
            int norm = conf.getInt("norm", -1);
            double cent_length = Double.POSITIVE_INFINITY;;
            double min = Double.POSITIVE_INFINITY;;
            int min_ind = -1;
            for (int i = 0; i < centroids.size(); i++) {
                double dist = distance(norm, value.toString(), centroids.get(i));
                if (dist < min || (dist == min && length(centroids.get(i)) < cent_length)) {
                    min = dist;
                    min_ind = i;
                    cent_length = length(centroids.get(i));
                }
            }
            context.write(new Text(Integer.toString(min_ind)),new Text(value.toString() + '&' + min));
        }
    }

    public static class job_mapper2
      extends Mapper<LongWritable, Text, Text, Text>{
        ArrayList<String> centroids = null;

        public void setup(Context context) throws IOException,
          InterruptedException
        {
            centroids = new ArrayList<>();

            URI[] cacheFiles = context.getCacheFiles();

            if (cacheFiles != null && cacheFiles.length > 0)
            {
                String line = "";
                FileSystem fs = FileSystem.get(context.getConfiguration());
                Path getFilePath = new Path(cacheFiles[0].toString());
                BufferedReader reader = new BufferedReader(new InputStreamReader(fs.open(getFilePath)));
                double e = 0;
                int i = 0;
                while ((line = reader.readLine()) != null) {
                    if (line.indexOf('#') == -1) {
                        centroids.add(line);
                    }
                    else {
                        centroids.add(line.split("#")[0]);
                    }
                    i ++;
                }
                if (centroids.size() > k) {
                    centroids.subList(k, centroids.size()).clear();
                }
            }
        }

        public void map(LongWritable key, Text value, Context context
        ) throws IOException, InterruptedException {
            String val = value.toString();
            if (val.indexOf('#') != -1) {
                val = val.split("#")[0];
            }
            int index = centroids.indexOf(val);
            if (index > 0) {
                context.write(new Text(Integer.toString(index)), new Text("@" + val));
            }
            //context.write(value, new Text(centroids.get(0)));
        }
    }

    public static class job_reducer
      extends Reducer<Text,Text,Text,Text> {
        public void reduce(Text key, Iterable<Text> values,
                           Context context
        ) throws IOException, InterruptedException {

            ArrayList<String> vals = new ArrayList<>();
            ArrayList<Double> res = new ArrayList<>();
            String centr = null;
            for (Text val : values) {
                if (val.toString().charAt(0) == '@') {
                    centr = val.toString().substring(1);
                } else {
                    vals.add(val.toString());
                }
            }
            if (vals.size() == 0) {
                vals.add(centr);
            }
            double error = 0;
            String[] f = vals.get(0).split("&");
            String[] fst = f[0].split(",");
            error = Double.parseDouble(f[1]);

            for (String s : fst) {
                res.add(Double.parseDouble(s));
            }
            for (int i = 1; i < vals.size(); i++) {
                String[] t = vals.get(i).split("&");
                error += Double.parseDouble(t[1]);
                String[] vec = t[0].split(",");
                for (int j = 0; j < vec.length; j++) {
                    res.set(j,res.get(j)+Double.parseDouble(vec[j]));
                }
            }
            double size = vals.size();
            Text k = new Text(Double.toString(res.get(0) / size));
            StringBuilder builder = new StringBuilder();
            for (int i = 1; i < res.size(); i++) {
                builder.append(",").append(res.get(i) / size);
            }
            if (builder.length() > 0) {
                context.write(k, new Text( builder.toString().substring(1) + '#' + error));
            }
            else{
                context.write(k, new Text( builder.toString()  + "#" + error));
            }
        }
    }

    public static class job2_mapper1
      extends Mapper<LongWritable, Text, Text, Text>{
        ArrayList<String> centroids = null;
        public void setup(Context context) throws IOException,
          InterruptedException
        {
            centroids = new ArrayList<>();

            URI[] cacheFiles = context.getCacheFiles();

            if (cacheFiles != null && cacheFiles.length > 0)
            {
                String line = "";
                FileSystem fs = FileSystem.get(context.getConfiguration());
                Path getFilePath = new Path(cacheFiles[0].toString());
                BufferedReader reader = new BufferedReader(new InputStreamReader(fs.open(getFilePath)));
                double e = 0;
                while ((line = reader.readLine()) != null) {
                    if (line.indexOf('#') == -1) {
                        centroids.add(line);
                    }
                    else {
                        String[] s = line.split("#");
                        centroids.add(s[0]);
                        e += Double.parseDouble(s[1]);
                    }
                }
                if (centroids.size() > k) {
                    centroids.subList(k, centroids.size()).clear();
                }
                errors.add(e);
            }
        }

        public void map(LongWritable key, Text value, Context context
        ) throws IOException, InterruptedException {
            Configuration conf = context.getConfiguration();
            int norm = conf.getInt("norm", -1);
            double cent_length = Double.POSITIVE_INFINITY;;
            double min = Double.POSITIVE_INFINITY;;
            int min_ind = -1;
            for (int i = 0; i < centroids.size(); i++) {
                double dist = distance(norm, value.toString(), centroids.get(i));
                if (dist < min || (dist == min && length(centroids.get(i)) < cent_length)) {
                    min = dist;
                    min_ind = i;
                    cent_length = length(centroids.get(i));
                }
            }
            context.write(new Text(Integer.toString(min_ind)),new Text(value.toString()));
        }
    }

    public static class job2_mapper2
      extends Mapper<LongWritable, Text, Text, Text>{
        ArrayList<String> centroids = null;

        public void setup(Context context) throws IOException,
          InterruptedException
        {
            centroids = new ArrayList<>();

            URI[] cacheFiles = context.getCacheFiles();

            if (cacheFiles != null && cacheFiles.length > 0)
            {
                String line = "";
                FileSystem fs = FileSystem.get(context.getConfiguration());
                Path getFilePath = new Path(cacheFiles[0].toString());
                BufferedReader reader = new BufferedReader(new InputStreamReader(fs.open(getFilePath)));
                double e = 0;
                int i = 0;
                while ((line = reader.readLine()) != null) {
                    if (line.indexOf('#') == -1) {
                        centroids.add(line);
                    }
                    else {
                        centroids.add(line.split("#")[0]);
                    }
                    i ++;
                }
                if (centroids.size() > k) {
                    centroids.subList(k, centroids.size()).clear();
                }
            }
        }

        public void map(LongWritable key, Text value, Context context
        ) throws IOException, InterruptedException {
            String val = value.toString();
            if (val.indexOf('#') != -1) {
                val = val.split("#")[0];
            }
            int index = centroids.indexOf(val);
            //context.write(value, new Text(centroids.get(0)));
        }
    }

    public static class job2_reducer
      extends Reducer<Text,Text,Text,Text> {
        public void reduce(Text key, Iterable<Text> values,
                           Context context
        ) throws IOException, InterruptedException {
            for (Text val : values) {
                context.write(key, val);
            }

        }
    }

    private static String inputPath;
    private static String centroidPath;
    private static String outputScheme;
    private static int norm;
    private static int k;
    private static ArrayList<Boolean> run = new ArrayList<>();
    private static int n;
    private static ArrayList<Double> errors = new ArrayList<>();

    public static void main(String[] args) throws InterruptedException, IOException, ClassNotFoundException {
        for (int i = 0; i < args.length; ++i) {
            if (args[i].equals("--inputPath")) {
                inputPath = args[++i];
            } else if (args[i].equals("--centroidPath")) {
                centroidPath = args[++i];
            } else if (args[i].equals("--outputScheme")) {
                outputScheme = args[++i];
            } else if (args[i].equals("--norm")) {
                norm = Integer.parseInt(args[++i]);
            } else if (args[i].equals("-k")) {
                k = Integer.parseInt(args[++i]);
            } else if (args[i].equals("-n")) {
                n = Integer.parseInt(args[++i]);
            } else {
                throw new IllegalArgumentException("Illegal cmd line arguement");
            }
        }
        System.out.println("k:" + k);
        Path cPath = new Path(centroidPath);

        if (inputPath == null || centroidPath == null || outputScheme == null) {
            throw new RuntimeException("Either outputpath or input path are not defined");
        }

        Configuration conf = new Configuration();
        conf.set("mapred.textoutputformat.separator", ",");
        conf.set("mapreduce.job.queuename", "eecs476");         // required for this to work on GreatLakes
        conf.setInt("norm", norm);
        conf.setInt("k",k);
        //job 1
        Job job = Job.getInstance(conf, "job");
        job.setJarByClass(step4_Kmeans.class);

        job.addCacheFile(cPath.toUri());

        MultipleInputs.addInputPath(job, new Path(inputPath), TextInputFormat.class, job_mapper1.class);
        MultipleInputs.addInputPath(job, new Path(centroidPath), TextInputFormat.class, job_mapper2.class);

        job.setReducerClass(job_reducer.class);

        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(Text.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        FileOutputFormat.setOutputPath(job, new Path(outputScheme + "1"));
        job.waitForCompletion(true);
        int i = 1;
        for (i = 1; i < n; i++) {
            job = Job.getInstance(conf, "job");
            job.setJarByClass(step4_Kmeans.class);
            cPath = new Path(outputScheme + i + "/part-r-00000");
            job.addCacheFile(cPath.toUri());

            MultipleInputs.addInputPath(job, new Path(inputPath), TextInputFormat.class, job_mapper1.class);
            MultipleInputs.addInputPath(job, new Path(outputScheme + i), TextInputFormat.class, job_mapper2.class);

            job.setReducerClass(job_reducer.class);

            job.setMapOutputKeyClass(Text.class);
            job.setMapOutputValueClass(Text.class);

            job.setOutputKeyClass(Text.class);
            job.setOutputValueClass(Text.class);

            FileOutputFormat.setOutputPath(job, new Path(outputScheme + (i+1)));
            job.waitForCompletion(true);
            if (errors.get(errors.size() - 1).equals(errors.get(errors.size() - 2))) {
                break;
            }
        }
        Job job2 = Job.getInstance(conf, "job");
        job2.setJarByClass(step4_Kmeans.class);

        job2.addCacheFile(cPath.toUri());

        MultipleInputs.addInputPath(job2, new Path(inputPath), TextInputFormat.class, job2_mapper1.class);
        MultipleInputs.addInputPath(job2, new Path(outputScheme + i), TextInputFormat.class, job2_mapper2.class);

        job2.setReducerClass(job2_reducer.class);

        job2.setMapOutputKeyClass(Text.class);
        job2.setMapOutputValueClass(Text.class);

        job2.setOutputKeyClass(Text.class);
        job2.setOutputValueClass(Text.class);

        FileOutputFormat.setOutputPath(job2, new Path(outputScheme + "40"));
        job2.waitForCompletion(true);

        System.out.println(errors.get(errors.size() - 1));
    }
}

