import tkinter as tk
from tkinter import messagebox
import numpy as np
import torch
from Reversi_model import ReversiGame, ReversiNNet, BOARD_SIZE

# 设置设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

class ReversiGUI:
    def __init__(self, master, first_player=1):
        self.master = master
        self.master.title("Reversi 8x8 - 人机对弈")
        self.game = ReversiGame()  # 8×8 棋盘
        self.nnet = ReversiNNet(BOARD_SIZE).to(device)
        # 加载模型
        self.nnet.load_state_dict(torch.load("reversi_model-iter25-epoch16-lr.pth", map_location=device))
        self.nnet.eval()
        self.cell_size = 60
        self.canvas = tk.Canvas(self.master, width=BOARD_SIZE * self.cell_size, height=BOARD_SIZE * self.cell_size)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.human_move)
        self.game_over = False  # 对局是否结束
        self.game.current_player = first_player  # 设置先手
        self.draw_board()
        self.update_board()
        # 开局前检测当前方是否有合法走子，无则切换
        self.check_and_switch()
        # AI 先手
        if first_player == -1:
            self.master.after(500, self.ai_move)

    def draw_board(self):
        # 绘制棋盘网格
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                x0 = j * self.cell_size
                y0 = i * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="green", outline="black")

    def update_board(self):
        # 更新棋盘上棋子的显示，并检查对局是否结束
        self.canvas.delete("piece")
        board = self.game.board
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                x0 = j * self.cell_size + 5
                y0 = i * self.cell_size + 5
                x1 = (j + 1) * self.cell_size - 5
                y1 = (i + 1) * self.cell_size - 5
                if board[i, j] == 1:
                    self.canvas.create_oval(x0, y0, x1, y1, fill="black", tags="piece")
                elif board[i, j] == -1:
                    self.canvas.create_oval(x0, y0, x1, y1, fill="white", tags="piece")
        self.master.update()
        self.check_game_over()

    def check_game_over(self):
        # 若双方均无合法走子则对局结束，弹窗显示黑白棋子数和结果
        if self.game_over:
            return
        if self.game.is_terminal(self.game.board):
            self.game_over = True
            board = self.game.board
            black_count = np.sum(board == 1)
            white_count = np.sum(board == -1)
            if black_count > white_count:
                result = "人类获胜！"
            elif white_count > black_count:
                result = "AI获胜！"
            else:
                result = "平局！"
            msg = f"对局结束！\n黑棋（人类）：{black_count} 子\n白棋（AI）：{white_count} 子\n{result}"
            messagebox.showinfo("Game Over", msg)

    def check_and_switch(self):
        # 检查当前执棋方是否有合法走子；若无则自动切换到对方
        valid_moves = self.game.get_valid_moves(self.game.board, self.game.current_player)
        if not valid_moves:
            self.game.current_player = -self.game.current_player
            self.update_board()
            if self.game.current_player == -1:
                self.master.after(500, self.ai_move)

    def human_move(self, event):
        # 仅当当前走子方为人类（黑棋）且对局未结束时响应点击
        if self.game.current_player != 1 or self.game_over:
            return
        valid_moves = self.game.get_valid_moves(self.game.board, 1)
        if not valid_moves:
            self.game.current_player = -1
            self.update_board()
            self.master.after(500, self.ai_move)
            return
        j = event.x // self.cell_size
        i = event.y // self.cell_size
        move = (i, j)
        if move in valid_moves:
            self.game.board = self.game.execute_move(self.game.board, 1, move)
            self.game.current_player = -1
            self.update_board()
            self.master.after(500, self.ai_move)

    def ai_move(self):
        # 仅当当前走子方为 AI（白棋）且对局未结束时进行落子
        if self.game.current_player != -1 or self.game_over:
            return
        valid_moves = self.game.get_valid_moves(self.game.board, -1)
        if not valid_moves:
            self.game.current_player = 1
            self.update_board()
            return
        from Reversi_model import MCTS, MCTSNode  # 确保此模块中的代码也使用GPU
        root = MCTS(self.game, self.nnet, num_simulations=400)
        node = MCTSNode(self.game.board, -1)
        moves, probs = root.get_move_probabilities(node, temp=0)
        if not moves:
            self.game.current_player = 1
            self.update_board()
            return
        move = moves[np.argmax(probs)]
        self.game.board = self.game.execute_move(self.game.board, -1, move)
        self.game.current_player = 1
        self.update_board()
        self.check_and_switch()

if __name__ == "__main__":
    root = tk.Tk()
    # 1 表示人类先手，-1 表示 AI 先手
    first_player = int(input("请输入先手方（1 表示人类先手，-1 表示 AI 先手）："))
    gui = ReversiGUI(root, first_player)
    root.mainloop()