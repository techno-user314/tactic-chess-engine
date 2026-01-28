from src.players import Bot

class DefaultBot(Bot):
    def evaluate_pos(self, board):
        my_mat = self.material_count(board)
        other_mat = self.material_count(board, for_opponent=True)
        return my_mat - other_mat
