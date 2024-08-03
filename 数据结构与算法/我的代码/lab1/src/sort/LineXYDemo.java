package sort;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.NumberAxis;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.chart.plot.XYPlot;
import org.jfree.chart.renderer.xy.XYLineAndShapeRenderer;
import org.jfree.chart.ui.ApplicationFrame;
import org.jfree.chart.ui.RectangleInsets;
import org.jfree.data.xy.XYDataset;
import org.jfree.data.xy.XYSeries;
import org.jfree.data.xy.XYSeriesCollection;

import java.awt.*;

public class LineXYDemo extends ApplicationFrame {
    // 该构造方法中完成了数据集、图表对象和显示图表面板的创建工作
    public LineXYDemo(String title, SortAlgorithm[] algorithms, int[] dataSizes, int testIterations) {
        super(title);
        XYDataset dataset = createDataset(algorithms, dataSizes, testIterations);             // 创建记录图中坐标点的数据集
        JFreeChart chart = createChart(dataset);         // 使用上一步已经创建好的数据集生成一个图表对象
        ChartPanel chartPanel = new ChartPanel(chart);   // 将上一步已经创建好的图表对象放置到一个可以显示的Panel上
        // 设置GUI面板Panel的显示大小
        chartPanel.setPreferredSize(new Dimension(1500, 500));
        setContentPane(chartPanel);                      // 这是JavaGUI的步骤之一，不用过于关心，面向对象课程综合训练的视频中进行了讲解。
    }

    public LineXYDemo(String title, Quicksort[] algorithms, int[] dataSizes, int testIterations) {
        super(title);
        XYDataset dataset = createDatasetNewQuick(algorithms, dataSizes, testIterations);             // 创建记录图中坐标点的数据集
        JFreeChart chart = createChart(dataset);         // 使用上一步已经创建好的数据集生成一个图表对象
        ChartPanel chartPanel = new ChartPanel(chart);   // 将上一步已经创建好的图表对象放置到一个可以显示的Panel上
        // 设置GUI面板Panel的显示大小
        chartPanel.setPreferredSize(new Dimension(1500, 500));
        setContentPane(chartPanel);                      // 这是JavaGUI的步骤之一，不用过于关心，面向对象课程综合训练的视频中进行了讲解。
    }

    public LineXYDemo(String title, Quicksort[] algorithms, double[] dataScales, int testIterations) {
        super(title);
        XYDataset dataset = createDatasetForOptimizedQuickRepeat(algorithms, dataScales, testIterations);             // 创建记录图中坐标点的数据集
        JFreeChart chart = createChartRepeat(dataset);         // 使用上一步已经创建好的数据集生成一个图表对象
        ChartPanel chartPanel = new ChartPanel(chart);   // 将上一步已经创建好的图表对象放置到一个可以显示的Panel上
        // 设置GUI面板Panel的显示大小
        chartPanel.setPreferredSize(new Dimension(1500, 500));
        setContentPane(chartPanel);                      // 这是JavaGUI的步骤之一，不用过于关心，面向对象课程综合训练的视频中进行了讲解。
    }

    private JFreeChart createChart(XYDataset dataset) {
        // 使用已经创建好的dataset生成图表对象
        // JFreechart提供了多种类型的图表对象，本次实验是需要使用XYLine型的图表对象
        JFreeChart chart = ChartFactory.createXYLineChart(
                "Sorting Algorithm Performance",      // 图表的标题
                "Data Size",                           // 横轴的标题名
                "Time (nanoseconds)",                           // 纵轴的标题名
                dataset,                       // 图表对象中使用的数据集对象
                PlotOrientation.VERTICAL,      // 图表显示的方向
                true,                          // 是否显示图例
                false,                         // 是否需要生成tooltips
                false                          // 是否需要生成urls
        );
        // 下面所做的工作都是可选操作，主要是为了调整图表显示的风格
        // 同学们不必在意下面的代码
        // 可以将下面的代码去掉对比一下显示的不同效果
        chart.setBackgroundPaint(Color.WHITE);
        XYPlot plot = (XYPlot) chart.getPlot();

        NumberAxis rangeAxis = (NumberAxis) plot.getRangeAxis();
        rangeAxis.setRange(4, rangeAxis.getUpperBound()); // 设置纵轴的起始值为 4.0


        plot.setBackgroundPaint(Color.lightGray);
        plot.setAxisOffset(new RectangleInsets(5.0, 5.0, 5.0, 6.0));
        plot.setDomainGridlinePaint(Color.WHITE);
        plot.setRangeGridlinePaint(Color.WHITE);
        XYLineAndShapeRenderer renderer = (XYLineAndShapeRenderer) plot.getRenderer();
        renderer.setDefaultShapesVisible(true);
        renderer.setDefaultShapesFilled(true);
        return chart;
    }

    private JFreeChart createChartRepeat(XYDataset dataset) {
        // 使用已经创建好的dataset生成图表对象
        // JFreechart提供了多种类型的图表对象，本次实验是需要使用XYLine型的图表对象
        JFreeChart chart = ChartFactory.createXYLineChart(
                "Sorting Algorithm Performance",      // 图表的标题
                "Repetition rate",                           // 横轴的标题名
                "Time (nanoseconds)",                           // 纵轴的标题名
                dataset,                       // 图表对象中使用的数据集对象
                PlotOrientation.VERTICAL,      // 图表显示的方向
                true,                          // 是否显示图例
                false,                         // 是否需要生成tooltips
                false                          // 是否需要生成urls
        );
        // 下面所做的工作都是可选操作，主要是为了调整图表显示的风格
        // 同学们不必在意下面的代码
        // 可以将下面的代码去掉对比一下显示的不同效果
        chart.setBackgroundPaint(Color.WHITE);
        XYPlot plot = (XYPlot) chart.getPlot();

        NumberAxis rangeAxis = (NumberAxis) plot.getRangeAxis();
        rangeAxis.setRange(4, rangeAxis.getUpperBound()); // 设置纵轴的起始值为 4.0


        plot.setBackgroundPaint(Color.lightGray);
        plot.setAxisOffset(new RectangleInsets(5.0, 5.0, 5.0, 6.0));
        plot.setDomainGridlinePaint(Color.WHITE);
        plot.setRangeGridlinePaint(Color.WHITE);
        XYLineAndShapeRenderer renderer = (XYLineAndShapeRenderer) plot.getRenderer();
        renderer.setDefaultShapesVisible(true);
        renderer.setDefaultShapesFilled(true);
        return chart;
    }

    private XYDataset createDatasetNew(SortAlgorithm[] algorithms, int[] dataSizes, int testIterations) {
        XYSeriesCollection dataset = new XYSeriesCollection();

        for (SortAlgorithm algorithm : algorithms) {
            XYSeries series = new XYSeries(algorithm.getClass().getSimpleName());
            for (int dataSize : dataSizes) {
                double averageTime = (SortTest.testForRandom(algorithm, dataSize, testIterations));
                //将横坐标做二的对数间隔（log2）；纵坐标作十的对数间隔处理（lg）
                series.add(Math.log(dataSize) / Math.log(2), Math.log10(averageTime));
            }
            dataset.addSeries(series);
        }
        for (SortAlgorithm algorithm : algorithms) {
            XYSeries series = new XYSeries(algorithm.getClass().getSimpleName() + "Uneven");
            for (int dataSize : dataSizes) {
                double averageTime = (SortTest.testForRandomSome(algorithm, dataSize, testIterations));
                //将横坐标做二的对数间隔（log2）；纵坐标作十的对数间隔处理（lg）
                series.add(Math.log(dataSize) / Math.log(2), Math.log10(averageTime));
            }
            dataset.addSeries(series);
        }

        return dataset;
    }

    private XYDataset createDatasetNewQuick(Quicksort[] algorithms, int[] dataSizes, int testIterations) {
        XYSeriesCollection dataset = new XYSeriesCollection();

        for (Quicksort algorithm : algorithms) {
            XYSeries series = new XYSeries(algorithm.getClass().getSimpleName() + algorithm.gap);
            for (int dataSize : dataSizes) {
                double averageTime = (SortTest.testForRandom(algorithm, dataSize, testIterations));
                //将横坐标取 log2；纵坐标取 lg
                series.add(Math.log(dataSize) / Math.log(2), Math.log10(averageTime));
            }
            dataset.addSeries(series);
        }
        for (Quicksort algorithm : algorithms) {
            XYSeries series = new XYSeries(algorithm.getClass().getSimpleName() + algorithm.gap + "Uneven");
            for (int dataSize : dataSizes) {
                double averageTime = (SortTest.testForRandomSome(algorithm, dataSize, testIterations));
                //将横坐标取 log2；纵坐标取 lg
                series.add(Math.log(dataSize) / Math.log(2), Math.log10(averageTime));
            }
            dataset.addSeries(series);
        }

        return dataset;
    }

    private XYDataset createDataset(SortAlgorithm[] algorithms, int[] dataSizes, int testIterations) {
        XYSeriesCollection dataset = new XYSeriesCollection();

        for (SortAlgorithm algorithm : algorithms) {
            XYSeries series = new XYSeries(algorithm.getClass().getSimpleName());
            for (int dataSize : dataSizes) {
                Double[] data = GenerateData.getSortedData(dataSize);
                double averageTime = (SortTest.testForAcsending(algorithm, dataSize, testIterations));
                //将横坐标做二的对数间隔（log2）；纵坐标作十的对数间隔处理（lg）
                series.add(Math.log(dataSize) / Math.log(2), Math.log10(averageTime));
            }
            dataset.addSeries(series);
        }

        return dataset;
    }

    private XYDataset createDatasetForOptimizedQuickRepeat(Quicksort[] algorithms, double[] dataScales, int testIterations) {
        XYSeriesCollection dataset = new XYSeriesCollection();

        for (Quicksort algorithm : algorithms) {
            XYSeries series = new XYSeries((algorithm.getClass().getSimpleName()) + algorithm.gap);
            for (double dataScale : dataScales) {
                double averageTime = (SortTest.testForRandomRepeat(algorithm, (int) Math.pow(2, 16), testIterations, dataScale));
                //将横坐标取 log2；纵坐标取 lg
                series.add(dataScale, Math.log10(averageTime));
            }
            dataset.addSeries(series);
        }

        return dataset;
    }


    public static void main(String[] args) {

    /*
        //绘制五条图线，包括插入排序，选择排序，希尔排序，快速排序以及归并排序）
        SortAlgorithm[] algorithms = {new Insertion(), new Selection(), new Shell(), new Quicksort(), new Mergesort()};
        //横坐标取2的八次方到16次方共9个数
        int[] dataSizes = new int[9];
        for (int i = 8; i <= 16; i++) {
            dataSizes[i - 8] = (int) Math.pow(2, i);
        }
        int testIterations = 20;
        LineXYDemo demo = new LineXYDemo("Sorting Algorithm Performance", algorithms, dataSizes, testIterations);
        demo.pack();
        demo.setVisible(true);
    }
    */
    /*
        //绘制五条图线，包括未优化 与 阈值为3,7,15,31的优化快速排序算法
        Quicksort[] algorithms = new Quicksort[5];
        algorithms[0] = new Quicksort();
        int j = 1;
        for (int i = 2; i < 6; i++) {
            algorithms[j++] = new QuicksortO((int) Math.pow(2, i) - 1);
        }

        //重复率
        double[] dataScales = new double[4];
        dataScales[0] = 0.5;
        dataScales[1] = 0.6;
        dataScales[2] = 0.8;
        dataScales[3] = 1.0;

        //横坐标取2的八次方到16次方共9个数
        int[] dataSizes = new int[9];
        for (int i = 8; i <= 16; i++) {
            dataSizes[i - 8] = (int) Math.pow(2, i);
        }

        int testIterations = 20;
        LineXYDemo demo = new LineXYDemo("Sorting Algorithm Performance", algorithms, dataSizes, testIterations);
        demo.pack();
        demo.setVisible(true);
    */
        /*
        //绘制五条图线，包括未优化 与 阈值为3,7,15,31的优化快速排序算法
        Quicksort[] algorithms = new Quicksort[5];
        algorithms[0] = new Quicksort();
        int j = 1;
        for (int i = 2; i <= 5; i++) {
            algorithms[j++] = new QuicksortO((int) Math.pow(2, i) - 1);
        }

        //重复率
        double[] RepetitionRate = new double[4];
        RepetitionRate[0] = 0.5;
        RepetitionRate[1] = 0.6;
        RepetitionRate[2] = 0.8;
        RepetitionRate[3] = 1.0;

        int testIterations = 20;
        LineXYDemo demo = new LineXYDemo("Sorting Algorithm Performance", algorithms, RepetitionRate, testIterations);
        demo.pack();
        demo.setVisible(true);
    */

        //绘制五条图线，包括未优化 与 阈值为3,7,15,31的优化快速排序算法
        Quicksort[] algorithms = new Quicksort[5];
        algorithms[0] = new Quicksort();
        int j = 1;
        for (int i = 2; i <= 5; i++) {
            algorithms[j++] = new QuicksortOO((int) Math.pow(2, i) - 1);
        }

        //重复率
        double[] RepetitionRate = new double[4];
        RepetitionRate[0] = 0.5;
        RepetitionRate[1] = 0.6;
        RepetitionRate[2] = 0.8;
        RepetitionRate[3] = 1.0;

        int testIterations = 20;
        LineXYDemo demo = new LineXYDemo("Sorting Algorithm Performance", algorithms, RepetitionRate, testIterations);
        demo.pack();
        demo.setVisible(true);


    /*
        Quicksort[] algorithms = new Quicksort[3];
        algorithms[0] = new Quicksort();
        algorithms[1] = new QuicksortO(7);
        algorithms[2] = new QuicksortOO(7);

        //重复率
        double[] RepetitionRate = new double[4];
        RepetitionRate[0] = 0.5;
        RepetitionRate[1] = 0.6;
        RepetitionRate[2] = 0.8;
        RepetitionRate[3] = 1.0;

        int testIterations = 20;
        LineXYDemo demo = new LineXYDemo("Sorting Algorithm Performance", algorithms, RepetitionRate, testIterations);
        demo.pack();
        demo.setVisible(true);

     */
    }
}


