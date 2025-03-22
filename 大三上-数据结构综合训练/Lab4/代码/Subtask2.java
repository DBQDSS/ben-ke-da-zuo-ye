import java.util.*;
import java.io.*;

public class Subtask2 {
    public static void main(String[] args) {
        WordLadderGraph graph = new WordLadderGraph();
        List<String> words = new ArrayList<>();

        // 读取 words5.txt 文件
        try (Scanner scanner = new Scanner(new File("words5.txt"))) {
            while (scanner.hasNextLine()) {
                words.add(scanner.nextLine().trim());
            }
        } catch (FileNotFoundException e) {
            System.err.println("文件 words5.txt 未找到！");
            return;
        }

        // 构建图
        graph.buildGraph(words);

        // 选择两个可连接的单词
        List<String> wordList = new ArrayList<>(graph.getAdjacencyList().keySet());
        Random random = new Random();
        String startWord, endWord;
        do {
            startWord = wordList.get(random.nextInt(wordList.size()));
            endWord = wordList.get(random.nextInt(wordList.size()));
        } while (!graph.isPathExist(startWord, endWord));

        // 交互式游戏
        Scanner inputScanner = new Scanner(System.in);
        System.out.println("开始单词：" + startWord);
        System.out.println("目标单词：" + endWord);
        System.out.println("请依次输入单词（输入“我不会”查看答案）：");

        String currentWord = startWord;
        boolean success = false;
        while (true) {
            String userInput = inputScanner.nextLine().trim();

            // 检查用户是否请求显示答案
            if (userInput.equals("我不会")) {
                List<String> solutionPath = findShortestPath(graph, startWord, endWord);
                System.out.println("正确答案路径：" + solutionPath);
                break;
            }

            // 检查输入是否合法
            if (!words.contains(userInput)) {
                System.out.println("无效输入，您输入的单词不在 words5 中！");
            } else if (graph.isOneLetterDifference(currentWord, userInput)) {
                currentWord = userInput;
                if (currentWord.equals(endWord)) {
                    System.out.println("恭喜你成功完成字梯！");
                    success = true;
                    break;
                } else {
                    System.out.println("继续输入下一个单词...");
                }
            } else {
                System.out.println("无效输入，请确保单词仅差一个字母！");
            }
        }
        if (!success) {
            System.out.println("游戏结束！");
        }
        inputScanner.close();
    }

    // 使用广度优先搜索（BFS）查找最短路径
    private static List<String> findShortestPath(WordLadderGraph graph, String startWord, String endWord) {
        Map<String, String> previous = new HashMap<>();
        Queue<String> queue = new LinkedList<>();
        Set<String> visited = new HashSet<>();

        queue.offer(startWord);
        visited.add(startWord);

        while (!queue.isEmpty()) {
            String current = queue.poll();
            if (current.equals(endWord)) {
                break;
            }
            for (String neighbor : graph.getAdjacencyList().get(current)) {
                if (!visited.contains(neighbor)) {
                    visited.add(neighbor);
                    previous.put(neighbor, current);
                    queue.offer(neighbor);
                }
            }
        }

        // 生成路径
        List<String> path = new LinkedList<>();
        for (String at = endWord; at != null; at = previous.get(at)) {
            path.add(0, at);
        }
        return path;
    }
}
