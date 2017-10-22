package bigdata;

import org.apache.commons.io.FileUtils;
import org.apache.commons.io.IOUtils;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaDoubleRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.canova.api.records.reader.RecordReader;
import org.canova.api.records.reader.impl.CSVRecordReader;
import org.deeplearning4j.nn.api.OptimizationAlgorithm;
import org.deeplearning4j.nn.conf.MultiLayerConfiguration;
import org.deeplearning4j.nn.conf.NeuralNetConfiguration;
import org.deeplearning4j.nn.conf.layers.DenseLayer;
import org.deeplearning4j.nn.conf.layers.FeedForwardLayer;
import org.deeplearning4j.nn.conf.layers.OutputLayer;
import org.deeplearning4j.nn.multilayer.MultiLayerNetwork;
import org.deeplearning4j.nn.weights.WeightInit;
import org.deeplearning4j.spark.canova.RecordReaderFunction;
import org.deeplearning4j.spark.impl.multilayer.SparkDl4jMultiLayer;
import org.nd4j.linalg.dataset.DataSet;
import org.nd4j.linalg.io.ClassPathResource;
import org.nd4j.linalg.lossfunctions.LossFunctions;
import org.deeplearning4j.eval.Evaluation;
import org.apache.spark.mllib.linalg.DenseMatrix;
import org.apache.spark.mllib.linalg.Matrix;
import org.apache.spark.mllib.linalg.DenseVector;
import org.apache.spark.mllib.linalg.Vector;
import java.util.Random;
import java.io.PrintWriter;

import java.io.File;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.io.FileInputStream;

public class Train
{
	public static void main(String[] args)
		throws Exception
	{
		// Fetch parameters
		String trainFile;
		String testFile;
		String outputPath;
		{
			if (args.length != 3) {
				usage();
				throw new Exception();
			}
			trainFile = args[0];
			testFile = args[1];
			outputPath = args[2];
		}

		// Load the training and testing data
		SparkConf conf = new SparkConf().setAppName("bigdata_musiclassifier").setMaster("local[*]");
                JavaSparkContext sc = new JavaSparkContext(conf);

		JavaRDD<DataSet> trainingData = readCSVWithOversampling(sc, trainFile);
		JavaRDD<DataSet> testingData = readCSV(sc, testFile);
		Matrix matrix = readCSVFeature(testFile);

		// Create a MLP
		MultiLayerConfiguration mlpConf = new NeuralNetConfiguration.Builder()
			.seed(12345)
			.iterations(800)
			.optimizationAlgo(OptimizationAlgorithm.CONJUGATE_GRADIENT)
			//.optimizationAlgo(OptimizationAlgorithm.STOCHASTIC_GRADIENT_DESCENT )
			//.learningRate(1e-5)
			//.l1(0.01).regularization(true).l2(1e-3)
			.list(4)
			.layer(0, new DenseLayer.Builder().nIn(32).nOut(256)
			        .activation("relu")
			        //.weightInit(WeightInit.XAVIER)
			        .weightInit(WeightInit.NORMALIZED)
				//.dropOut(0.2)
			        .build())
			.layer(1, new DenseLayer.Builder().nIn(256).nOut(128)
			        .activation("relu")
			        .weightInit(WeightInit.XAVIER)
			        //.weightInit(WeightInit.NORMALIZED)
				//.dropOut(0.2)
			        .build())
			.layer(2, new DenseLayer.Builder().nIn(128).nOut(64)
			        .activation("relu")
			        .weightInit(WeightInit.XAVIER)
			        //.weightInit(WeightInit.NORMALIZED)
				//.dropOut(0.2)
			        .build())
			.layer(3, new OutputLayer.Builder(LossFunctions.LossFunction.MCXENT)
			        .weightInit(WeightInit.XAVIER)
			        .activation("softmax")
			        .nIn(64).nOut(15).build())
			.backprop(true).pretrain(false)
			.build();

		MultiLayerNetwork net = new MultiLayerNetwork(mlpConf);
		net.init();
		net.setUpdater(null);
		SparkDl4jMultiLayer sparkNetwork = new SparkDl4jMultiLayer(sc,net);

		// Train
		for (int i = 0; i < 1; i++) {
		        MultiLayerNetwork network = sparkNetwork.fitDataSet(trainingData);
			sparkNetwork = new SparkDl4jMultiLayer(sc, network);
			Evaluation trainingEval = sparkNetwork.evaluate(trainingData);
			//JavaDoubleRDD temp = sparkNetwork.scoreExamples(trainingData, false);
			//temp.saveAsTextFile("temp"); 
			Evaluation testingEval = sparkNetwork.evaluate(testingData); 
			//Vector result = sparkNetwork.predict(new DenseVector(new double[] {0.0,140.69506,0.311,0.0,0.811,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,-12.361,0.0,0.848,5,7.72606,99.66,0.0,0.0,0.0,0.0,0.0,0.757,0.0,0.0,0.0,0.0}));
			//System.err.println(result.toString());
			//System.err.println("Epoch = " + i + ", Training Score = " + trainingEval.confusionToString() + ", Testing Score = " + testingEval.confusionToString());
			System.err.println("Epoch = " + i + ", Training Score = " + trainingEval.accuracy() + ", Testing Score = " + testingEval.accuracy());
			System.gc();
		}
		Matrix outputMatrix = sparkNetwork.predict(matrix);
		PrintWriter writer = new PrintWriter(outputPath, "UTF-8");
		for (int i = 0; i < outputMatrix.numRows(); i++) {
			for (int j = 0; j < outputMatrix.numCols() - 1; j++) {
				writer.print(outputMatrix.apply(i, j) + ",");
			}
			writer.print(outputMatrix.apply(i, outputMatrix.numCols() - 1));
			writer.print("\n");
		}
		writer.close();
		
	}

	private static void usage()
	{
		System.out.println("Usage: java Train <Training File> <Testing File> <Output Path>");
	}

	private static JavaRDD<DataSet> readCSV(final JavaSparkContext sc, String filename) 
		throws Exception
	{
		RecordReader recordReader = new CSVRecordReader(0, ",");
		ClassPathResource classPathResource = new ClassPathResource(filename);
		String inputStr = IOUtils.toString(classPathResource.getInputStream());

		String[] lines = inputStr.split("\n");
		List<String> linesList = Arrays.asList(Arrays.copyOfRange(lines, 1, lines.length - 1));
		for (int i = 0; i < linesList.size(); i++) {
			String linesListElement = linesList.get(i);
			int j;
			for (j = 0; j < linesListElement.length(); j++) {
				if (linesListElement.charAt(j) == ',')
					break;
			}
			linesList.set(i, new String(linesListElement.getBytes(), j + 1, 
				linesListElement.length() - (j + 1)));
		}
		JavaRDD<String> dataLines = sc.parallelize(linesList);
		JavaRDD<DataSet> result = dataLines.map(new RecordReaderFunction(recordReader, 32, 15));

		return result;
	}

	private static Matrix readCSVFeature(final String filename)
		throws Exception
	{
		ClassPathResource classPathResource = new ClassPathResource(filename);
		String inputStr = IOUtils.toString(classPathResource.getInputStream());

		String[] lines = inputStr.split("\n");
		double[] values = new double[(lines.length - 1) * 32];
		for (int i = 1; i < lines.length; i++) {
			String[] col = lines[i].split(",");
			for (int j = 1; j <= 32; j++) {
				values[(i - 1) * 32 + (j - 1)] = Double.parseDouble(col[j]);
			}
		}
		
		return new DenseMatrix(lines.length - 1, 32, values);
	} 

	private static JavaRDD<DataSet> readCSVWithOversampling(final JavaSparkContext sc, String filename) 
		throws Exception
	{
		RecordReader recordReader = new CSVRecordReader(0, ",");
		ClassPathResource classPathResource = new ClassPathResource(filename);
		String inputStr = IOUtils.toString(classPathResource.getInputStream());

		String[] lines = inputStr.split("\n");
		List<String> linesList = Arrays.asList(Arrays.copyOfRange(lines, 1, lines.length - 1));
		int [] labelCount = new int[15];
		int count = 0;
		for (int i = 0; i < linesList.size(); i++) {
			String linesListElement = linesList.get(i);
			int j;
			for (j = 0; j < linesListElement.length(); j++) {
				if (linesListElement.charAt(j) == ',')
					break;
			}
			linesList.set(i, new String(linesListElement.getBytes(), j + 1, 
				linesListElement.length() - (j + 1)));

			for (j = linesListElement.length() - 1; j >= 0; j--) {
				if (linesListElement.charAt(j) == ',')
					break;
			}
			
			labelCount[Integer.parseInt(linesListElement.substring(j + 1))]++;
			count++;
		}
		
		double [] prob = new double[15];
		for (int i = 0; i < 15; i++) {
			prob[i] = (double)count / (double)labelCount[i] * 1.3 / 100.0;
		}

		List<String> newLinesList = new ArrayList<String>();
		Random random = new Random();
		for (int i = 0; i < 10; i++) {
			for (String line : linesList) {
				int j;
				for (j = line.length() - 1; j >= 0; j--) {
					if (line.charAt(j) == ',')
						break;
				}
				int label = Integer.parseInt(line.substring(j + 1));
				if (random.nextFloat() < prob[label])
					newLinesList.add(line);
			}
		}

		JavaRDD<String> dataLines = sc.parallelize(newLinesList);
		JavaRDD<DataSet> result = dataLines.map(new RecordReaderFunction(recordReader, 32, 15));

		return result;
	} 
}
