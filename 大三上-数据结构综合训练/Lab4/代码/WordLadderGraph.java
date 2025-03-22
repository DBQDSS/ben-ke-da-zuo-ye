import java.util.*;

public class WordLadderGraph {

    private Map<String, List<String>> adjacencyList;

    public WordLadderGraph() {
        this.adjacencyList = new HashMap<>();
    }

    public void addWord(String word) {
        adjacencyList.putIfAbsent(word, new ArrayList<>());
    }

    public void addEdge(String word1, String word2) {
        if (isOneLetterDifference(word1, word2)) {
            adjacencyList.get(word1).add(word2);
            adjacencyList.get(word2).add(word1);
        }
    }

    public boolean isOneLetterDifference(String word1, String word2) {
        if (word1.length() != word2.length()) return false;
        int differences = 0;
        for (int i = 0; i < word1.length(); i++) {
            if (word1.charAt(i) != word2.charAt(i)) {
                differences++;
                if (differences > 1) return false;
            }
        }
        return differences == 1;
    }

    public void buildGraph(List<String> words) {
        for (String word : words) {
            addWord(word);
        }
        for (String word1 : words) {
            for (String word2 : words) {
                if (!word1.equals(word2)) {
                    addEdge(word1, word2);
                }
            }
        }
    }

    public Map<String, List<String>> getAdjacencyList() {
        return adjacencyList;
    }

    public boolean isPathExist(String startWord, String endWord) {
        Set<String> visited = new HashSet<>();
        Queue<String> queue = new LinkedList<>();
        queue.offer(startWord);
        while (!queue.isEmpty()) {
            String current = queue.poll();
            if (current.equals(endWord)) return true;
            visited.add(current);
            for (String neighbor : adjacencyList.get(current)) {
                if (!visited.contains(neighbor)) {
                    queue.offer(neighbor);
                }
            }
        }
        return false;
    }
}
