
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
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
    public LineXYDemo(String title){
        super(title);
        XYDataset dataset = createDataset();             // 创建记录图中坐标点的数据集
        JFreeChart chart = createChart(dataset);         // 使用上一步已经创建好的数据集生成一个图表对象
        ChartPanel chartPanel = new ChartPanel(chart);   // 将上一步已经创建好的图表对象放置到一个可以显示的Panel上
        // 设置GUI面板Panel的显示大小
        chartPanel.setPreferredSize(new Dimension(500, 270));
        setContentPane(chartPanel);                      // 这是JavaGUI的步骤之一，不用过于关心，面向对象课程综合训练的视频中进行了讲解。
    }

    private JFreeChart createChart(XYDataset dataset) {
        // 使用已经创建好的dataset生成图表对象
        // JFreechart提供了多种类型的图表对象，本次实验是需要使用XYLine型的图表对象
        JFreeChart chart = ChartFactory.createXYLineChart(
                "LineXY Chart Demo",      // 图表的标题
                "X",                           // 横轴的标题名
                "Y",                           // 纵轴的标题名
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
        XYPlot plot = (XYPlot)chart.getPlot();
        plot.setBackgroundPaint(Color.lightGray);
        plot.setAxisOffset(new RectangleInsets(5.0, 5.0, 5.0, 6.0));
        plot.setDomainGridlinePaint(Color.WHITE);
        plot.setRangeGridlinePaint(Color.WHITE);
        XYLineAndShapeRenderer renderer = (XYLineAndShapeRenderer) plot.getRenderer();
        renderer.setDefaultShapesVisible(true);
        renderer.setDefaultShapesFilled(true);
        return chart;
    }

    private XYDataset createDataset() {
        // 本样例中想要显示的是三组数据的变化图
        // X数组是三组数据共同拥有的x坐标值；Y1、Y2和Y3数组分别存储了三组数据对应的y坐标值
        double[] X = {1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0};
        double[] Y1 = {1.0, 4.0, 3.0, 5.0, 5.0, 7.0, 7.0, 8.0};
        double[] Y2 = {5.0, 7.0, 6.0, 8.0, 4.0, 4.0, 2.0, 1.0};
        double[] Y3 = {10.0, 11.8, 8.9, 3.5, 8.8, 9.0, 3.1, 0.0};
        double[][] Y = {Y1, Y2, Y3};
        // jfreechart中使用XYSeries对象存储一组数据的(x,y)的序列，因为有三组数据所以创建三个XYSeries对象
        XYSeries[] series = {new XYSeries("First"), new XYSeries("Second"), new XYSeries("Third")};
        int N = X.length;
        int M = series.length;
        for(int i = 0; i < M; i++)
            for(int j = 0; j < N; j++)
                series[i].add(X[j], Y[i][j]);
        // 因为在该图表中显示的数据序列不止一组，所以在jfreechart中需要将多组数据序列存放到一个XYSeriesCollection对象中
        XYSeriesCollection dataset = new XYSeriesCollection();
        for(int i = 0; i < M; i++)
            dataset.addSeries(series[i]);

        return dataset;
    }

    public static void main(String[] args) {
        LineXYDemo demo = new LineXYDemo("Demo");
        demo.pack();
        demo.setVisible(true);
    }
}
