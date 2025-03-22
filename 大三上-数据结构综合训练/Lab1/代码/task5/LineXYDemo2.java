package task5;

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

public class LineXYDemo2 extends ApplicationFrame {
    public LineXYDemo2(String title, task5.Quicksort[] algorithms, int[] dataSizes, int testIterations) {
        super(title);
        XYDataset dataset = createDatasetForDepth(algorithms, dataSizes, testIterations);
        JFreeChart chart = createChartForDepth(dataset);
        ChartPanel chartPanel = new ChartPanel(chart);
        chartPanel.setPreferredSize(new Dimension(1500, 500));
        setContentPane(chartPanel);
    }

    private JFreeChart createChartForDepth(XYDataset dataset) {
        JFreeChart chart = ChartFactory.createXYLineChart(
                "Quicksort Recursive Depth",
                "log2(N)",
                "Depth",
                dataset,
                PlotOrientation.VERTICAL,
                true,
                false,
                false
        );

        chart.setBackgroundPaint(Color.WHITE);
        XYPlot plot = (XYPlot) chart.getPlot();
        NumberAxis rangeAxis = (NumberAxis) plot.getRangeAxis();
        rangeAxis.setRange(0, rangeAxis.getUpperBound());

        plot.setBackgroundPaint(Color.lightGray);
        plot.setAxisOffset(new RectangleInsets(5.0, 5.0, 5.0, 6.0));
        plot.setDomainGridlinePaint(Color.WHITE);
        plot.setRangeGridlinePaint(Color.WHITE);
        XYLineAndShapeRenderer renderer = (XYLineAndShapeRenderer) plot.getRenderer();
        renderer.setDefaultShapesVisible(true);
        renderer.setDefaultShapesFilled(true);
        return chart;
    }

    private XYDataset createDatasetForDepth(task5.Quicksort[] algorithms, int[] dataSizes, int testIterations) {
        XYSeriesCollection dataset = new XYSeriesCollection();

        for (task5.Quicksort algorithm : algorithms) {
            XYSeries series = new XYSeries(algorithm.getClass().getSimpleName() + algorithm.gap);
            for (int dataSize : dataSizes) {
                double maxDepth = getMaxDepth(algorithm, dataSize, testIterations);
                series.add(Math.log(dataSize) / Math.log(2), maxDepth);
            }
            dataset.addSeries(series);
        }

        return dataset;
    }

    private double getMaxDepth(task5.Quicksort algorithm, int dataSize, int testIterations) {
        double maxDepth = 0;
        for (int i = 0; i < testIterations; i++) {
            Comparable[] array = GenerateData.getInversedData(dataSize);
            algorithm.sort(array);
            int depth = algorithm.getMaxDepth();
            if (depth > maxDepth) {
                maxDepth = depth;
            }
            algorithm.resetDepth();
        }
        return maxDepth;
    }

    public static void main(String[] args) {
        Quicksort[] algorithms = {new Quicksort()};

        int[] dataSizes = new int[9];
        for (int i = 8; i <= 16; i++) {
            dataSizes[i - 8] = (int) Math.pow(2, i);
        }

        int testIterations = 50;
        LineXYDemo2 demo = new LineXYDemo2("Quicksort Recursive Depth", algorithms, dataSizes, testIterations);
        demo.pack();
        demo.setVisible(true);
    }
}