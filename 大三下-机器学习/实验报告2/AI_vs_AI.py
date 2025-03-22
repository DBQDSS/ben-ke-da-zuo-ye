import numpy as np
import torch
from Reversi_model import ReversiGame, ReversiNNet, BOARD_SIZE, MCTS, MCTSNode, device

# ===== 模型配置（请根据需要修改下面变量） =====
MODEL1_NAME = "reversi_model-iter20-epoch20"  # 玩家1模型名称（字符串变量）
MODEL2_NAME = "reversi_model-iter20-epoch20-lr"  # 玩家2模型名称（字符串变量）
MODEL1_PATH = MODEL1_NAME + ".pth"  # 玩家1使用的模型文件路径
MODEL2_PATH = MODEL2_NAME + ".pth"  # 玩家2使用的模型文件路径
# ===================================================

def simulate_game(black_net, white_net, num_simulations=400):
    """
    模拟一局对弈：传入执黑和执白的神经网络，采用 MCTS 搜索进行落子，
    当一方无合法走子时直接切换回合，直至游戏结束，返回最终棋盘状态。
    """
    game = ReversiGame()
    while not game.is_terminal(game.board):
        valid_moves = game.get_valid_moves(game.board, game.current_player)
        if not valid_moves:
            # 当前玩家无合法走子，直接过子
            game.current_player = -game.current_player
            continue

        # 根据当前执棋方选择对应的网络
        net = black_net if game.current_player == 1 else white_net

        # 采用 MCTS 搜索选择落子（温度 temp=0 表示贪心选择）
        root = MCTS(game, net, num_simulations=num_simulations)
        node = MCTSNode(game.board, game.current_player)
        moves, probs = root.get_move_probabilities(node, temp=0)
        if len(moves) == 0:
            game.current_player = -game.current_player
            continue
        chosen_move = moves[np.argmax(probs)]
        game.board = game.execute_move(game.board, game.current_player, chosen_move)
        game.current_player = -game.current_player

    return game.board

def evaluate_game(board):
    """
    根据最终棋盘状态计算双方棋子数、胜负结果以及胜子差：
    返回：
      result: (result_black, result_white)
         其中 result_black 为1表示黑棋胜、–1表示黑棋负、0表示平局；
         result_white 则为相反。
      margin_black: 黑棋比白棋多的棋子数（可为负）；
      margin_white: 白棋比黑棋多的棋子数；
      black_count, white_count: 棋子数
    """
    black_count = np.sum(board == 1)
    white_count = np.sum(board == -1)
    if black_count > white_count:
        result = (1, -1)
    elif black_count < white_count:
        result = (-1, 1)
    else:
        result = (0, 0)
    margin_black = black_count - white_count
    margin_white = white_count - black_count
    return result, margin_black, margin_white, black_count, white_count

def main():
    num_games_each_config = 10  # 每种配置下对弈局数（共两种配置）

    # 统计两模型的对局结果
    stats = {
        "model1": {"wins": 0, "draws": 0, "losses": 0, "margin": 0.0, "games": 0},
        "model2": {"wins": 0, "draws": 0, "losses": 0, "margin": 0.0, "games": 0}
    }

    # 加载模型（ReversiNNet 与 Reversi_model_8.py 中的 BOARD_SIZE 保持一致）
    model1_obj = ReversiNNet(BOARD_SIZE).to(device)
    model2_obj = ReversiNNet(BOARD_SIZE).to(device)
    model1_obj.load_state_dict(torch.load(MODEL1_PATH, map_location=device))
    model2_obj.load_state_dict(torch.load(MODEL2_PATH, map_location=device))
    model1_obj.eval()
    model2_obj.eval()

    # 配置1：model1_obj执黑（先手），model2_obj执白（后手）
    for _ in range(num_games_each_config):
        board = simulate_game(model1_obj, model2_obj, num_simulations=400)
        (result_black, result_white), margin_black, margin_white, _, _ = evaluate_game(board)
        # 更新统计：黑棋由model1_obj执，白棋由model2_obj执
        stats["model1"]["games"] += 1
        stats["model2"]["games"] += 1
        if result_black == 1:
            stats["model1"]["wins"] += 1
            stats["model2"]["losses"] += 1
        elif result_black == -1:
            stats["model1"]["losses"] += 1
            stats["model2"]["wins"] += 1
        else:
            stats["model1"]["draws"] += 1
            stats["model2"]["draws"] += 1
        stats["model1"]["margin"] += margin_black
        stats["model2"]["margin"] += margin_white

    # 配置2：model2_obj执黑（先手），model1_obj执白（后手）
    for _ in range(num_games_each_config):
        board = simulate_game(model2_obj, model1_obj, num_simulations=400)
        (result_black, result_white), margin_black, margin_white, _, _ = evaluate_game(board)
        # 此时黑棋由model2_obj执，白棋由model1_obj执
        stats["model2"]["games"] += 1
        stats["model1"]["games"] += 1
        if result_black == 1:
            stats["model2"]["wins"] += 1
            stats["model1"]["losses"] += 1
        elif result_black == -1:
            stats["model2"]["losses"] += 1
            stats["model1"]["wins"] += 1
        else:
            stats["model2"]["draws"] += 1
            stats["model1"]["draws"] += 1
        stats["model2"]["margin"] += margin_black
        stats["model1"]["margin"] += margin_white

    # 计算胜率（以总局数计算）和平均胜子差
    for key in stats:
        games = stats[key]["games"]
        win_rate = (stats[key]["wins"] / games) * 100 if games > 0 else 0
        avg_margin = stats[key]["margin"] / games if games > 0 else 0
        stats[key]["win_rate"] = win_rate
        stats[key]["avg_margin"] = avg_margin

    # 按照要求打印结果表，使用前面声明的模型名称变量
    header = "       胜    平    负    胜率(%)    平均每局胜子"
    line1 = f"玩家1({MODEL1_NAME}): {stats['model1']['wins']:3d}  {stats['model1']['draws']:3d}  {stats['model1']['losses']:3d}   {stats['model1']['win_rate']:7.2f}      {stats['model1']['avg_margin']:7.2f}"
    line2 = f"玩家2({MODEL2_NAME}): {stats['model2']['wins']:3d}  {stats['model2']['draws']:3d}  {stats['model2']['losses']:3d}   {stats['model2']['win_rate']:7.2f}      {stats['model2']['avg_margin']:7.2f}"
    print(header)
    print(line1)
    print(line2)

if __name__ == "__main__":
    main()
