import java.io.*;
import java.util.*;

public class Subtask1 {
    public static void main(String[] args) {
        WordLadderGraph graph = new WordLadderGraph();
        List<String> words = new ArrayList<>();

        // 读取 words5.txt 文件
        try (BufferedReader br = new BufferedReader(new FileReader("words5.txt"))) {
            String line;
            while ((line = br.readLine()) != null) {
                words.add(line.trim());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        // 构建图
        graph.buildGraph(words);

        // 生成无法连接的单词列表
        try (BufferedWriter writer = new BufferedWriter(new FileWriter("noladder.txt"))) {
            for (String word : graph.getAdjacencyList().keySet()) {
                if (graph.getAdjacencyList().get(word).isEmpty()) {
                    writer.write(word);
                    writer.newLine();
                }
            }
            System.out.println("noladder.txt 文件生成完毕！");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
