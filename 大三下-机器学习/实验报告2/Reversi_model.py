import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from tqdm import tqdm
import matplotlib.pyplot as plt

# 设置设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# 将棋盘大小改为 8x8
BOARD_SIZE = 8

# 定义黑白棋游戏逻辑：棋盘、规则、落子执行
class ReversiGame:
    def __init__(self):
        self.board = self.init_board()
        self.current_player = 1  # 黑棋先行

    def init_board(self):
        board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        mid1 = BOARD_SIZE // 2 - 1
        mid2 = BOARD_SIZE // 2
        # 初始局面：中心四格，黑白对置（符合 8x8 标准局面）
        board[mid1, mid1] = -1
        board[mid1, mid2] = 1
        board[mid2, mid1] = 1
        board[mid2, mid2] = -1
        return board

    def get_valid_moves(self, board, player):
        moves = []
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i, j] == 0 and self.check_move(board, player, (i, j)):
                    moves.append((i, j))
        return moves

    def check_move(self, board, player, move):
        i, j = move
        valid = False
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                x, y = i + di, j + dj
                found_opponent = False
                while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
                    if board[x, y] == -player:
                        found_opponent = True
                    elif board[x, y] == player:
                        if found_opponent:
                            valid = True
                        break
                    else:
                        break
                    x += di
                    y += dj
        return valid

    def execute_move(self, board, player, move):
        new_board = board.copy()
        i, j = move
        new_board[i, j] = player
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                pieces_to_flip = []
                x, y = i + di, j + dj
                while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
                    if new_board[x, y] == -player:
                        pieces_to_flip.append((x, y))
                    elif new_board[x, y] == player:
                        for pos in pieces_to_flip:
                            new_board[pos] = player
                        break
                    else:
                        break
                    x += di
                    y += dj
        return new_board

    def is_terminal(self, board):
        # 当双方都无合法走子时结束
        if len(self.get_valid_moves(board, 1)) == 0 and len(self.get_valid_moves(board, -1)) == 0:
            return True
        return False

    def get_winner(self, board):
        black = np.sum(board == 1)
        white = np.sum(board == -1)
        if black > white:
            return 1
        elif white > black:
            return -1
        else:
            return 0

    def display_board(self, board):
        # 使用 matplotlib 显示棋盘状态（1：黑，-1：白，0：空）
        plt.figure(figsize=(4, 4))
        plt.imshow(board, cmap='gray_r')
        plt.xticks(range(BOARD_SIZE))
        plt.yticks(range(BOARD_SIZE))
        plt.show()


# 构建CNN（输出落子概率分布和局面估值）
class ReversiNNet(nn.Module):
    def __init__(self, board_size, dropout_p=0.3):
        super(ReversiNNet, self).__init__()
        self.board_size = board_size
        self.conv1 = nn.Conv2d(1, 64, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(128 * board_size * board_size, 256)
        self.fc_policy = nn.Linear(256, board_size * board_size)
        self.fc_value = nn.Linear(256, 1)
        self.dropout = nn.Dropout(p=dropout_p)

    def forward(self, x):
        # 输入 x: (batch, 1, board_size, board_size)
        x = F.relu(self.conv1(x))
        x = self.dropout(x)
        x = F.relu(self.conv2(x))
        x = self.dropout(x)
        x = x.view(-1, 128 * self.board_size * self.board_size)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        policy = self.fc_policy(x)  # 原始 logits
        value = torch.tanh(self.fc_value(x))
        return policy, value



# 实现 MCTS
class MCTSNode:
    def __init__(self, board, player, parent=None):
        self.board = board
        self.player = player
        self.parent = parent
        self.children = {}  # move -> child node
        self.visit_count = 0
        self.total_value = 0
        self.prior = 0


def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


class MCTS:
    def __init__(self, game, nnet, c_puct=1.0, num_simulations=200):
        self.game = game
        self.nnet = nnet
        self.c_puct = c_puct
        self.num_simulations = num_simulations
        self.Q = {}  # key: (node_id, move) -> Q值
        self.N = {}  # key: (node_id, move) -> 访问次数
        self.P = {}  # key: (node_id, move) -> 先验概率

    def search(self, node):
        if self.game.is_terminal(node.board):
            winner = self.game.get_winner(node.board)
            if winner == 0:
                return 0
            return 1 if winner == node.player else -1

        valid_moves = self.game.get_valid_moves(node.board, node.player)
        if not valid_moves:
            # 无合法走子则“过子”，转换玩家
            next_board = node.board.copy()
            child = MCTSNode(next_board, -node.player, parent=node)
            value = -self.search(child)
            return value

        if not node.children:
            # 扩展叶子节点
            board_tensor = torch.FloatTensor(node.board).unsqueeze(0).unsqueeze(0).to(device)
            policy_logits, value = self.nnet(board_tensor)
            policy_logits = policy_logits.detach().cpu().numpy().flatten()
            policy = np.zeros(BOARD_SIZE * BOARD_SIZE)
            for move in valid_moves:
                idx = move[0] * BOARD_SIZE + move[1]
                policy[idx] = np.exp(policy_logits[idx])
            if policy.sum() > 0:
                policy = policy / np.sum(policy)
            else:
                policy = np.ones(BOARD_SIZE * BOARD_SIZE) / (BOARD_SIZE * BOARD_SIZE)
            for move in valid_moves:
                next_board = self.game.execute_move(node.board, node.player, move)
                child_node = MCTSNode(next_board, -node.player, parent=node)
                node.children[move] = child_node
                key = (id(node), move)
                self.P[key] = policy[move[0] * BOARD_SIZE + move[1]]
                self.N[key] = 0
                self.Q[key] = 0
            return value.item()

        # 选择具有最大 UCB 值的走法
        best_score = -float('inf')
        best_move = None
        for move in valid_moves:
            key = (id(node), move)
            if self.N[key] > 0:
                u = self.Q[key] + self.c_puct * self.P[key] * np.sqrt(node.visit_count) / (1 + self.N[key])
            else:
                u = self.c_puct * self.P[key] * np.sqrt(node.visit_count + 1e-8)
            if u > best_score:
                best_score = u
                best_move = move

        child = node.children[best_move]
        value = -self.search(child)
        key = (id(node), best_move)
        self.N[key] += 1
        self.Q[key] = (self.Q[key] * (self.N[key] - 1) + value) / self.N[key]
        node.visit_count += 1
        return value

    def get_move_probabilities(self, root, temp=1):
        for _ in range(self.num_simulations):
            self.search(root)
        valid_moves = self.game.get_valid_moves(root.board, root.player)
        counts = np.array([self.N.get((id(root), move), 0) for move in valid_moves])
        if len(valid_moves) == 0:
            return valid_moves, np.array([])
        if temp == 0:
            best_move = valid_moves[np.argmax(counts)]
            probs = np.zeros(len(valid_moves))
            probs[valid_moves.index(best_move)] = 1
            return valid_moves, probs
        counts = counts ** (1. / temp)
        probs = counts / np.sum(counts)
        return valid_moves, probs


# 自对弈数据生成
def self_play(game, nnet, num_games=10):
    examples = []
    for _ in range(num_games):
        game_instance = ReversiGame()
        states, mcts_probs, current_players = [], [], []
        while True:
            # 若当前玩家无合法走子，则直接过子
            valid = game.get_valid_moves(game_instance.board, game_instance.current_player)
            if not valid:
                states.append(game_instance.board.copy())
                mcts_probs.append(np.zeros(BOARD_SIZE * BOARD_SIZE))
                current_players.append(game_instance.current_player)
                game_instance.current_player = -game_instance.current_player
                # 如果双方均无合法走子，则结束游戏
                if len(game.get_valid_moves(game_instance.board, game_instance.current_player)) == 0:
                    winner = game.get_winner(game_instance.board)
                    rewards = [1 if winner == player else -1 if winner != 0 else 0 for player in current_players]
                    for state, pi, reward in zip(states, mcts_probs, rewards):
                        examples.append((state, pi, reward))
                    break
                continue

            root = MCTS(game, nnet, num_simulations=200)
            node = MCTSNode(game_instance.board, game_instance.current_player)
            moves, probs = root.get_move_probabilities(node, temp=1)
            # 若 MCTS 返回空列表，则同样进行过子操作
            if len(moves) == 0:
                states.append(game_instance.board.copy())
                mcts_probs.append(np.zeros(BOARD_SIZE * BOARD_SIZE))
                current_players.append(game_instance.current_player)
                game_instance.current_player = -game_instance.current_player
                continue

            # 构造落子概率向量（长度 = BOARD_SIZE * BOARD_SIZE）
            pi = np.zeros(BOARD_SIZE * BOARD_SIZE)
            for move, p in zip(moves, probs):
                idx = move[0] * BOARD_SIZE + move[1]
                pi[idx] = p
            states.append(game_instance.board.copy())
            mcts_probs.append(pi)
            current_players.append(game_instance.current_player)
            # 按概率选择走法
            move = moves[np.random.choice(len(moves), p=probs)]
            game_instance.board = game.execute_move(game_instance.board, game_instance.current_player, move)
            game_instance.current_player = -game_instance.current_player
            if game.is_terminal(game_instance.board):
                winner = game.get_winner(game_instance.board)
                rewards = [1 if winner == player else -1 if winner != 0 else 0 for player in current_players]
                for state, pi, reward in zip(states, mcts_probs, rewards):
                    examples.append((state, pi, reward))
                break
    return examples

# 模型训练
def train(nnet, examples, lr, epochs=10, batch_size=32, return_losses=False):
    # 使用传入的 lr 设置优化器的学习率
    optimizer = optim.Adam(nnet.parameters(), lr=lr, weight_decay=1e-4)
    epoch_losses = []
    epoch_policy_losses = []
    epoch_value_losses = []

    # 每个 epoch 的训练过程
    for epoch in tqdm(range(epochs), desc="Training epochs"):
        np.random.shuffle(examples)
        batch_losses = []
        batch_policy_losses = []
        batch_value_losses = []
        for i in range(0, len(examples), batch_size):
            batch = examples[i:i + batch_size]
            boards = np.array([ex[0] for ex in batch])
            target_pi = np.array([ex[1] for ex in batch])
            target_v = np.array([ex[2] for ex in batch])
            boards = torch.FloatTensor(boards).unsqueeze(1).to(device)
            target_pi = torch.FloatTensor(target_pi).to(device)
            target_v = torch.FloatTensor(target_v).unsqueeze(1).to(device)
            optimizer.zero_grad()
            out_pi, out_v = nnet(boards)
            loss_v = F.mse_loss(out_v, target_v)
            loss_pi = -torch.mean(torch.sum(target_pi * F.log_softmax(out_pi, dim=1), dim=1))
            loss = loss_v + loss_pi
            loss.backward()
            optimizer.step()
            batch_losses.append(loss.item())
            batch_policy_losses.append(loss_pi.item())
            batch_value_losses.append(loss_v.item())
        avg_loss = np.mean(batch_losses)
        avg_policy_loss = np.mean(batch_policy_losses)
        avg_value_loss = np.mean(batch_value_losses)
        epoch_losses.append(avg_loss)
        epoch_policy_losses.append(avg_policy_loss)
        epoch_value_losses.append(avg_value_loss)
        print(f"Epoch {epoch+1}/{epochs}: Loss={avg_loss:.4f}, Policy Loss={avg_policy_loss:.4f}, Value Loss={avg_value_loss:.4f}")

    if return_losses:
        return epoch_losses, epoch_policy_losses, epoch_value_losses

if __name__ == "__main__":
    game = ReversiGame()
    nnet = ReversiNNet(BOARD_SIZE, dropout_p=0.3).to(device)
    all_examples = []
    num_iterations = 25  # 自对弈轮数
    global_epoch_losses = []
    global_epoch_policy_losses = []
    global_epoch_value_losses = []

    lr0 = 0.01

    for iter in range(num_iterations):
        lr = lr0 * (0.1 ** (iter / num_iterations))

        print(f"Self play iteration: {iter + 1} with learning rate: {lr}")
        examples = self_play(game, nnet, num_games=10) # 自对弈盘数
        all_examples.extend(examples)
        epoch_losses, epoch_policy_losses, epoch_value_losses = train(nnet, all_examples, lr=lr, epochs=16,
                                                                      batch_size=32, return_losses=True) # 记得修改epoch
        global_epoch_losses.extend(epoch_losses)
        global_epoch_policy_losses.extend(epoch_policy_losses)
        global_epoch_value_losses.extend(epoch_value_losses)

    # 保存训练好的模型
    torch.save(nnet.state_dict(), "reversi_model-iter25-epoch16-lr.pth") # 记得修改路径

    # 将所有轮次的训练 loss 拼在一起，画在一张图上
    total_epochs = len(global_epoch_losses)
    epochs_range = range(1, total_epochs + 1)
    plt.figure(figsize=(10, 5))
    plt.plot(epochs_range, global_epoch_losses, label="Total Loss")
    plt.plot(epochs_range, global_epoch_policy_losses, label="Policy Loss")
    plt.plot(epochs_range, global_epoch_value_losses, label="Value Loss")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.title("Combined Training Loss Metrics")
    plt.legend()
    plt.savefig("combined_training_metrics-iter25-epoch16-lr.png") # 记得修改命名
    plt.show()
